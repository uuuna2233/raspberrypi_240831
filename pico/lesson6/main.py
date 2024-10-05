import tools, pubsub
from machine import ADC, Timer, Pin, PWM, RTC

sensor1 = ADC(4) # 內建溫度
sensor2 = ADC(Pin(28)) # 光敏電阻
sensor3 = ADC(Pin(26)) # 可變電阻
pwm1 = PWM(Pin(15)) # PWM LED

class SensorManager:
    def __init__(self):
        pass

    def read_temperature(self):
        ''' 偵測溫度 '''
        
        adc_value = sensor1.read_u16()
        volt = (3.3/65535) * adc_value
        temperature = 27 - (volt - 0.706)/0.001721
        temp_value = round(temperature, 1)
        
        return temp_value
        
    def read_light(self):
        ''' 偵測光線 '''
        
        adc_value = sensor2.read_u16()
        
        return adc_value

    def read_resistance(self):
        ''' 可變電阻改變 LED 亮度 '''
        
        pwm1.freq(50)
        
        duty = sensor3.read_u16() # 電壓轉為 16進制
        pwm1.duty_u16(duty)
        light_level = round(duty/65535*10)
        
        return light_level

    def read_all(self, t):
        '''
        一次性讀取所有感測器的數據
        :param t:Timer 的實體，每 2秒執行 1次
        '''
        
        readings = {
            "現在溫度": self.read_temperature(),
            "現在光線": self.read_light(),
            "可變電阻": self.read_resistance()
        }
        for sensor, value in readings.items():
            pubsub.pub(f'SA-01/{sensor}', f'{value}')
    
if __name__ == "__main__":
    try:
        tools.connect()
        pubsub.connect()
    except RuntimeError as e:
        print(e)
    except Exception:
        print('Unknown Error')
    else:
        manager = SensorManager()
    #   t = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t: manager.read_all())
        t = Timer(period=1000, mode=Timer.PERIODIC, callback=manager.read_all)
    


