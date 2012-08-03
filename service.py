from serial import Serial
import io
from time import *
import signal
import sys
from struct import pack
import random
from subprocess import check_output
import re
from os import sys

if(sys.platform == 'win32' ):
  s = Serial(7,9600)
else:
  s = Serial('/dev/ttyACM0',9600)
  s.open()


sleep(1)

def sendMsg(message,x=0,y=0,font = 's'):
  m= pack("BBBBs",0xff,0x01,x,y,font)+message+"\x00"
  #print(m)
  s.write(m)
  s.flushOutput()
  waitDone()
def setColor(fg):
  m= pack("BBBBB",0xff,0x02,(fg&0xff),(fg >> 8) & 0xff, (fg >> 16) & 0xff)
  s.write(m)
  s.flushOutput()
  waitDone()

def setBackgroundColor(fg):
  m= pack("BBBBB",0xff,0x03,(fg&0xff),(fg >> 8) & 0xff, (fg >> 16) & 0xff)
  s.write(m)
  s.flushOutput()
  waitDone()

def fillScreen(fg):
  m= pack("BBBBB",0xff,0x04,(fg&0xff),(fg >> 8) & 0xff, (fg >> 16) & 0xff)
  s.write(m)
  s.flushOutput()
  waitDone()

def signal_handler(signal, frame):
    print "bai bai"
    s.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def clearScreen():
  s.write("\xff\x00")
  waitDone()

def waitDone():
  done = False
  while s.readline().strip()  != "SCRDONE":
    sleep(0.1)

fillScreen(0xffffff)
setBackgroundColor(0xffffff)
setColor(0x0)
if sys.platform == 'win32':
  from coretemp import *
  UpdateCoreTemp()
  #sendMsg("Coretemp:",10,5)
  cores=GetCoreTemperatures()
  for core in range(0,cores.__len__()):
    sendMsg("Core"+str(core),10,20+core*20,'s')
  while True:
    UpdateCoreTemp()
    y= 20
    temps=GetCoreTemperatures()
    loads=GetCoreLoad()
    for t in temps:
      sendMsg(str(t)+"C",220,y,'b')
      y+=20
    y=20
    for l in loads:
      sendMsg("{:^6.0%}".format(l/100.0),110,y,'b')
      y+=20
    sleep(0.5)
  
else:
  for core in range(0,4):
    sendMsg("Core"+str(core)+": ",10,10+core*25,'b')
  while True:
    y = 10
    sensors = check_output(["sensors"])
    cores=re.compile("^Core (\\d):\\s+\\+(\\d+\\.\\d+)",re.MULTILINE).findall(sensors)
    for core in cores:
      sendMsg(core[1]+"C",200,y,'b')
      y+=25
    sleep(1)
    #setColor(random.getrandbits(32))
    #sendMsg(asctime(),0,100,'b')
    #sendMsg("You Are Teh base",0,120,'s')
    

