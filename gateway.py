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

def envia_msg(fila, msg):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	channel.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})

	channel.basic_publish(exchange='', routing_key='hello', body=msg)
	print(" [x] Sent 'Hello World!'")

	connection.close()

def callback(ch, method, properties, body):
	print(f" [x] Received {body}")

def le_fila(fila):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	channel.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})
	channel.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)

	channel.start_consuming()

def comando_cliente():

def mostra_lista_promo():

def armazena_promo():

def envia_promo():

def envia_voto():