import json
import subprocess
import pymongo



MONGO_CONN = pymongo.MongoClient()
DB = MONGO_CONN.interview
UNI_TAB = DB.uni

class MitmWork:
    def response(self, flow):
        if flow.request.pretty_url.startswith("https://int.51sdx.com/niuzy/uinfo/univ/univEnrollList"):
            js = json.loads(flow.response.text)
            for ele in js.get("data"):

                res = get_output(ele)
                res["_id"]= res["umId"]
                UNI_TAB.insert(res)
        else:
            print(flow.request.pretty_url) 
            


def  get_output(data):
    keys =["enrollId","lowScore","lowRank"]
    cmd = "node score.js {} {} {}".format(*[data[key] for key in keys]) 
    print(cmd)
    p = subprocess.Popen(cmd ,shell=True,stdout=subprocess.PIPE,encoding='utf-8')
    lst = p.stdout.read().split(" ")
    print(lst, 'ssss')
    for i,key in enumerate(keys):
        data[key] = lst[i].strip()
    return data

# item = {"batchName":"本科普通批","year":2021,"umId":10055605,"majorTypeId":3,"batchId":2,"courseValue":0,"univName":"南开大学(5)","enrollId":36590565,"courseGroup":"无限制","lowScore":5762,"zbType":1,"lowRank":2552}
# print(get_output(item))
addons = [MitmWork()]