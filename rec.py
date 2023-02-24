import paho.mqtt.client as mqtt
from analyze import analyze
import numpy as np
import cv2
import json
import sys

dump = len(sys.argv) == 2
print('dump', dump)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("flowy/raw")


prev = 0
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    image_size = (405, 720)
    img = np.frombuffer(msg.payload, np.uint8).reshape(image_size[1], image_size[0], 4)
    result, conf = analyze(img)
    conf *= 100
    conf = int(conf)
    filename = f'data/{result}.jpg'
    print(result, conf, filename)
    if dump:
        cv2.imwrite(filename, img)
    try:
        if len(result) == 9:
            consumption = int(result) / 10
            global prev
            if 0 <= (consumption-prev) < 50:
                data = json.dumps(dict(volume=consumption))
                print('publish', data)
                client.publish("flowy/status", data)
            prev = consumption
    except Exception as e:
        print(e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("nas.local")
client.loop_forever()
