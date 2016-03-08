import re
import os

from urlparse import urljoin

from webcrawler.spiders import CrawlSpider
from webcrawler.collectors import BaseCollector
from webcrawler.post_processors import BasePostProcessor

FIXTURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)


def dummy_collector():
    class DummyCollector(BaseCollector):

        def clean(self, item):
            return item

    return DummyCollector()


def dummy_post_processor():
    class DummyPostProcessor(BasePostProcessor):

        def process(self, item):
            return None

    return DummyPostProcessor()


def dummy_spider():
    class DummySpider(CrawlSpider):
        domains = [
            re.compile(ur'.*.?gocardless.com')
        ]
        start_urls = ['http://www.gocardless.com']

        def parse(self, response, tree):

            assets_dict = {
                'img_assets': tree.xpath('//img/@src'),
                'js_assets': tree.xpath('//script/@src'),
                'css_assets': tree.xpath(
                    '//link[@rel="stylesheet"]/@href'
                )
            }

            static_assets = []
            for _, assets in assets_dict.items():
                for asset in assets:
                    # Build absolute urls for each asset so that they can be
                    # referenced in the sitemap.
                    static_assets.append(urljoin(response.url, asset))

            # Contruct the item dict which is then passed to the collector.
            sitemap_item = {
                'page_url': response.url,
                'static_assets': static_assets
            }

            return sitemap_item

    return DummySpider()


def dummy_urlopen(url):
    with open(FIXTURES_DIR + '/test_html_1.html', 'r') as f:
        html = f.read()

    return html
