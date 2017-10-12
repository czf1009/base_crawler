import base_crawler.base
from base_crawler.base import BaseCrawler


class TestCrawler(BaseCrawler):
    start_urls = ['http://www.banggo.com/']

    def parse(self, response, body):
        print(response)
        print(body)


if __name__ == '__main__':
    test_crawler = TestCrawler()
    test_crawler.crawler()