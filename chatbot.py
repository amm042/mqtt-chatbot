import paho.mqtt.client as mqtt
import markovify
import random
import time
import datetime
import json
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


with open("words", "r") as f:
    words = list(filter(lambda x: len(x)> 0, f.read().split("\n")))
with open("finn.txt", "r") as f:
    text = f.read()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(text)
textModel = markovify.Text(text)

client.connect("mqtt.bucknell.edu")
last = datetime.datetime.now()

while True:
    if datetime.datetime.now() - last > datetime.timedelta(seconds=1):
        topic = random.choice(words)
        #print(topic)
        #sen = textModel.make_short_sentence(140)
        sen = textModel.make_short_sentence(140)#, max_overlap_total=100)
        print (topic, ':', sen)

        client.publish('root/'+topic+'/bot',
            json.dumps({
                'clientTime': int(time.time()),
                'message': sen,
                'iconUrl': 'https://www.eg.bucknell.edu/~amm042/ic_account_circle_white_24dp_2x.png'
            }))
        last = datetime.datetime.now()
    client.loop()
