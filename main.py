import _thread as th
from network import *
from socket import *
from machine import Pin, PWM
from dcmotor import DCMotor
from time import sleep
import esp
esp.osdebug(None)
import gc
gc.collect()


ssid = 'Guest'
password = 'FTD-2021'
frequency = 15000

station = WLAN(STA_IF)
station.active(True)
#station.ifconfig(('192.168.43.100', '255.255.255.0', '192.168.43.1', '192.168.43.1'))
station.connect(ssid, password)

while station.isconnected() == False:
  pass
print('connexion établie')
print(station.ifconfig())

auto=False

enable = PWM(Pin(13), frequency)


pin3 = Pin(18, Pin.OUT)
pin4 = Pin(19, Pin.OUT)
dc_motor01 = DCMotor(pin3, pin4, enable)


pin5 = Pin(22, Pin.OUT)
pin6 = Pin(23, Pin.OUT)
dc_motor02 = DCMotor(pin5, pin6, enable)

s = socket(AF_INET,SOCK_STREAM)
s.bind(('', 80))
s.listen(5) 



def eviteur():
    print('a')
    while True :
        if auto:
            print('eviteur')
            sleep(1)


def web():
    global auto

    while True:
        conn,addr =s.accept()
        request =conn.recv(1024)
        request =str(request)
        print(request[:20])
        if request.find('/?mode=auto')==6:
            auto=True
            print('auto')
           
        elif request.find('/?mode=manuel')==6:
            auto=False
            
        elif request.find('/?pompe=on')==6:
            print('pompe on')

        elif request.find('/?pompe=off')==6:
            print('pompe off')
        
        elif request.find('/?dir=back')==6:
            dc_motor01.backwards(50)
            dc_motor02.backwards(50)

        elif request.find('/?dir=forward')==6:
            dc_motor01.forward(50)
            dc_motor02.forward(50)

        elif request.find('/?dir=right')==6:
            dc_motor01.forward(50)
            dc_motor02.backwards(50)

        elif request.find('/?dir=left')==6:
            dc_motor01.forward(50)
            dc_motor02.backwards(50)

        elif request.find('/?dir=stop')==6:
            dc_motor01.stop()
            dc_motor02.stop()

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.close()



th.start_new_thread(web,())
th.start_new_thread(eviteur,())