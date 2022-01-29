from pymongo import MongoClient

DB_NAME = 'test'
CUSTOMER_COLLECTION = 'customer'
PRODUCT_COLLECTION = 'product'

connection_str = "mongodb://localhost:27017/"
client = MongoClient(connection_str)

db = client[DB_NAME]
customer = db[CUSTOMER_COLLECTION]
product = db[PRODUCT_COLLECTION]