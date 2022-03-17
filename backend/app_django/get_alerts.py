import json
from bson import ObjectId, json_util
from pymongo import MongoClient



from django.http import JsonResponse

def get_alerts_by_page(page=1):
    serverMongo = 'localhost:27017'
    cia = "ocyan"
    client = MongoClient('mongodb://' + cia + ':' + cia + f'@{serverMongo}/{cia}')
    db = client[cia]
    alerts = []
    for alert in db.alerts.find().sort('timestamp', -1).limit((6*page)+1):
        alerts.append(alert)
    client.close()
    return alerts
