from machine import Pin,PWM
from servo import Servo
from hcsr04 import HCSR04
from time import sleep
s=Servo(Pin(13))
sensor = HCSR04(trigger_pin=25, echo_pin=26)

while True:
    distance = sensor.distance_cm()
    sleep(1)
    print('Distance:',int(distance),'cm')
    if 0<int(distance )< 10:
        s.write_angle(90)
    else:
        s.write_angle(0)
        
    sleep(2)
        

   
    
