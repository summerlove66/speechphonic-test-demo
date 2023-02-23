import requests
import time
import random
import redis
from selenium import webdriver

HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

REDIS_CONN = redis.StrictRedis(connection_pool=redis.ConnectionPool(host='localhost', port=6379, password="123456"))
UNI_KEY ="uni"

def get_uni_infos():
    REDIS_CONN.delete(UNI_KEY)
    for i in range(1,2):

        #原接口pageSize固定是10 ，这里为了减少请求次数，直接100。
        url = "https://int.51sdx.com/niuzy/uinfo/univ/queryUniv?pageSize=100&pageNum={}&verifyTimestamp={}".format(i,time.time()*1000)
        r = requests.get(url ,headers= HEADERS)
        for ele in r.json().get("data"):
            REDIS_CONN.rpush(UNI_KEY,ele["univId"])


def get_detail():
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    PROXY = "localhost:8888"

    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": PROXY,
      
        "sslProxy": PROXY
    }

    driver = webdriver.Firefox(capabilities=firefox_capabilities)
    
    driver.implicitly_wait(30)
    
    while True:
        if not REDIS_CONN.exists(UNI_KEY):
            break
        univ_id = REDIS_CONN.rpop(UNI_KEY).decode()

        driver.get("https://m.51sdx.com/m/est/schooldetail?univId={}&proviceId=1".format(univ_id))
        
        time.sleep(random.randint(6,26))
    


if __name__ == "__main__":
    get_uni_infos()
    get_detail()
   