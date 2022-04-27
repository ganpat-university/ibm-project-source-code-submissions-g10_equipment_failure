import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
date = datetime.datetime.now()
ORG = "2g61je"
DEVICE_TYPE = "Raspberry"
DEVICE_ID = "b827eb763d09"
TOKEN = "0PHp3GTqRisdF9k0k("
GPIO.setmode(GPIO.BOARD)
TRIG = 16
ECHO = 18
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

server = ORG + ".messaging.internetofthings.ibmcloud.com";
pubTopic1 = "iot-2/evt/status1/fmt/json";
pubTopic2 = "iot-2/evt/status2/fmt/json";
subTopic = "iot-2/type/+/id/+/evt/+/fmt/+";
authMethod = "use-token-auth";
token = TOKEN;
clientId = "d:" + ORG + ":" + DEVICE_TYPE + ":" + DEVICE_ID;

mqttc = mqtt.Client(client_id=clientId)
mqttc.username_pw_set(authMethod, token)
mqttc.connect(server, 1883, 60)
def send_email():
    fromaddr = "mrthisisemail@gmail.com"
    toaddr = "adarsh62656@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Alert: Server Room  "
    body = "We find that the Product is not there So please check the machine is it working or not working"+"\n Thank You\nTime:"+time.strftime("%H:%M:%S")+"\nDate:"+date.strftime("%d")+"/"+date.strftime("%b")+"/"+date.strftime("%Y")+"\nEncountered 10 Seconds of inactivity"
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Mrs@email0")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
def product_distance():
        try:
                GPIO.output(TRIG, True)
                time.sleep(0.00001)
                GPIO.output(TRIG, False)
                while GPIO.input(ECHO)==0:
                        pulse_start = time.time()
                while GPIO.input(ECHO)==1:
                        pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                distance = round(distance+1.15, 2)
                #mqttc.publish(pubTopic1, min(99,distance))
                print min(99,distance)
                return min(99,distance)
        except KeyboardInterrupt:
                GPIO.cleanup()
while True:
        mini=float('inf')
        maxi=0
        flag=0
        start=time.time()
        li=[0 for i in range(10)]
        for i in range(600):
                time.sleep(1)
                li.append(product_distance())
                li.pop(0)
                if i>9:
                        if  min(li)==max(li) and min(li)==99 and flag==0:
                                send_email()
                                body = "We find that the Product is not there So please check the machine is it working or not working"+"\n Thank You\nTime:"+time.strftime("%H:%M:%S")+"\nDate:"+date.strftime("%d")+"/"+date.strftime("%b")+"/"+date.strftime("%Y")+"\nEncountered 10 Seconds of inactivity"
                                mqttc.publish(pubTopic1,body)
                                flag==1
mqttc.loop_forever()