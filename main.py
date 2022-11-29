import _thread as th
from network import *
from socket import *
from machine import Pin, PWM
from dcmotor import DCMotor
from time import sleep
from hcsr04 import HCSR04
import esp
#from servo import Servo

esp.osdebug(None)
import gc
gc.collect()
frontSensor = HCSR04(trigger_pin=25, echo_pin=26)
rightSensor = HCSR04(trigger_pin=12, echo_pin=14)
leftSensor = HCSR04(trigger_pin=33, echo_pin=32)



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


pin3 = Pin(19, Pin.OUT)
pin4 = Pin(18, Pin.OUT)
dc_motor01 = DCMotor(pin3, pin4, enable)


pin5 = Pin(23, Pin.OUT)
pin6 = Pin(22, Pin.OUT)
dc_motor02 = DCMotor(pin5, pin6, enable)

cleanerMotor = Pin(2, Pin.OUT)
pompeMotor = Pin(4, Pin.OUT)
cleanerMotor.value(0)
pompeMotor.value(0)

s = socket(AF_INET,SOCK_STREAM)
s.bind(('', 80))
s.listen(5) 



def eviteur():
    while True :
        if auto:
            distance1 = frontSensor.distance_cm()
            distance2 = rightSensor.distance_cm()
            distance3 = leftSensor.distance_cm()
            if (0<distance1<25) or (0<distance2<10) or (0<distance3<10) :
                dc_motor01.stop()
                dc_motor02.stop()
                dc_motor01.backwards(2)
                dc_motor02.backwards(2)
                sleep(0.5)
                distance2 = rightSensor.distance_cm()
                distance3 = leftSensor.distance_cm()
                if distance2>20:
                    dc_motor01.backwards(2)
                    dc_motor02.forward(2)
                    sleep(0.7)
                elif distance3>20:
                    dc_motor02.backwards(2) 
                    dc_motor01.forward(2)
                    sleep(0.7)
                    
            else:
                dc_motor01.forward(2.5)
                dc_motor02.forward(2.5)
            sleep(0.07)
           


def web():
    global auto
    while True:
        conn,addr =s.accept()
        request =conn.recv(1024)
        request =str(request)
        print(request[:20])
        if request.find('/?mode=auto')==6:
            auto=True
           
        elif request.find('/?mode=manuel')==6:
            auto=False
            dc_motor01.stop()
            dc_motor02.stop()
            
        elif request.find('/?pompe=on')==6:
            pompeMotor.value(1)

        elif request.find('/?pompe=off')==6:
            pompeMotor.value(0)
        
        elif request.find('/?dir=back')==6:
            dc_motor01.backwards(2)
            dc_motor02.backwards(2)

        elif request.find('/?dir=forward')==6:
            dc_motor01.forward(2.5)
            dc_motor02.forward(2.5)

        elif request.find('/?dir=right')==6:
            dc_motor01.forward(2)
            dc_motor02.backwards(2)

        elif request.find('/?dir=left')==6:
            dc_motor02.forward(2)
            dc_motor01.backwards(2)

        elif request.find('/?dir=stop')==6:
            dc_motor01.stop()
            dc_motor02.stop()
        
        elif request.find('/?servo=on') == 6:
            cleanerMotor.value(1)
        elif request.find('/?servo=off') == 6:
            cleanerMotor.value(0)
            
        #elif request.find('/?servo=on') == 6:
        #    servoMotor.duty(70)
        #elif request.find('/?servo=off') == 6:
        #    servoMotor.duty(90)
        
        
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.close()



th.start_new_thread(web,())
th.start_new_thread(eviteur,())
