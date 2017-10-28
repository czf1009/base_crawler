import re
import os
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
        # {'url': 'http://p124.sezuzu.com/2017/08/12/0318_Sacrifice_8_001.jpg'}
    ]

    async def parse(self, response):
        if not os.path.exists('imgs'):
            os.mkdir('imgs')
            
        page = await response.text()

        total_page = int(re.findall(u'尾(.*)页', page)[0])
        for i in range(2, total_page+1):
            url = '{}index{}.html'.format(response.url, i)
            url_item = {'url': url,'callback':self.next}
            self.queue.put(url_item)

        img_urls = re.findall('http://[^"]*jpg', page)
        for img_url in img_urls:
            url_item = {'url': img_url,'callback':self.down_img}
            self.queue.put(url_item)
        with open('index1.html', 'w') as f:
            for img_url in img_urls:
                img_path = 'imgs/'+img_url.split('/')[-1]
                f.write('<img src="{}"/>\n'.format(img_path))

    async def next(self, response):
        page = await response.text()
        file_name = str(response.url).split('/')[-1]
        img_urls = re.findall('http://[^"]*jpg', page)
        for img_url in img_urls:
            url_item = {'url': img_url,'callback':self.down_img}
            self.queue.put(url_item)
        with open(file_name, 'w') as f:
            for img_url in img_urls:
                img_path = 'imgs/'+img_url.split('/')[-1]
                f.write('<img src="{}"/>\n'.format(img_path))

    async def down_img(self, response):
        url = str(response.url)
        # print('start downloading page {}'.format(response.url))
        with open('imgs/'+url.split('/')[-1], 'wb') as f:
            f.write(await response.read())
        # print('page {} down'.format(response.url))


def main():
    """
    main function
    """
    test_crawler = TestCrawler()
    test_crawler.crawler()


if __name__ == '__main__':
    main()
