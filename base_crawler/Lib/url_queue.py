from base_crawler.Lib import queue


class Queue(object):
    """
    Url queue class
    """
    def __init__(self, timeout=5, maxsize=0):
        self.url_queue = queue.LifoQueue(maxsize)
        self.timeout = timeout

    def is_empty(self):
        """
        Check is queue empty
        """
        return self.url_queue.empty()

    def put(self, item):
        """
        Put item into queue
        """
        self.url_queue.put(item)

    def get(self):
        """
        Pop an item from queue
        """
        try:
            return self.url_queue.get(timeout=self.timeout)
        except Exception as e:
            print(e)
            return None

    def size(self):
        """
        Return the length of queue
        """
        return self.url_queue.qsize()
