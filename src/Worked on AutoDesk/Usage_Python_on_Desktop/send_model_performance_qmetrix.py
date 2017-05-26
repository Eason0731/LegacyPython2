import pymongo
import datetime


# Added By Wally
class mongo:
    def __init__(self, url, port, dbName, collection):
        client = pymongo.MongoClient(url, port)
        self.db = client[dbName]
        self.collection = collection

    def save(self, dic, collection = 'default-pymongo-collection##'):
        if collection == 'default-pymongo-collection##':
            insert_collection = self.collection
        else:
            insert_collection = collection
        insertID = self.db[insert_collection].save(dic)
        return insertID

def send_modeling_perf(dic):
    MONGO_PROD_URL = '10.35.131.198'
    MONGO_STG_URL = '10.148.173.92'
    mongo_stg_instance = mongo(MONGO_STG_URL, 27017, 'fusion_rating', 'model_performance')
    mongo_prod_instance = mongo(MONGO_PROD_URL, 27017, 'fusion_rating', 'model_performance')
    tile = '%s vs Rel. Build(%s)' % (dic['Build'], dic['Baseline_Build'])
    doc_windows = {
        "name" : tile,
        "platform" : "win",
        "build" : dic['Build'],
        "comparedBuild" : dic['Baseline_Build'],
        "data" : dic['Windows'],
        "time" : datetime.datetime.now()
    }

    doc_mac = {
        "name" : tile,
        "platform" : "mac",
        "build" : dic['Build'],
        "comparedBuild" : dic['Baseline_Build'],
        "data" : dic['Mac'],
        "time" : datetime.datetime.now()
    }
    mongo_stg_instance.save(doc_windows)
    mongo_prod_instance.save(doc_windows)
    mongo_stg_instance.save(doc_mac)
    mongo_prod_instance.save(doc_mac)

if __name__ == "__main__":
    dic = {}
    dic['Build'] = "2.0.2667"
    dic['Baseline_Build'] = "2.0.2604"
    dic['Windows'] = {
            "Assembly" : 1,
            "Image" : 0.99,
            "GraphicsTime" : 0.98,
            "Graphics" : 1.03,
            "POLE" : 1.04,
            "Sketch" : 0.97,
            "Solid" : 1.01,
            "Surface" : 0.99,
            "TSpline" : 0.99,
        }
    dic['Mac'] = {
            "Assembly" : 0.97,
            "Image" : 0.96,
            "GraphicsTime" : 0.98,
            "Graphics" : 1.02,
            "POLE" : 1.01,
            "Sketch" : 1.05,
            "Solid" : 0.99,
            "Surface" : 0.96,
            "TSpline" : 1.03,
        }
    send_modeling_perf(dic)
    print "Thank you!!!"

    
