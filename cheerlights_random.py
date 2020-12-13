from time import sleep
from star import Star
import datetime
import random
import paho.mqtt.client as mqtt
    
step = 0.5
count = 0
star = Star(pwm=True)
leds = star.leds
dt = datetime.datetime.today()

length=25
if(dt.day < 25):
    length=dt.day
length=5
start=0
end=start+length-1
on_brightness=0.5
off_brightness=0.0

def hashval(str,size):
    hash=0
    for x in str: hash += (ord(x))
    return(hash % size)

def on_connect(client, obj, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("cheerlightsRGB")

def on_message(client, obj, msg):
    message=msg.payload.decode('UTF-8')
    print(message)
    value=int(message.replace("#",""),16) % 26
    print(value)

    avail_leds=list(range(26))
    for x in range(value):
       led=random.choices(avail_leds)[0]
       avail_leds.remove(led)
       #leds[led].value=on_brightness
       leds[led].pulse()

    for i in avail_leds:
       leds[i].value=off_brightness


def on_log(client, obj, level, msg):
    print(msg)

client = mqtt.Client()

client.on_connect  = on_connect
client.on_message = on_message
#client.on_log = on_log

client.connect("mqtt.cheerlights.com", 1883, 60)

client.loop_forever()


try:
    leds[0].pulse()
    while True:                
        for y in range(25):
            x = y+1;
            if(end<start):
                if(x>=start or x<=end+1):
                    leds[x].value=on_brightness 
                else:
                    leds[x].value=off_brightness
            else:
                if(x>=start and x<=end):
                    leds[x].value=on_brightness
                else:
                    leds[x].value=off_brightness                           
        start=(start+1)%26
        end=(end+1)%26

        sleep(0.2)

except KeyboardInterrupt:
    star.close()

