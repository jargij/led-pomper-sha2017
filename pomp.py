import socket
import random
from PIL import Image
HOST = 'barflood.sha2017.org'
PORT = 2342
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
send = sock.send

def pixel(x,y,r,g,b,a=255):
    if a == 255:
        print('PX %d %d %02x%02x%02x\n' % (x,y,r,g,b))
    else:
        print('PX %d %d %02x%02x%02x%02x\n' % (x,y,r,g,b,a))

def worm(x,y,n,r,g,b):
    while n:
        pixel(x,y,r,g,b,25)
        x += random.randint(0,2)-1
        y += random.randint(0,2)-1
        n -= 1

im = Image.open('poes.png').convert('RGB')
im.thumbnail((150,150), Image.ANTIALIAS)
_,_,w,h = im.getbbox()
for x in xrange(w):
    for y in xrange(h):
        r,g,b = im.getpixel((x,y))
        pixel(x+80,y+24,r,g,b)
