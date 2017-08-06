import pika
import json
import socket

import time

QUEUE_SERVER = '188.166.23.205'
QUEUE_NAME = 'pomper'

TARGET_SERVER = 'barflood.sha2017.org'
TARGET_PORT = 2342

connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_SERVER, credentials=pika.PlainCredentials(username='pomper', password='pomper')))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=False)

def callback(ch, method, properties, body):
    try:
        decode_body = json.loads(body.decode('utf-8'))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TARGET_SERVER, TARGET_PORT))
        send = sock.send
        try:
            messages = ""
            for item in decode_body:
                message = 'PX %d %d %s\n' % (item["x"], item["y"], item["rgb"])
                messages += message
            messages = messages.encode('utf-8')
            while True:
            # for item in range(10):
                send(messages)
                time.sleep(0.0167)
        except Exception:
            import traceback
            print('er ging iets fout')
            print(traceback.print_exc())
    except Exception:
        import traceback
        print("Er wss iets in de socket fout")
        print(traceback.print_exc())
        # callback(ch, method, properties, body)

channel.basic_qos(prefetch_count=1, all_channels=True)
channel.basic_consume(callback,
                      queue=QUEUE_NAME,
                      no_ack=False
                      )

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()