import pika
import os


class server(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(os.environ.get(
            'CLOUDAMQP_URL', 'amqp://pvgvzuwg:0uQZJTh7NYP4N17Zxf4sdgjzSbW4OZT4@hedgehog.rmq.cloudamqp.com/pvgvzuwg'
        )))
        self.last_ch = ''
        self.last_method = ''
        self.message = ""

    def Connect(self):
        self.channel = self.connection.channel()

    def MakeQueue(self, queue_name1):
        self.queue_name1 = queue_name1
        self.channel.queue_declare(queue=self.queue_name1)

    def Write(self, message1, queue1):
        self.message1 = message1
        self.queue1 = queue1
        self.channel.basic_publish(exchange='',
                              routing_key=self.queue1,
                              body=self.message1)

    def Disconnect(self):
        self.connection.close()

    def callback(self, ch, method, properties, body):

        self.last_ch = ch
        self.last_method = method
        self.message = str(body)[2:-1]
        body = ""
        self.channel.stop_consuming()

    def ReadConfig(self, queue_name, auto_ack):
        self.queue_name = queue_name
        self.auto_ack = auto_ack
        self.channel.basic_consume(self.queue_name,
                              self.callback,
                              auto_ack=self.auto_ack)

    def Read(self):

        self.channel.start_consuming()
        return self.message

    def Delete(self):
        self.last_ch.basic_ack(delivery_tag=self.last_method.delivery_tag)

    def DeleteQueue(self, queue):
        self.queue = queue
        self.channel.queue_delete(queue=self.queue)