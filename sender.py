import pika
import json
import socket

QUEUE_SERVER = '188.166.23.205'
QUEUE_NAME = 'pomper'

TARGET_SERVER = 'barflood.sha2017.org'
TARGET_PORT = '2342'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_SERVER, credentials=pika.PlainCredentials(username='pomper', password='pomper')))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)

def callback(ch, method, properties, body):
    decode_body = json.loads(body)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TARGET_SERVER, TARGET_PORT))
    send = sock.send
    try:
        for item in decode_body['data']:
            send('PX %d %d %02x%02x%02x%02x\n' % (item['x'], item['y'], item['color']))
    except Exception:
        import traceback
        print('er ging iets fout')
        print(traceback.print_exc())


channel.basic_consume(callback,
                      queue=QUEUE_NAME,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()