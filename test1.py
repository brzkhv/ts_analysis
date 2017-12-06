import pymongo
import matplotlib.pyplot as plt

db_client = pymongo.MongoClient('192.168.1.160', 27017)
db = db_client.bitfinex.overview
data = db.find()

# local_client = pymongo.MongoClient()
# local_db = local_client.bitfinex.overview_pi
# local_db.insert_many(data)
# for dd in data:
#     print(dd)
print(db.count())

