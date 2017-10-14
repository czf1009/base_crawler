import copy
import logging
import threading
import time

import asyncio

from base_crawler import config
from base_crawler.Lib.downloader import Downloader
from base_crawler.Lib.url_queue import Queue

# from pymongo import MongoClient


# import objgraph


class BaseCrawler(object):
    """
    Base crawler
    """

    def __init__(self, **kwargs):
        self.queue = Queue()
        self.dupefilter = set()
        self.downloader = Downloader(self.queue)


        # logging.basicConfig(level=logging.DEBUG)
        # self.logger = logging.getLogger(__name__)

        self.dir_name = 'json_id'
        self.done_count = 0

        self.loop = asyncio.get_event_loop()
        self.start_async_loop()
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_url_items'):
            self.start_url_items = []

    @property
    def logger(self):
        """base logger"""
        logger = logging.getLogger(__name__)
        return logging.LoggerAdapter(logger, {'spider': self})

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
    def put_start_url_item(self):
        """
        Put url_item into queue
        :return:
        """
        for start_url_item in self.start_url_items:
            # url_item = {
            #     'url': '',
            #     'headers': dict(),
            #     'cookies': dict(),
            #     'post_data': dict(),
            #     'method': 'get'
            # }
            # url_item.update(start_url_item)
            # url_item = copy.deepcopy(url_item)
            start_url_item['callback'] = self.parse
            self.queue.put(start_url_item)

    def crawler(self):
        """
        异步爬取店铺ID页，并保存爬取到的json文件至本地。
        :return:
        """
        self.logger.debug('crawler')
        self.put_start_url_item()

        asyncio.set_event_loop(self.loop)

        # client = MongoClient(config.mongo_host, config.mongo_port)
        # db = client.meituan

        while True:
            empty_times = 0
            while self.queue.is_empty():
                empty_times+=1
                if empty_times > 5:
                    self.logger.info(
                        "\n\n==============================END======================\n\n")
                    return
                time.sleep(1)
            print('queue is empty')
            asyncio.run_coroutine_threadsafe(self.spider(), loop=self.loop)
            time.sleep(config.REQUEST_DELAY)


    async def spider(self):
        """
        Fetch page and save to local path
        :return:
        """
        self.logger.debug('spider')

        url_item = self.queue.get()
        if 'callback' not in url_item.keys():
            raise 'You must give callback.'
        url_item = self.init_url_item(url_item)

        resp = await self.downloader.download(url_item)
        if not resp:
            return

        # # Complete spider rule
        # await self.parse(resp)
        callback = url_item['callback']
        print(callback)
        await callback(resp)
        # # end spider

        self.done_count += 1
        self.logger.info('已经下载完成%s个页面', self.done_count)

    def init_url_item(self, url_item):
        keys = url_item.keys()
        if 'cookies' not in keys:
            url_item['cookies'] = dict()
        if 'headers' not in keys:
            url_item['headers'] = dict()
        if 'post_data' not in keys:
            url_item['post_data'] = dict()
        if 'method' not in keys:
            url_item['method'] = 'get'
        return url_item

    def parse(self, response):
        """
        parse response
        """
        raise NotImplementedError
