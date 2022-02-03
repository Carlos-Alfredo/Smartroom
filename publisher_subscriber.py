#import RPi.GPIO as GPIO
import time
#import serial
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
import asyncio
import threading

IOTHUB_DEVICE_CONNECTION_STRING = 'HostName=ServidorIoT.azure-devices.net;DeviceId=DispositivoTeste;SharedAccessKey=vI0U2HxL1HV/60SVzXoskPCAhNZpmmN28r1ilGaiKfs='
CONNECTION_STR = "Endpoint=sb://testeiotbroker.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Tig31UtDJ9LY+epBCrzehYnPtM3KvbLjxMU9SycGcKY="
TOPIC_NAME = "telemetria"
SUBSCRIPTION_NAME = "Gerenciador_de_atuadores"

#arduino = serial.Serial('/dev/ttyUSB0', 9600)

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(27,GPIO.OUT)
#GPIO.setup(23,GPIO.OUT)

def send_telemetry(sender, telemetry_message):
    message = ServiceBusMessage(json.dumps(telemetry_message))
    # send the message to the topic
    with sender:
        sender.send_messages(message)


def thread_telemetria(servicebus_client,TOPIC_NAME):
    while(True):
        '''temperatura = arduino.readline()
        temperatura = temperatura.decode("utf-8")
        temperatura = float(temperatura)
        print(temperatura)
        umidade = arduino.readline()
        umidade = umidade.decode("utf-8")
        umidade = float(umidade)
        print(umidade)
        luminosidade = arduino.readline()
        luminosidade = luminosidade.decode("utf-8")
        luminosidade = int(luminosidade)
        print(luminosidade)
        presenca = arduino.readline()
        presenca = presenca.decode("utf-8")
        presenca = int(presenca)
        print(presenca)'''
        temperatura=28
        umidade=88
        luminosidade=188
        presenca=1
        dispositivo = "Raspberry Pi + Arduino"
        
        dados = {
            "temperatura": temperatura,
            "umidade": umidade,
            "luminosidade": luminosidade,
            "presenca": presenca
        }
        with servicebus_client:
            sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
            send_telemetry(sender, dados)

        
        '''
        if(luminosidade < "159"):
            GPIO.output(27, 1)
        if(luminosidade >= "150"):
            GPIO.output(27, 0)
            
        if(presenca == "1"):
            GPIO.output(23, 1)
        if(presenca == "0"):
            GPIO.output(23, 0)
        '''
            
        time.sleep(1)

def thread_atuacao(servicebus_client,TOPIC_NAME,SUBSCRIPTION_NAME):
    
    while 1:
        with servicebus_client:
            receiver = servicebus_client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5)
            with receiver:
                for msg in receiver:
                    print(msg)
                    receiver.complete_message(msg)

        time.sleep(1)

servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

t_1 = threading.Thread(target=thread_telemetria, args=(servicebus_client,TOPIC_NAME,))
t_2 = threading.Thread(target=thread_atuacao, args=(servicebus_client,TOPIC_NAME,SUBSCRIPTION_NAME,))

t_1.start()

t_2.start()

