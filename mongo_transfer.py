from pymongo import MongoClient
import requests

# user -> user do mongo
# password -> senha do mongo
# db -> nome do banco no mongo
# collection -> nome da coleção no banco
# alert -> alerta, um dict
def mongo_insert_one(user="", password="", db="", collection="", alert=None):
    # Insere um novo alerta no mongo
    client = MongoClient(host="localhost", port=27017, username=user, password=password)
    db = client[db]
    collection = db[collection]
    collection.insert_one(alert)
    client.close()
    print(f"INSERTED - ID {alert['id']}")


def mongo_update_one(user="", password="", db="", collection="", alert=None):
    # Pesquisa pelo alerta no mongo e atualiza algumas informações
    client = MongoClient(host="localhost", port=27017, username=user, password=password)
    db = client[db]
    collection = db[collection]
    collection.update_one({"id": alert["id"]}, {"$set": {
        "anotacoes": alert["anotacoes"],
        "thumb_up": alert["thumb_up"],
        "thumb_down": alert["thumb_down"],
        "firebase_image_url": alert["firebase_image_url"],
        "get_opsreport": alert["get_opsreport"],
        "get_attachment": alert["get_attachment"],
        "witsml_confirm": alert["witsml_confirm"]
        }})
    client.close()
    print(f"UPDATED - ID: {alert['id']}")


# backend_ip -> ip que o django está rodando
# backend_port -> port que o django está rodando
def mongo_all(user="", password="", db="valaris", collection="alerts", backend_ip="127.0.0.1", backend_port="8000"):
    # Pega todos os dados do banco sql e salva no mongo. Cria o banco mongo
    response = requests.get(f"http://{backend_ip}:{backend_port}/api/v1/alerts/all/")
    alerts = response.json()
    client = MongoClient(host="localhost", port=27017, username=user, password=password)
    db = client[db]
    collection = db[collection]
    collection.insert_many(alerts)
    client.close()
    print("MONGO DATABASE CREATED!")
