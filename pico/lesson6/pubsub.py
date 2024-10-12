import time
import binascii
import machine
from umqtt.simple import MQTTClient
from machine import Pin

# Global variable to hold the MQTT client

def connect():
    print('yesyes')
    global mqtt
    try:
        SERVER = "192.168.0.252"
        CLIENT_ID = binascii.hexlify(machine.unique_id())
        #TOPIC = b"SA-57/ChickenHouse/temperature"
        mqtt = MQTTClient(CLIENT_ID, SERVER,user='pi',password='raspberry')
        mqtt.connect()
        
        print("MQTT connected successfully.")
    
    except Exception as e:
        print(f"MQTT connection failed: {e}")
        mqtt.disconnect()
        
        mqtt = None

    
def pub(TOPIC, value):
    global mqtt
    if mqtt is None:
        print("MQTT client is not connected.")
        return
    # Ensure mqtt is connected before publishing
    try:
        mqtt.publish(TOPIC, f"b'{value}'")
    except Exception as e:
        print(f"Failed to publish message: {e}")

