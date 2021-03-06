import socket
import random
from PIL import Image
import json
import sys, getopt
import math
import pika


# Screen VARS
offset_x = 80
offset_y = 24
screen_width = 240
screen_height = 240

# Internal options
queueAddress = ''
fileName = ''
workers = 36

Matrix = []


def main(argv):
    global fileName, workers
    inputFile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:w:", ["file=", "workers="])
    except getopt.GetoptError:
        print('img_to_queue.py -i <inputfile> -w workers')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('img_to_queue.py -i <inputfile> -w workers')
            sys.exit()
        elif opt in ("-i", "--file"):
            fileName = arg
            print("File to process: " + fileName)
        elif opt in ("-w", "--workers"):
            workers = int(arg)

            if (math.sqrt(float(workers)) - int(math.sqrt(float(workers))) > 0):
                print('The square root of amount of workers is not a whole numbers. GTFO!')
                sys.exit()
            print("Amount of available workers: " + str(workers))
    pompImage()


def addPixelToWorkFile(x, y, r, g, b, index_x, index_y, Matrix):
    #print("Current index x:" + str(index_x) + " y: " + str(index_y))
    Matrix[index_x][index_y].append({'x': x, 'y': y, 'rgb': "%0.2X" % r + '' + "%0.2X" % g + '' + "%0.2X" % b})


def pompImage():
    print("Processiong image to JSON")
    im = Image.open(fileName).convert('RGB')
    im.thumbnail((240, 240), Image.ANTIALIAS)
    _, _, width, height = im.getbbox()
    # start with x and y index 1
    slice_size = int(screen_width / int(math.sqrt(workers)))
    amount_of_keys = int(screen_width / slice_size)
    print(amount_of_keys)

    w, h = amount_of_keys, amount_of_keys
    Matrix = [[[] for x in range(w)] for y in range(h)]

    # workFile = [[0 for x in range(amount_of_keys)] for y in range(amount_of_keys)]




    for x in range(width):
        index_x = int((x / slice_size))
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            index_y = int((y / slice_size))
            addPixelToWorkFile(x + offset_x, y + offset_y, r, g, b, index_x, index_y, Matrix)

            # print("Current index x:"+str(index_x)+" y: "+str(index_y)+" WORKER:"+str(index_y*index_x))
    sendToQueue(Matrix)


def sendToQueue(arrayOfWorkers):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                   credentials=pika.PlainCredentials(username='pomper',
                                                                                                     password='pomper')))
    channel = connection.channel()
    channel.queue_declare(queue='pomper', durable=False,)
    channel.queue_purge(queue='pomper')
    for worker in arrayOfWorkers:
        for pixels in worker:
            channel.basic_publish(exchange='',
                          routing_key='pomper',
                          body=json.dumps(pixels))

if __name__ == "__main__":
    main(sys.argv[1:])

