import re

from base_crawler.base import BaseCrawler


class TestCrawler(BaseCrawler):
    """
    TestCrawler
    """
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
        # {'url': 'https://www.baidu.com/'}
        # {'url': 'http://www.xxmumu.com/artkt/qulingshisishibazaihui89Phanhejixiazai/'}
        {'url': 'http://www.xxmumu.com/artkt/yuanzuoharrysongaibianalexshiftqizidefengxian8fanwai123P/'}
    ]

    async def parse(self, response):
        page = await response.text()

        total_page = int(re.findall(u'尾(.*)页', page)[0])
        for i in range(2, total_page+1):
            url = '{}index{}.html'.format(response.url, i)
            url_item = {'url': url,'callback':self.next}
            self.queue.put(url_item)

        img_urls = re.findall('http://[^"]*jpg', page)
        with open('index1.html', 'w') as f:
            for img_url in img_urls:
                f.write('<img src="{}"/>\n'.format(img_url))

    async def next(self, response):
        page = await response.text()
        file_name = str(response.url).split('/')[-1]
        img_urls = re.findall('http://[^"]*jpg', page)
        with open(file_name, 'w') as f:
            for img_url in img_urls:
                f.write('<img src="{}"/>\n'.format(img_url))

    async def down_img(self, response):
        url = str(response.url)
        print('start downloading page {}'.format(response.url))
        with open(url.split('/')[-1], 'wb') as f:
            f.write(response.read())
        print('page {} down'.format(response.url))


def main():
    """
    main function
    """
    test_crawler = TestCrawler()
    test_crawler.crawler()


if __name__ == '__main__':
    main()
