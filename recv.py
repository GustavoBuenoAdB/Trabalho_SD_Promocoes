import pika
import defs

ROUT_KEY = 'bla_bla'
ROUT_KEY2 = 'bla_bla2'

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
	bind_fila(channel, fila, exch, ROUT_KEY)
	bind_fila(channel, fila, exch, ROUT_KEY2)
	consumir(channel, fila)

def callback(ch, method, properties, body):
	print(f" [x] Received {body}")

if __name__ == '__main__':
	le_fila(defs.FILA, defs.EXCH)