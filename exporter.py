import csv
import pymongo


# 从mongod 导出数据
def export(tab, fieldnames):
    conn = pymongo.MongoClient()
    db = conn["interview"]
    collection = db[tab]

    with open('{}.csv'.format(tab), 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ele in collection .find():
            item = {k: ele[k] for k in fieldnames}
            print(item)
            writer.writerow(item)


if __name__ == "__main__":
    export("gov139", ["mid", "title", "date", "content"])

    export("uni", ['batchName',
                   'year',
                   'umId',
                   'majorTypeId',
                   'batchId',
                   'courseValue',
                   'univName',
                   'enrollId',
                   'courseGroup',
                   'lowScore',
                   'zbType',
                   'lowRank'])
