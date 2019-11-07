import logging
import time
import sys
import socket

from PIL import ImageGrab
from PIL import Image


udp_port = 9999
host = '' #add ip of raspi here
logging.basicConfig(filename='colorstreamer.log',level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

if len(sys.argv)>0:
	host = sys.argv[1]
	

#grab screen with antialiasing, resize t 1x1, read pixel 0,0
def get_average_color1():
	global color
	try:
		img2 = ImageGrab.grab().resize((1, 1), Image.ANTIALIAS)
		color = img2.getpixel((0, 0))
	except:
		print("error when grabbing screen")
	return '{:02x}{:02x}{:02x}'.format(*color) #format to integer of 3 decimals, separated by :


#init socket
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#sock.bind(host, udp_port)
except socket.error, msg:
	logging.error ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit(0)
logging.info ('Socket config complete - Port: ' + str(udp_port) + ' - Host: ' + host)
 
#get color and send to remote host
while (1==1):
	msg = get_average_color1()
	try :
        #Set the whole string
		sock.sendto(msg, (host, udp_port))
	except socket.error, msg:
		logging.error ('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
