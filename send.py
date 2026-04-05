import pika
import defs

def envia_msg(fila, msg, key, exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	channel.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})

	channel.basic_publish(exchange=exch, routing_key=key, body=msg)
	print(" [x] Sent 'Hello World!'")

	connection.close()

if __name__ == '__main__':
	envia_msg(defs.FILA,'Salve Salveeee!!', defs.KEY, defs.EXCH)
