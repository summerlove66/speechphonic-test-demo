import requests
import json
import time
import pymongo
import random
from lxml.html import etree 
from urllib.parse import urljoin
from   schedule import *



DOMAIN = "https://www.12309.gov.cn"

HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}


MONGO_CONN = pymongo.MongoClient()
DB = MONGO_CONN.interview
GOV_TAB = DB.gov139



class PageNode(SpiderNode):

    def parse(self):
        REDIS_CONN.delete(self.key)
        lst = list(range(1,31))
        random.shuffle(lst)
        for ele in lst:
            REDIS_CONN.rpush(self.key, ele)

class LinkNode(SpiderNode):

    @staticmethod
    def get_links(channel,page,size):
        url = "https://www.12309.gov.cn/getFileListByPage"
        r = requests.post(url,data={"codeId":"","page":page,"size":size,"fileType":"重要案件信息","channelWebPath":channel,"channelLevels":""},headers=HEADERS,proxies={"http":"http://localhost:9999","https":"https://localhost:9999"})
        js = r.json()
        if js.get("code") !=200 or item.get("title") =="":
            raise Exception("bad request", page)

        item ={}    
        for ele in js.get("results").get("hits").get("hits"):
            print(ele)

            item["date"] = ele["publishedTimeStr"]
            item["mid"] = ele["mid"]
            item["title"]=ele["title"]
            item["content"] =ele["content"]
            item["_id"] =item["mid"]
            yield item
        
            
    def parse(self):
        try:
            for ele in self. get_links("/gj/xj" ,self.val,15):
                try:
                    GOV_TAB.insert_one(ele)
                except pymongo.DuplicateKeyError:
                    pass
        except Exception as e:
            print("bad req" ,e)
            REDIS_CONN.lpush(self.key,self.val)
    
# class DetailNode(SpiderNode):

#     @staticmethod
#     def get_detail(link):

#         r = requests.get(link,headers=HEADERS)
#         r.encoding ="utf8"
#         html = r.text
#         tree= etree.HTML(html)
#         title = "".join(tree.xpath("//div[@class='detail_tit']//text()")).strip()
#         dateinfo = "".join(tree.xpath("//span[@class='fl extend1']//text()")).replace("时间：","")
#         cont = "".join(tree.xpath("//div[@id='fontzoom']//p//text()")).replace("\u2002","").strip()
#         uid = link.split("/")[-1].split(".")[0].split("_")[1]
#         return {"title":title,"date":dateinfo ,"content":cont,"link":link,"_id":uid}

#     def parse(self):
#         data = self.get_detail(urljoin(DOMAIN , self.val))
#         print(data)
#         if not data.get("title"):
#             REDIS_CONN.lpush(self.key,data["link"])
#             #raise Exception("bad request" ,data["link"])

#         GOV_TAB.insert(data)

             

if __name__ == "__main__":
    gov_sleep = Sleep_Setting("gov-sleep")
    gov_sleep.set_sleep("8-18")

    spider_list = [PageNode("gov-pages"),LinkNode("gov-links")]
 
    sch = Schedule(spider_list,gov_sleep)
    sch.initlizer()
    sch.run_spider()