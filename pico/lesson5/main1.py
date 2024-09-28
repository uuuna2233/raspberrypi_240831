from machine import ADC, Timer, Pin, PWM, RTC
    
adcpin1 = 4
adcpin2 = 26
pwmpin1 = 15

sensor1 = ADC(adcpin1)
sensor2 = ADC(Pin(adcpin2))
pwm1 = PWM(Pin(pwmpin1))

def read_temperature(t):
    adc_value = sensor1.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    
    print(f'現在溫度: {round(temperature, 1)}')

def read_resistor(t):    
    pwm1.freq(10)
    
    duty = sensor2.read_u16()
    print(duty)
    pwm1.duty_u16(duty)
    
    print(f'可變電阻: {round(duty/65535*10)}')
    
t1 = Timer(period=200, mode=Timer.PERIODIC, callback=read_temperature)
t2 = Timer(period=200, mode=Timer.PERIODIC, callback=read_resistor)
