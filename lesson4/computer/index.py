import os
import csv
from datetime import datetime
import paho.mqtt.client as mqtt
import configparser

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
# 定義回呼函式，負責 broker 收到 topic 訊息
def on_message(mosq, obj, msg):
    global temp_origin_value, led_origin_value, resistance_origin_value

    # Decode the message payload
    payload = msg.payload.decode('utf-8')

    # print("topic:{0},payload:{1},qos:{2}".format(msg.topic,msg.payload.decode('utf-8'),msg.qos)) #msg.payload是binary string
    # Define a mapping for topics to their respective variables and types
    topic_mapping = {
        f"{channel}/temperature": (float, "temp_", temp_origin_value),
        f"{channel}/light": (int, "led_", led_origin_value),
        f"{channel}/resistance": (int, "resistance_", resistance_origin_value),
    }

    value_type, value_name, origin_value = topic_mapping[msg.topic]
    new_value = value_type(payload)

    # Dynamically access the origin variable using globals()
    # Update the value only if it has changed
    if origin_value != new_value:
        globals()[value_name+'origin_value'] = new_value

        saveData(msg.topic, new_value)
        print(f"{msg.topic}: {new_value}")

# Define the callback function for when the client connects to the broker
# 定義回呼函式，負責處理當 clent 連線至broker時
def on_connect(client, userdata, flags, rc,properties=None):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic once connected
    client.subscribe(f"{channel}/#")
    
def main():
    # 必需使用 VERSION2，VERSION1 已經Deprecation
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.on_connect = on_connect
	
	# Set user ID and password
    client.username_pw_set("pi", "raspberry")
	
	# SSL連線
	# client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')	
	# Connect to the broker (replace 'broker_address' with the address of your MQTT broker)
    client.connect(host, port, 60)

    client.loop_forever()
    pass

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    host = config['broker']['host']
    port = int(config['broker']['port'])
    user = config['broker']['user']
    password = config['broker']['password']
    led_origin_value = temp_origin_value = resistance_origin_value = config['pi']['origin_value']
    channel = config['mqtt']['channel']
    main()