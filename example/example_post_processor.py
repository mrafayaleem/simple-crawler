import os

from jinja2 import Environment
from jinja2 import PackageLoader

from webcrawler.post_processors import BasePostProcessor

RESULT_DIR = 'result'


class ExamplePostProcessor(BasePostProcessor):

    def __init__(self):
        env = Environment(loader=PackageLoader('example', 'templates'))
        # Cache the template so we don't have to do it again for every item.
        self.template = env.get_template('sitemap_template.html')

        # Directory where result will be stored.
        self.result_dir = os.path.dirname(os.path.abspath(__file__))
        self.result_dir = os.path.join(self.result_dir, RESULT_DIR)
        self.url_count = 0

    def process(self, item):
        self.url_count += 1
        filename = str(self.url_count) + '.html'

        # Template output to be written to a file.
        output = self.template.render(
            page_url=item['page_url'],
            static_assets=item['static_assets']
        )

        with open(os.path.join(self.result_dir, filename), 'w') as f:
            # Write sitemap for a single url.
            f.write(output)
