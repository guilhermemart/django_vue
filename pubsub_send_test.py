# rodar esse codigo escreve uma mensagem no bd
# usada para testar o watchdog
import pgpubsub


def send_event():
    pubsub = pgpubsub.connect(dbname="altave", user='altave', password='altave', host="localhost")
    pubsub.notify('canal_1', 'mensagem_enviada')


if __name__ == "__main__":
    send_event()