from base_crawler.base import BaseCrawler


class TestCrawler(BaseCrawler):
    start_urls = ['http://www.banggo.com/']


    def parse(self, response, body):
        print(response)
        print(body)


def main():
    """
    main function
    """
    test_crawler = TestCrawler()
    test_crawler.crawler()

if __name__ == '__main__':
    main()