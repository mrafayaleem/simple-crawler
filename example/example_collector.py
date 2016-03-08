
from webcrawler.collectors import BaseCollector

RESULT_DIR = 'result'


class ExampleCollector(BaseCollector):

    def clean(self, item):
        """This implementation doesn't do anything to the item."""

        return item
