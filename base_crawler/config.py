import aiohttp

RETRY_HTTP_CODES = []

RETRY_TIMES = 20
REQUEST_DELAY = 0.5

# mysql
# docker数据库
IP = "127.0.0.1"
USER = "root"
PASSWD = "root"
DB_NAME = "new_hudong_db"

# MongoDB
mongo_host = '127.0.0.1'
mongo_port = 27017

# 代理配置
use_proxy = True
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = 'HQ8N7BXWV799DRJD'
proxyPass = "123723582510D114"

# # requests
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
    }
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
    }

# # aiohttp
proxy = "http://%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    }
proxy_auth = aiohttp.BasicAuth(proxyUser, proxyPass)


# selenium
service_args = [
    "--proxy-type=http",
    "--proxy=%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
    },
    "--proxy-auth=%(user)s:%(pass)s" % {
        "user": proxyUser,
        "pass": proxyPass,
    },
]
