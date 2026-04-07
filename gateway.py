import pika

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import defs

CHAVE_PRIVADA = "priv_gate.der"

def valida_assinatura(msg, assinatura, quem):
	chave_publica = CHAVE_PUBLICA[quem]

	key = RSA.import_key(open(chave_publica, 'rb').read())
	h = SHA256.new(msg)

	try:
		pkcs1_15.new(key).verify(h, assinatura)
		print("The signature is valid.")
		return True
	except (ValueError, TypeError):
		print("The signature is not valid.")
		return False

def gera_assinatura_msg(msg):
	key = RSA.import_key(open(CHAVE_PRIVADA, 'rb').read())
	msg.encode()
	h = SHA256.new(msg)
	signature = pkcs1_15.new(key).sign(h)
	return signature

def inic_conec(exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	channel.exchange_declare(exchange=exch, exchange_type='direct')
	channel.confirm_delivery()

	return connection, channel

def envia_msg(channel, msg, key, exch):
	channel.basic_publish(exchange=exch, routing_key=key, body=msg)


if __name__ == '__main__':
	main()

def inic_fila(channel, fila, exch):
	channel.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})
	channel.exchange_declare(exchange=exch, exchange_type='direct')

def bind_fila(channel, fila, exch, key):
	channel.queue_bind(exchange=exch, queue=fila, routing_key=key)

def consumir(channel, fila):
	channel.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)
	channel.start_consuming()

def le_fila(fila, exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	inic_fila(channel, fila, exch)
	bind_fila(channel, fila, exch, defs.R_KEY_GATEWAY)
	consumir(channel, fila)

def callback(ch, method, properties, body):
	print(f" [x] Received {body}")

def interface_cliente():
	print("[1] Adicionar nova promoção \n [2] Listar promoções \n [3] Votar promoções" )

def main():

	#essa função vai entrar em um loop infinito de leitura
	#le_fila(defs.FILA_GATEWAY, defs.EXCH_GATEWAY)

	#essa parada aqui, vai ter que ser uma parte do callback, leu enviou pq leu sabe, pq ler e mandar sem ser com thread vai dar pau
	connection, channel = inic_conec(defs.EXCH)
	#enviar pra promo
	envia_msg(channel, "TESTE_GATE_PROMO", defs.R_KEY_PROMOCAO, defs.EXCH)

	connection.close()

#def comando_cliente():

#def mostra_lista_promo():

#def armazena_promo():

#def envia_promo():

#def envia_voto():