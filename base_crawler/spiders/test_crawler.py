import re

from lxml import etree

from base_crawler.base import BaseCrawler


class TestCrawler(BaseCrawler):

    start_url_items = [
        # {
        #     'url': 'http://image.suning.cn/uimg/sop/richtext/189429929924297384356060.gif',
        #     'headers': {
        #         'Host': 'image.suning.cn',
        #         'Cache-Control': 'no-cache',
        #         'Content-Length': ''
        #     },
        #     'cookies': {
        #         'sessionid': '8828ed48-d2f3-4fa4-a9ee-438c42c6f4f0',
        #         'Hm_lvt_d8276dcc8bdfef6bb9d5bc9e3bcfcaf4': '1507876494'
        #     }
        # }
        {'url': 'http://www.xxmumu.com/artkt/CGshuinendeshaonv24P/'}
    ]

    async def parse(self, response):
        page = await response.text()

        total_page = re.findall(u'尾(.*)页', page)[0]
        print(total_page)

        img_urls = re.findall('<img src=[^>]*>', page)
        with open('pic.html', 'w') as f:
            for img_url in img_urls:
                f.write(img_url + '\n')

        self.logger.info('done')


def main():
    """
    main function
    """
    test_crawler = TestCrawler()
    test_crawler.crawler()


if __name__ == '__main__':
    main()
