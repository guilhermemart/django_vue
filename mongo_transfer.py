from pymongo import MongoClient
import requests

#backend_ip -> ip que o django está rodando
#backend_port -> port que o django está rodando
#db -> nome do banco no mongo
#collection -> nome da coleção no banco
def transfer_and_update(backend_ip="192.168.0.46", backend_port="8000", db="valaris", collection="alerts"):
    response = requests.get(f"http://{backend_ip}:{backend_port}/api/v1/alerts/all/")
    alerts = response.json()
    client = MongoClient("localhost", 27017)
    db = client[db]
    collection = db[collection]
    docs = collection.find()
    # Salva os docs sem o '_id' que o mongo coloca
    docs_to_compare = []
    for doc in docs:
        doc.pop("_id", None)
        docs_to_compare.append(doc)

    for alert in alerts:
        # Verifica se o alerta tem algum valor diferente do banco
        if alert not in docs_to_compare:
            # Verifica se o alerta está no banco (pelo id)
            if next((item for item in docs_to_compare if item["id"] == alert["id"]), None):
                # Tem no banco, então irá atualizar
                collection.update_one({"id": alert["id"]}, {"$set": {
                    "anotacoes": alert["anotacoes"],
                    "thumb_up": alert["thumb_up"],
                    "thumb_down": alert["thumb_down"],
                    "firebase_image_url": alert["firebase_image_url"],
                    "get_opsreport": alert["get_opsreport"],
                    "get_attachment": alert["get_attachment"],
                    "witsml_confirm": alert["witsml_confirm"]}})
                print(f"UPDATED - ID: {alert['id']}")
            else:
                # Não tem no banco, então inserta
                collection.insert_one(alert)
                print(f"INSERTED - ID: {alert['id']}")
