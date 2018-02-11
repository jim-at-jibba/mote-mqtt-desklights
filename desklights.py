import paho.mqtt.client as mqttClient
import time

import motephat as mote
from colorsys import hsv_to_rgb

mote.configure_channel(1, 16, False)

def hex_to_rgb(value):
    value = value.lstrip("#")
    length = len(value)
    return tuple(int(value[i:i + length // 3], 16) for i in range(0, length, length // 3))

def mote_on():
    for channel in range(4):
        for pixel in range(16):
            mote.set_pixel(channel + 1, pixel, 255,255,255, 0.7)
        time.sleep(0.01)

    mote.show()

def mote_change(c):
    r,g,b = hex_to_rgb(c)
    print(r,g,b)
    for channel in range(4):
        for pixel in range(16):
            mote.set_pixel(channel + 1, pixel, r,g,b, 0.5)
        time.sleep(0.01)

    mote.show()

def mote_off():
    mote.clear()
    mote.show()

def on_connect(client, userData, flags, rc):
    if rc == 0:
        print("Connected to broker")

        global Connected
        Connected = True
    else:
        print("Connection Failed")

def on_message(client, userData, message):
    bytes = message.payload
    string = "".join(map(chr,bytes))
    print("Message received: " + string)

    if string == "0":
        mote_off()
    elif string == "1":
        mote_on()
    else:
        mote_change(string)

Connected = False # global variable to track connectivity

broker_address = '192.168.1.217'
port = 1883

client = mqttClient.Client("DeskPi")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address,port=port)
client.loop_start()

while Connected != True:
    time.sleep(0.1)

client.subscribe("test")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
