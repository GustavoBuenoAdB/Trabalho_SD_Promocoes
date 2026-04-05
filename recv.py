import pika
import defs

def callback(ch, method, properties, body):
	print(f" [x] Received {body}")

def le_fila(fila, key, exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	channel.queue_declare(queue=fila, durable=True, arguments={'x-queue-type': 'quorum'})
	channel.exchange_declare(exchange=exch, exchange_type='direct')
	channel.queue_bind(exchange=exch, queue=fila, routing_key=key)
	channel.basic_consume(queue=fila, auto_ack=True, on_message_callback=callback)

	channel.start_consuming()

if __name__ == '__main__':
	le_fila(defs.FILA, defs.KEY, defs.EXCH)