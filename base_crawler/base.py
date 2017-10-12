import asyncio
import copy
import json
import logging
import threading
import time

# from pymongo import MongoClient

# import config
from base_crawler.Lib.connect_db import connect_mysql
from base_crawler.Lib.downloader import Downloader
from base_crawler.Lib.url_queue import Queue

# import objgraph


class BaseCrawler(object):
    """
    Base crawler
    """

    def __init__(self, **kwargs):
        self.queue = Queue()
        self.dupefilter = set()
        self.downloader = Downloader(self.queue)


        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.dir_name = 'json_id'
        self.request_delay = 2.5
        self.done_count = 0

        self.loop = asyncio.get_event_loop()
        self.start_async_loop()
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def __enter__(self):
        print("__enter__ method")
        return self  # 返回对象给as后的变量

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("__exit__ method")

        if exc_traceback is None:
            print("Exited without Exception")
            return True
        print("Exited with Exception")
        return False

    def start_async_loop(self):
        """
        Start download loop
        """

        def start_loop(loop):
            """Run download loop"""
            loop.run_forever()
        download_thread = threading.Thread(
            target=start_loop, args=(self.loop,))
        download_thread.setDaemon(True)  # 设置为守护线程
        download_thread.start()

    # **********************************download_page
    def put_start_urls(self):
        """
        Put url_item into queue
        :return:
        """
        url_item = {
            'url': '',
            'headers': dict(),
            'cookies': dict(),
            'post_data': dict()
        }
        for start_url in start_urls:
            url_item['url'] = start_url
            self.queue.put(copy.deepcopy(url_item))

    def crawler(self):
        """
        异步爬取店铺ID页，并保存爬取到的json文件至本地。
        :return:
        """
        self.logger.debug('crawler')
        self.put_start_urls()

        asyncio.set_event_loop(self.loop)

        # client = MongoClient(config.mongo_host, config.mongo_port)
        # db = client.meituan

        while not self.queue.is_empty():
            asyncio.run_coroutine_threadsafe(self.spider(), loop=self.loop)
            time.sleep(self.request_delay)

        self.logger.info(
            "\n\n==============================END======================\n\n")
        time.sleep(100)

    async def spider(self):
        """
        Fetch page and save to local path
        :return:
        """
        self.logger.debug('spider')

        url_item = self.queue.get()
        resp, body = await self.downloader.download(url_item)
        if not resp:
            return

        # # Complete spider rule
        self.parse(resp, body)
        # # end spider

        self.done_count += 1
        self.logger.info('已经下载完成%s个页面, 已过滤重复链接%s', self.done_count, count_dump)

    def parse(self, response, body):
        raise NotImplementedError

if __name__ == '__main__':
    start_urls = []

    start_time = time.time()

    base_crawler = BaseCrawler()
    base_crawler.crawler()

    print('店铺ID页已爬取完成，等待店铺信息与商品信息爬取完成')
    time.sleep(100)

    print('程序耗时： %f分', ((time.time() - start_time) / 60))

    # time.sleep(3600)
