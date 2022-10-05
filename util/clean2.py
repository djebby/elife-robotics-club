import _thread as th
from network import *
from socket import *
from machine import Pin
from time import sleep
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'clubpilotebeja'
password = 'clubpilote'

station = WLAN(STA_IF)
station.active(True)
station.ifconfig(('192.168.43.100', '255.255.255.0', '192.168.43.1', '192.168.43.1'))
station.connect(ssid, password)

while station.isconnected() == False:
  pass
print('connexion établie')
print(station.ifconfig())
import gc
gc.collect()
auto=False

m11 = Pin(18, Pin.OUT)
m12 = Pin(19, Pin.OUT)
m21 = Pin(22, Pin.OUT)
m22 = Pin(23, Pin.OUT)

def avancer (a,b,c,d):
    m11.value(a)
    m12.value(b)
    m21.value(c)
    m22.value(d)
    
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
            
        if request.find('/?pompe=on')==6:
            print('pompe on')
        elif request.find('/?pompe=off')==6:
            print('pompe off')
        

        if request.find('/?dir=back')==6:
            avancer(0,1,0,1)
            print('reculer')


        elif request.find('/?dir=forward')==6:
            avancer(1,0,1,0)
            print('avancer')

        elif request.find('/?dir=right')==6:
            avancer(0,1,1,0)
            print('right')

        elif request.find('/?dir=left')==6:
            avancer(1,0,0,1)
            print('left')

        elif request.find('/?dir=stop')==6:
            avancer(0,0,0,0)
            print('stop')

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.close()
      
        
        

th.start_new_thread(web,())

th.start_new_thread(eviteur,())
        


