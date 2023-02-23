import random
import redis
import time
import traceback


REDIS_CONN = redis.StrictRedis(connection_pool=redis.ConnectionPool(
    host='localhost', port=6379, password="123456"))


class SpiderNode:
    def __init__(self, key):
        self.key = key
        self.val = None

    def set_val(self, val):
        self.val = val

    def parse():
        pass


class Sleep_Setting:
    def __init__(self, name):
        self.name = name

    def set_sleep(self, sleep_info: str):
        '''
        @sleep_info : 10-20
        '''

        REDIS_CONN.set(self.name, sleep_info)

    def sleep(self):
        if not REDIS_CONN.exists(self.name):
            return
        sleep_info = REDIS_CONN.get(self.name).decode().split("-")
        time.sleep(random.randint(int(sleep_info[0]), int(sleep_info[1])))


class Schedule:
    def __init__(self, spider_node_list: list, sleep_setting: Sleep_Setting):
        self.spider_node_list = spider_node_list
        self.sleep_setting = sleep_setting

    def initlizer(self):
        start_node = self.spider_node_list[0]
        REDIS_CONN.delete(start_node.key)
        start_node.parse()

    def run_spider(self, catch_error_link=False, catch_exception=False, except_wait=30):
        '''

        :param spider_node_list:   list 爬虫层级列表
        :param catch_error_link: boolean  遇到错误时 是否将链接重新放回缓存
        :param catch_exception: boolean  是否捕获错误
        :param except_wait: int 某一层级遇到错误时停止 在捕获错误时 需要重新运行的话 ，需暂停的时间
        :return:
        '''

        for i in range(1, len(self.spider_node_list)):
            while True:
                redis_key = self.spider_node_list[i - 1].key
                k = REDIS_CONN.rpop(redis_key)

                print(k)
                if k == None:
                    break
                _layer = self.spider_node_list[i]
                _layer.set_val(k.decode())
                print("layer {}:{}".format(_layer, k.decode()))
                try:
                    _layer.parse()
                    self.sleep_setting.sleep()
                except Exception as e:
                    print("CRAWLER ERROR ", e)
                    traceback.print_exc()
                    if not catch_exception:
                        raise Exception()
                    else:
                        time.sleep(except_wait)
                finally:
                    if catch_error_link:
                        REDIS_CONN.lpush(redis_key, _layer.val)
