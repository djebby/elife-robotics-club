from machine import Pin,PWM
from hcsr04 import HCSR04
from time import sleep
from dcmotor import DCMotor

frontSensor = HCSR04(trigger_pin=25, echo_pin=26)
rightSensor = HCSR04(trigger_pin=12, echo_pin=14)
leftSensor = HCSR04(trigger_pin=33, echo_pin=32)
pin3 = Pin(18, Pin.OUT)
pin4 = Pin(19, Pin.OUT)
pin5 = Pin(22, Pin.OUT)
pin6 = Pin(23, Pin.OUT)
enable = PWM(Pin(13), frequency)
M1=DCMotor(pin3,pin4,enable)
M2=DCMotor(pin5,pin6,enable)




while True:
    distance1 = frontSensor.distance_cm()
    distance2 = rightSensor.distance_cm()
    distance3 = leftSensor.distance_cm()
    if distance<25:
        sleep(1)
        M1.stop()
        M2.stop()
        if distance2>20:
            M1.backwards(20)
            M2.forward(20)
        elif distance3>20:
            M2.backwards(20)
            M1.forward(20)
            
    else:
        M1.forward(20)
        M2.forward(20)
    sleep(2)
        
        
