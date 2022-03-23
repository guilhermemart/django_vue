import pgpubsub


def wait_for_new_alert():
    # funcao para escutar o canal_1 e travar o cursor
    # chamada na view que será chamada no frontend
    pubsub = pgpubsub.connect(user='altave', database='altave', host="localhost", password="altave")
    pubsub.listen('canal_1')
    pubsub.listen('canal_2')

    #fazer uma list ou dict pra diferenciar esse return do canal 1 e canal 2
    for e in pubsub.events():  # esse looping fica travado nesse ponto até haver algum evento no bd
        if e.payload == "mensagem_enviada":
            print("mensagem_recebida")
            return "1"
        elif e.payload == "mensagem_atualizada":
            print("atualizado")
            return "0"
        if e.channel == "canal_2":
            print("red_zone atualizado")
            return ["canal_2", e.payload]
        else:
            print(e.payload)
        return e.payload
    pubsub.unlisten('canal_1')
    pubsub.unlisten('canal_2')
