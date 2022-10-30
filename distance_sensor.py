from machine import Pin,PWM
from hcsr04 import HCSR04
from time import sleep
from dcmotor import DCMotor

frontSensor = HCSR04(trigger_pin=25, echo_pin=26)
rightSensor = HCSR04(trigger_pin=12, echo_pin=14)
leftSensor = HCSR04(trigger_pin=33, echo_pin=32)
frequency = 15000
pin3 = Pin(19, Pin.OUT)
pin4 = Pin(18, Pin.OUT)
pin5 = Pin(23, Pin.OUT)
pin6 = Pin(22, Pin.OUT)
enable = PWM(Pin(13), frequency)
M1=DCMotor(pin3,pin4,enable) # left motors
M2=DCMotor(pin5,pin6,enable) # right motors




while True:
    distance1 = frontSensor.distance_cm()
    distance2 = rightSensor.distance_cm()
    distance3 = leftSensor.distance_cm()
    
    
    if (0<distance1<25) or (0<distance2<25) or (0<distance3<25) :
        M1.stop()
        M2.stop()
        M1.backwards(2)
        M2.backwards(2)
        sleep(0.5)
        distance2 = rightSensor.distance_cm()
        distance3 = leftSensor.distance_cm()
        if distance2>20:
            M1.backwards(2)
            M2.forward(2)
            sleep(0.7)
        elif distance3>20:
            M2.backwards(2) 
            M1.forward(2)
            sleep(0.7)
            
    else:
        M1.forward(2.5)
        M2.forward(2.5)
    sleep(0.07)