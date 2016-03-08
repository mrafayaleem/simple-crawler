import unittest

from mock import patch
from mock import MagicMock

from webcrawler.crawlers import SimpleCrawler
from webcrawler.utils.hash import url_hash

from tests.utils import dummy_collector
from tests.utils import dummy_post_processor
from tests.utils import dummy_spider


class SimpleCrawlerTest(unittest.TestCase):

    def setUp(self):

        spider = dummy_spider()
        self.crawler_args = {
            'spider': spider,
            'collectors': [dummy_collector()],
            'post_processors': [dummy_post_processor()],
            'concurrent_requests': 1
        }

    def test_crawl(self):
        with patch('workerpool.WorkerPool', MagicMock()):
            crawler = SimpleCrawler(**self.crawler_args)

        urls = crawler._crawl(
            url='http://www.gocardless.com',
            spider=self.crawler_args['spider'],
            url_hashes=set(),
            collectors=self.crawler_args['collectors'],
            post_processors=self.crawler_args['post_processors']
        )
        self.assertEqual(len(urls), 69)

        url_hashes = set()
        url_hashes.add(url_hash('http://gocardless.com'))
        urls = crawler._crawl(
            url='http://gocardless.com',
            spider=self.crawler_args['spider'],
            url_hashes=url_hashes,
            collectors=self.crawler_args['collectors'],
            post_processors=self.crawler_args['post_processors']
        )
        self.assertEqual(len(urls), 0)
