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
        self.dir_name = 'json'
        self.ALLOWED_HTTP_CODES = [200] + config.ALLOWED_HTTP_CODES
        if config.use_proxy:
            # proxy = config.proxy
            # proxy_auth = config.proxy_auth
            self.proxy = config.proxies['http']
        else:
            self.proxy = None


    async def fetch_page(self, url_item):
        """
        fetch page headers and body
        """
        if 'cookies' in url_item.keys():
            cookie_str = ''
            for i, j in url_item['cookies'].items():
                cookie_str += '%s=%s;' % (i, j)
            url_item['headers']['cookie'] = cookie_str
            url_item['headers']['user-agent'] = random.choice(agents)

        if url_item['method'] == 'get':
            async with aiohttp.ClientSession(conn_timeout=5) as session:
                async with session.get(
                        url_item['url'], headers=url_item['headers'],
                        data=json.dumps(url_item['post_data']), proxy=self.proxy) as response:
                    if response.status in self.ALLOWED_HTTP_CODES:
                        await response.read()
                    return response
        elif url_item['method'] == 'post':
            async with aiohttp.ClientSession(conn_timeout=5) as session:
                async with session.post(
                        url_item['url'], headers=url_item['headers'],
                        data=json.dumps(url_item['post_data']), proxy=self.proxy) as response:
                    if response.status in self.ALLOWED_HTTP_CODES:
                        await response.read()
                    return response
        else:
            raise'method:{} is invalid!'.format(url_item['method'])

    async def download(self, url_item):
        """
        return response
        """
        resp = await self.fetch_page(url_item)
        # logger.info("\n正在爬取页面: %s\npost_data: %s\ncookies:%s\nheaders:%s\n状态码：%s",
        #             url_item['url'], url_item['post_data'], url_item['cookies'],
        #             url_item['headers'], resp.status)

        if resp.status not in self.ALLOWED_HTTP_CODES:
            logger.info("\033[1;31m正在爬取页面: %s  状态码：%s\033[0m", url_item['url'], resp.status)
            self.retry(url_item)
            return False

        logger.info("\033[1;32m正在爬取页面: %s  状态码：%s\033[0m", url_item['url'], resp.status)

        return resp

    def retry(self, url_item):
        """
        retry download
        """
        if 'retry_times' in url_item:
            if url_item['retry_times'] <= config.RETRY_TIMES:
                url_item['retry_times'] += 1
            else:
                logger.debug('重试超过%d次,页面: %s\npost_data: %s\ncookies:%s',
                             config.RETRY_TIMES, url_item['url'],
                             url_item['post_data'], url_item['cookies'])
                return False
        else:
            url_item['retry_times'] = 1
        self.queue.put(url_item)
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.loop.close()
        pass
