from webcrawler.crawlers import SimpleCrawler

from example_spider import ExampleSpider
from example_collector import ExampleCollector
from example_post_processor import ExamplePostProcessor


def run():
    spider = ExampleSpider()
    crawler = SimpleCrawler(
        spider=spider,
        collectors=[ExampleCollector()],
        post_processors=[ExamplePostProcessor()],
        concurrent_requests=10
    )

    crawler.start()

if __name__ == '__main__':
    run()
