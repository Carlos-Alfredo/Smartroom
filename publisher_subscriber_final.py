import time
import serial
from azure.servicebus import ServiceBusClient
from busCommunication import *
import Classes
import json
import threading
import datetime
import lamp

SUBSCRIPTION_NAME = "Gerenciador_de_atuadores"

comunicacao = serial.Serial('/dev/ttyUSB0', 9600)

#comunicacao.open()


def thread_telemetria(CONNECTION_STR,TOPIC_NAME_TELEMETRY):
    temperatura=1
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True, retry_total=15, retry_backoff_factor=1, retry_backoff_max=30)
    while 1:
        temperatura = comunicacao.readline()
        temperatura = temperatura.decode("utf-8")
        temperatura = float(temperatura)
        #print(temperatura)
        umidade = comunicacao.readline()
        umidade = umidade.decode("utf-8")
        umidade = float(umidade)
        #print(umidade)
        luminosidade = comunicacao.readline()
        luminosidade = luminosidade.decode("utf-8")
        luminosidade = int(luminosidade)
        #print(luminosidade)
        presenca = comunicacao.readline()
        presenca = presenca.decode("utf-8")
        presenca = int(presenca)
        print(presenca)
        #temperatura=temperatura+1
        #umidade=17
        #luminosidade=22
        #presenca=1
        dispositivo = "Raspberry Pi + Arduino"
        
        dados = {
            "temperatura": temperatura,
            "umidade": umidade,
            "luminosidade": luminosidade,
            "presenca": presenca,
            "tempo": datetime.datetime.utcnow().timestamp()
        }
        send_message(servicebus_client,TOPIC_NAME_TELEMETRY,dados)
        
        time.sleep(1)
            

def thread_atualizar_ambiente(ambiente,CONNECTION_STR,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True, retry_total=10, retry_backoff_factor=1, retry_backoff_max=30)
    telemetria=receive_message(servicebus_client,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME)
    if telemetria!=0:
        ambiente.atualizar_parametros(telemetria)
    while 1:
        telemetria=receive_message(servicebus_client,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME)
        if telemetria!=0:
            ambiente.atualizar_parametros(telemetria)
        #print(ambiente.temperatura)
        #print(ambiente.umidade)
        #print(ambiente.luminosidade)
        print(ambiente.presenca)
        time.sleep(1)

def thread_atualizar_controle(controle,CONNECTION_STR,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True, retry_total=10, retry_backoff_factor=1, retry_backoff_max=30)
    comandos=receive_message(servicebus_client,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME)
    if comandos!=0:
        controle.atualizar_parametros(comandos)
    while 1:
        comandos=receive_message(servicebus_client,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME)
        if comandos!=0:
            controle.atualizar_parametros(comandos)
        #print(controle.tempo_atualizacao)
        #print(controle.temperatura)
        #print(controle.umidade)
        print(controle.luminosidade)
        #print(controle.presenca)
        #string=str(controle.luminosidade)+','+str(controle.temperatura)+'/'
        #comunicacao.write(string)
        #comunicacao.write(',')
        #comunicacao.write(controle.temperatura)
        #comunicacao.write('/')
        time.sleep(5)




ambiente=Classes.Ambiente()
controle=Classes.Controle()
lampada=lamp.Lamp(0, 12)
lampada.set_luminosity(100)

t_1 = threading.Thread(target=thread_telemetria, args=(CONNECTION_STR,TOPIC_NAME_TELEMETRY))
t_2 = threading.Thread(target=thread_atualizar_controle, args=(controle,CONNECTION_STR,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME))
t_3 = threading.Thread(target=thread_atualizar_ambiente, args=(ambiente,CONNECTION_STR,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME))
t_4 = threading.Thread(target=lamp.business_rule, args=(lampada,ambiente,controle))

t_1.start()

t_2.start()

t_3.start()

t_4.start()

#comunicacao.close()