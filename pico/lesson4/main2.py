from machine import Timer, Pin

green_led = Pin(14, Pin.OUT)
green_count = 0

def green_led_mycallback(t):
    global green_count
    green_count += 1
    print(f"green_led目前執行:{green_count}次")
    green_led.toggle()
    
    if green_count == 100:
        t.deinit()

green_led_timer = Timer(mode=Timer.PERIODIC, period=1000, callback=green_led_mycallback)

red_led = Pin(15, Pin.OUT)
red_count = 0

def red_led_mycallback(t):
    global red_count
    red_count += 1
    print(f"red_led目前執行:{red_count}次")
    red_led.toggle()
    
    if red_count == 50:
        t.deinit()
        
red_led_timer = Timer(mode=Timer.PERIODIC, period=2000, callback=red_led_mycallback)
