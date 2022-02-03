#import RPi.GPIO as GPIO
import time
#import serial
from azure.servicebus import ServiceBusClient
from busCommunication import *
import Classes
import json
import threading
import datetime
import lamp

SUBSCRIPTION_NAME = "Gerenciador_de_atuadores"

#arduino = serial.Serial('/dev/ttyUSB0', 9600)

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(27,GPIO.OUT)
#GPIO.setup(23,GPIO.OUT)


def thread_telemetria(CONNECTION_STR,TOPIC_NAME_TELEMETRY):
    temperatura=1
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
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
        temperatura=temperatura+1
        umidade=15
        luminosidade=25
        presenca=1
        dispositivo = "Raspberry Pi + Arduino"
        
        dados = {
            "temperatura": temperatura,
            "umidade": umidade,
            "luminosidade": luminosidade,
            "presenca": presenca,
            "tempo": datetime.datetime.utcnow().timestamp()
        }
        send_message(servicebus_client,TOPIC_NAME_TELEMETRY,dados)
        

        
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
        time.sleep(5)
            

def thread_atualizar_ambiente(ambiente,CONNECTION_STR,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    telemetria=receive_message(servicebus_client,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME)
    if telemetria!=0:
        ambiente.atualizar_parametros(telemetria)
    while 1:
        telemetria=receive_message(servicebus_client,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME)
        if telemetria!=0:
            ambiente.atualizar_parametros(telemetria)
        print(ambiente.temperatura)
        time.sleep(1)

def thread_atualizar_controle(controle,CONNECTION_STR,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    comandos=receive_message(servicebus_client,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME)
    if comandos!=0:
        controle.atualizar_parametros(comandos)
    while 1:
        comandos=receive_message(servicebus_client,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME)
        if comandos!=0:
            controle.atualizar_parametros(comandos)
        time.sleep(5)




ambiente=Classes.Ambiente()
controle=Classes.Controle()
lampada=lamp.Lamp(0)

t_1 = threading.Thread(target=thread_telemetria, args=(CONNECTION_STR,TOPIC_NAME_TELEMETRY))
t_2 = threading.Thread(target=thread_atualizar_controle, args=(controle,CONNECTION_STR,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME))
t_3 = threading.Thread(target=thread_atualizar_ambiente, args=(ambiente,CONNECTION_STR,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME))
t_4 = threading.Thread(target=lamp.business_rule, args=(lampada,ambiente,controle))

t_1.start()

t_2.start()

t_3.start()



#t_4.start()