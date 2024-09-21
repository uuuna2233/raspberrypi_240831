from machine import Pin
import time

red_led = Pin(14, Pin.OUT)
button = Pin(15, Pin.IN, Pin.PULL_DOWN)

while True:
    if button.value():
        print(str(button.value()))
        red_led.toggle()
        time.sleep(0.5)