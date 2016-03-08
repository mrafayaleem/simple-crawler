import workerpool
import logging
import threading

from urllib2 import urlopen
from urlparse import urljoin
from Queue import Queue

from lxml import etree

from utils.xpath import build_abs_url_xpath
from utils.xpath import build_relative_url_xpath
from utils.url import is_url_in_domain
from utils.url import is_absolute
from utils.hash import url_hash
from utils.stdout import setup_stdout

setup_stdout()
logger = logging.getLogger('webcrawler')

# A list of extensions that we would ignore when encountered in href links
IGNORED_HREF_EXTENSIONS = [
    # frontend
    '.css', 'js',

    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',
]


class SimpleCrawler(object):
    """A recursive exhaustive crawler implementation.
    """

    # Build absolute url xpath to extract absolute urls from doc
    abs_url_xpath = build_abs_url_xpath(
        IGNORED_HREF_EXTENSIONS
    )

    # Build relative url xpath to extract relative urls from doc
    relative_url_xpath = build_relative_url_xpath(
        IGNORED_HREF_EXTENSIONS
    )

    _lock = threading.Lock()

    def __init__(
            self, spider, collectors=None,
            post_processors=None, concurrent_requests=1):
        self.pool = workerpool.WorkerPool(size=concurrent_requests)
        self.spider = spider
        self.collectors = collectors if collectors else []
        self.post_processors = post_processors if post_processors else []

        self.result = Queue()
        self.url_hashes = set()

    def start(self):
        """The entry point for the crawler. It starts from the start urls
        and crawls exhaustively on them. Implemented using the workerpool
        pattern.
        """

        more_urls = []
        for url in self.spider.start_urls:
            _hash = url_hash(url)
            if is_absolute(url) and is_url_in_domain(
                    url, self.spider.domains) and (_hash not in self.url_hashes):

                # Collect urls from start_urls
                more_urls = more_urls + self._crawl(
                    url=url,
                    spider=self.spider,
                    url_hashes=self.url_hashes,
                    collectors=self.collectors,
                    post_processors=self.post_processors
                )

        # Start asynchronous crawls and keep on crawling until all urls are
        # exhasuted
        while more_urls:
            # While we have more urls, send these urls to workers to process
            # and collect new urls discovered within the html and repeat.
            # This is the actual implementation for exhaustive crawling.
            _more_urls = self.pool.map(
                lambda x: self._crawl(
                    x, self.spider, self.url_hashes, self.collectors,
                    self.post_processors
                ), more_urls
            )

            # For more discovered urls, reduce all the results to a single
            # big list.
            more_urls = reduce(lambda x, y: x + y, _more_urls)

        # Wait for all the workers to finish the job and shutdown gracefully.
        self.pool.shutdown()
        self.pool.join()

    @classmethod
    def _crawl(cls, url, spider, url_hashes, collectors, post_processors):

        _blank = []

        # Add hashes using a lock to avoid race condition between worker
        # threads.
        with cls._lock:
            if url_hash(url) in url_hashes:
                return _blank
            else:
                url_hashes.add(url_hash(url))

        # If a request fails, log and return
        try:
            logger.info('Crawling: %s', url)
            response = urlopen(url)
        except Exception as e:
            logger.error('Request failed for url %s Exception: %s', url, e)
            return _blank

        # If parsing fails, log and return
        try:
            htmlparser = etree.HTMLParser()
            tree = etree.parse(response, htmlparser)
        except Exception as e:
            logger.error(
                'Failed parsing response for url %s Exception: %s', url, e)
            return _blank

        try:
            abs_urls = tree.xpath(
                cls.abs_url_xpath,
                namespaces={"re": "http://exslt.org/regular-expressions"}
            )
        except Exception as e:
            logger.error('Absolute url extraction failed for %s', url)
            abs_urls = []

        try:
            relative_urls = tree.xpath(
                cls.relative_url_xpath,
                namespaces={"re": "http://exslt.org/regular-expressions"}
            )
        except Exception as e:
            logger.error('Relative url extraction failed for %s', url)
            relative_urls = []

        # Filter out all absolute urls that are outside of domain. This is
        # only valid for absolute urls as relative urls are always within
        # the domain.
        abs_urls = filter(
            lambda x: is_url_in_domain(x, spider.domains), abs_urls
        )

        # Build absolute urls from relative urls and merge in abs_urls.
        abs_urls = abs_urls + [urljoin(url, r_url) for r_url in relative_urls]
        logger.info('%s more urls discovered on %s', len(abs_urls), url)

        urls_to_crawl = []

        # At this point, we are sure that every url in abs_urls is absolute
        # and lies within the domain. Next, we filter which url to actually
        # crawl.
        for abs_url in abs_urls:
            _hash = url_hash(abs_url)
            if _hash not in url_hashes:
                urls_to_crawl.append(abs_url)

        # Here we call the spider parse method and pass the result to the
        # collectors.
        try:
            parsed = spider.parse(response, tree)
        except Exception as e:
            logger.error('Error parsing HTML for %s: Exception %s', url, e)
        else:
            logger.info('Parsed HTML for %s', url)
            try:
                parsed = reduce(
                    lambda x, y: y.clean(x),
                    collectors, parsed
                )
            except Exception as e:
                logger.error('Error cleaning %s: Exception %s', url, e)
            else:
                try:
                    for post_procesor in post_processors:
                        post_procesor.process(parsed)
                except Exception as e:
                    logger.error(
                        'Error post processing %s: Exception %s', url, e)

        return urls_to_crawl
