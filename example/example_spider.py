import re

from urlparse import urljoin

from webcrawler.spiders import CrawlSpider


class ExampleSpider(CrawlSpider):

    # Domains are always regexes
    domains = [
        re.compile(ur'.*.?dubizzle.com')
    ]
    start_urls = ['http://dubai.dubizzle.com']

    def parse(self, response, tree):

        img_assets = tree.xpath('//img/@src')
        js_assets = tree.xpath('//script/@src')
        css_assets = tree.xpath(
            '//link[@rel="stylesheet"]/@href'
        )

        assets_dict = {
            'img_assets': img_assets,
            'js_assets': js_assets,
            'css_assets': css_assets
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
