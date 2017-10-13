from base_crawler.base import BaseCrawler


class TestCrawler(BaseCrawler):
    
    start_url_items = [
        {
            'url': 'http://image.suning.cn/uimg/sop/richtext/189429929924297384356060.gif',
            'headers': {
                # 'Host': 'image.suning.cn',
                # 'Cache-Control': 'no-cache',
                'Content-Length': ''
            },
            # 'cookies': {
            #     'sessionid': '8828ed48-d2f3-4fa4-a9ee-438c42c6f4f0',
            #     'Hm_lvt_d8276dcc8bdfef6bb9d5bc9e3bcfcaf4': '1507876494'
            # }
        }
        # {'url': 'http://image.suning.cn/uimg/sop/richtext/136024498895054476743920.gif'}
        # {'url': 'http://image.suning.cn/uimg/sop/richtext/189429929924297384356060.gif'}
    ]


    async def parse(self, response):
        print(response)
        with open('test.jpg', 'wb')as f:
            f.write(await response.read())
        print('done')


def main():
    """
    main function
    """
    test_crawler = TestCrawler()
    test_crawler.crawler()

if __name__ == '__main__':
    main()