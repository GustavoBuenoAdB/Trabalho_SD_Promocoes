import pika
import defs

def inic_conec(exch):
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()

	channel.exchange_declare(exchange=exch, exchange_type='direct')
	channel.confirm_delivery()

	return connection, channel

def envia_msg(channel, msg, key, exch):
	channel.basic_publish(exchange=exch, routing_key=key, body=msg, properties=pika.BasicProperties(delivery_mode=2))

def main():
	connection, channel = inic_conec(defs.EXCH)

	envia_msg(channel, "TESTE", defs.KEY, defs.EXCH)

	connection.close()

if __name__ == '__main__':
	main()
