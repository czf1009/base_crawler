
#  @Author: Zephyr_chen
#  @Date: 2017-10-13 16:05:34
#  @Last Modified by: mikey.zhaopeng
#  @Last Modified time: 2017-10-13 16:06:10

# import asyncio
import json
import logging
import random

import aiohttp

from base_crawler import config
from base_crawler.Lib.user_agents import agents

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('downloader')


class Downloader(object):
    """
    Downloader
    """

    def __init__(self, queue):
        self.queue = queue
        # self.session = requests.Session()  # 创建一个会话接口
        # requests.adapters.DEFAULT_RETRIES = 5
        # self.session.keep_alive = False  # 访问完后关闭会话
        self.dir_name = 'json'
        self.session = aiohttp.ClientSession(conn_timeout=5)

    async def fetch_page(self, url_item):
        """
        fetch page headers and body
        """
        cookie_str = ''
        for i, j in url_item['cookies'].items():
            cookie_str += '%s=%s;' % (i, j)
        url_item['headers']['cookie'] = cookie_str
        url_item['headers']['user-agent'] = random.choice(agents)

        if config.use_proxy:
            proxy = config.proxies['http']
        else:
            proxy = None

        if url_item['method'] == 'get':
            async with self.session.get(
                    url_item['url'], headers=url_item['headers'],
                    data=json.dumps(url_item['post_data']), proxy=proxy) as response:
                await response.read()
                return response
        elif url_item['method'] == 'post':
            async with self.session.post(
                    url_item['url'], headers=url_item['headers'],
                    data=json.dumps(url_item['post_data']), proxy=proxy) as response:
                await response.read()
                return response
        else:
            raise'method:{} is invalid!'.format(url_item['method'])

    async def download(self, url_item):
        """
        return response
        """
        resp = await self.fetch_page(url_item)
        logger.info("\n正在爬取页面: %s\npost_data: %s\ncookies:%s\nheaders:%s\n状态码：%s",
                    url_item['url'], url_item['post_data'], url_item['cookies'], url_item['headers'], resp.status)

        print(resp)
        if resp.status != 200:
            self.retry(url_item)
            return False

        return resp

    def retry(self, url_item):
        
        if 'retry_times' in url_item:
            if url_item['retry_times'] <= config.RETRY_TIMES:
                url_item['retry_times'] += 1
            else:
                logger.debug('重试超过%d次,页面: %s\npost_data: %s\ncookies:%s', config.RETRY_TIMES, url_item['url'],
                             url_item['post_data'], url_item['cookies'])
                return False
        else:
            url_item['retry_times'] = 1
        self.queue.put(url_item)
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        # self.loop.close()
