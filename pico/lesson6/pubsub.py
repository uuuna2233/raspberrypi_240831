import time
import binascii
import machine
from umqtt.simple import MQTTClient
from machine import Pin
import tools

def connect():
    try:
        SERVER = "192.168.0.252"
        CLIENT_ID = binascii.hexlify(machine.unique_id())
        #TOPIC = b"SA-57/ChickenHouse/temperature"
        mqtt = MQTTClient(CLIENT_ID, SERVER,user='pi',password='raspberry')
        mqtt.connect()
    except Exception:
        mqtt.disconnect()

    
def pub(TOPIC, value):
    mqtt.publish(TOPIC, f"b'{value}'")

