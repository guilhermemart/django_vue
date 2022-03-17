import pgpubsub


def wait_for_new_alert():
    # funcao para escutar o canal_1 e travar o cursor
    # chamada na view que será chamada no frontend
    pubsub = pgpubsub.connect(user='altave', database='altave', host="localhost", password="altave")
    pubsub.listen('canal_1')
    for e in pubsub.events():  # esse looping fica travado nesse ponto até haver algum evento no bd
        if e.payload == "mensagem_enviada":
            print("mensagem_recebida")
        elif e.payload == "mensagem_atualizada":
            print("atualizado")
        else:
            print(e.payload)
        return e.payload
    pubsub.unlisten('canal_1')
