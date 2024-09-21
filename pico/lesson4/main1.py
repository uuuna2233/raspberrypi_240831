from machine import Pin, PWM
import time, random

led = Pin(15, mode=Pin.OUT)
'''
while True:
    for i in (0,1):
        led.value(i)
        delay = random.randint(0,2)
        time.sleep(delay)
        print(delay)
'''

ledpwm = PWM(led)
ledpwm.freq(1000)

while True :
    for i in range(65535):
        ledpwm.duty_u16(i)
#        time.sleep(0.005)
    for i in range(65535, -1, -1):
        ledpwm.duty_u16(i)
#        time.sleep(0.005)

        