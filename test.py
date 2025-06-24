from pymongo import MongoClient

try:
    client = MongoClient("mongodb+srv://sidiqolasode:8khpTX3g8Wc3tg9f@eviladvice.sszqwnn.mongodb.net/?retryWrites=true&w=majority&appName=eviladvice")
    client.admin.command("ping")
    print("✅ MongoDB is connected!")
except Exception as e:
    print("❌ MongoDB not connected:", e)
