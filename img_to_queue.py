import socket
import random
from PIL import Image
import json
import sys, getopt

HOST = 'barflood.sha2017.org'
PORT = 2342
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
send = sock.send

offset_x = 80
offset_y = 24
queueAddress = ''
fileName = ''

def main(argv):
	inputFile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'img_to_queue.py -i <inputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'img_to_queue.py -i <inputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			fileName = arg
			print("File to process: "+fileName)
	pompImage()
		

def pixel(x,y,r,g,b,a=255):
    if a == 255:
		json.dumps({'meta':{}, 'data':{'x':x, 'y':y, 'r':r, 'g':g, 'b':b}})
    else:
		json.dumps({'meta':{}, 'data':{'x':x, 'y':y, 'r':r, 'g':g, 'b':b, 'a':a}})


def pompImage():
	print("Processiong image to JSON")
	im = Image.open(fileName).convert('RGB')
	im.thumbnail((150,150), Image.ANTIALIAS)
	_,_,w,h = im.getbbox()
	for x in xrange(w):
		for y in xrange(h):
			r,g,b = im.getpixel((x,y))
			pixel(x+offset_x,y+offset_y,r,g,b)

if __name__ == "__main__":
   main(sys.argv[1:])

