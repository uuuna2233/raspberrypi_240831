import os
import csv
from datetime import datetime
import paho.mqtt.client as mqtt

def saveData(topic,value):
    root_dir=os.getcwd()
    data_path=os.path.join(root_dir,"data")

    # 沒有目錄，建立目錄
    if not (os.path.isdir(data_path)):
        print("資料夾不存在")
        os.mkdir("data")

    # 獲取當前時間並格式化為字串
    current_date = datetime.today().strftime("%Y-%m-%d")
    filename = f"{current_date}.csv"
    filepath=os.path.join(data_path,filename)

    current_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # 定義 CSV 標題
    header = ['時間', '設備', '值']

    # 沒有檔案，建立檔案
    if not (os.path.exists(filepath)):
        # 創建 CSV 檔案並寫入標題
        with open(filepath, mode='w', encoding='utf-8-sig', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)  # 寫入標題行
            csvwriter.writerow([current_time, topic, value])
    else:
        with open(filepath, mode='a', encoding='utf-8-sig', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([current_time, topic, value])

# Define the callback function for when a message is received
# 定義回呼函式,負責bloker收到topic訊息
def on_message(mosq, obj, msg):
    global temp_origin_value
    global led_origin_value
    global resistance_origin_value

    #print("topic:{0},payload:{1},qos:{2}".format(msg.topic,msg.payload.decode('utf-8'),msg.qos)) #msg.payload是binary string
    if msg.topic=="SA-57/temperature":
        temperature=float(msg.payload.decode('utf-8'))
        if temp_origin_value!=temperature:
            temp_origin_value=temperature
            saveData("Temperature",temperature)
            print(f"Temperature:{temperature}")
    elif msg.topic=="SA-57/light":
        led_level=int(msg.payload.decode('utf-8'))
        if led_origin_value!=led_level:
            led_origin_value=led_level
            saveData("LightLevel",led_level)
            print(f"LightLevel:{led_level}")

    elif msg.topic=="SA-57/resistance":
        resistance=int(msg.payload.decode('utf-8'))
        if resistance_origin_value!=resistance:
            resistance_origin_value=resistance
            saveData("resistance",resistance)
            print(f"resistance:{resistance}")
    
# Define the callback function for when the client connects to the broker
# 定義回呼函式,負責處理當clent連線至broker時
def on_connect(client, userdata, flags, rc,properties=None):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic once connected
    client.subscribe("SA-57/#")
    
def main():
    #必需使用VERSION2,VERSION1已經Deprecation
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.on_connect = on_connect
	
	# Set user ID and password
    client.username_pw_set("pi", "raspberry")
	
	#SSL連線
	#client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    # 	
	# Connect to the broker (replace 'broker_address' with the address of your MQTT broker)
    client.connect("192.168.0.252", 1883, 60)

    client.loop_forever()
    pass

if __name__ == "__main__":
    led_origin_value=0
    temp_origin_value=0
    resistance_origin_value=0
    main()