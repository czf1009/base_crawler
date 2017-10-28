import logging
import threading
import time
import functools

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

    def callback(self, url, future):
        if future.exception():
            self.logger.error("\n\033[1;31mException: %s\nurl: %s\033[0m" % (future.exception(), url))
            # print(type(future.exception()))
        self.logger.info("\033[1;32mfuture.result: %s\033[0m" % future.result())

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
            if self.queue.is_empty():
                # print('queue is empty')
                # if len(asyncio.Task.all_tasks()) == 0:
                #     self.download_thread.is_dead()
                #     self.logger.info(
                #         "\n\n==============================END======================\n\n")
                #     return
                is_done = True
                for task in asyncio.Task.all_tasks():
                    # print('task: %s' % task)
                    if not task.done():
                        print('Task running')
                        # print('task: %s' % task)
                        is_done = False
                        break
                if is_done:
                    self.logger.info(
                        "\n\n==============================END======================\n\n")
                    return
                time.sleep(2)
            else:
                url_item = self.queue.get()
                # print('url_item: %s' % url_item)
                asyncio.run_coroutine_threadsafe(self.spider(url_item), loop=self.loop).add_done_callback(functools.partial(self.callback, url_item['url']))
                time.sleep(config.REQUEST_DELAY)

    async def spider(self, url_item):
        """
        Fetch page and save to local path
        :return:
        """
        # self.logger.debug('spider')

        if 'callback' not in url_item.keys():
            raise 'You must give callback.'
        url_item = self.init_url_item(url_item)

        resp = await self.downloader.download(url_item)
        if not resp:
            return

        # # Complete spider rule
        # await self.parse(resp)
        callback = url_item['callback']
        # print(callback)
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
