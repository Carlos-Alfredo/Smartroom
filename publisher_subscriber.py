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
            

def business_rule(lamp,ambiente,controle):#Regra de negócios para a lâmpada, será uma thread
    k_luminosity=calibration_routine(lamp,ambiente)
    print("Constante de luminosidade: ",k_luminosity)
    if(controle.luminosidade==0 or ambiente.presenca==0):#Caso particular luz off
        lamp.set_luminosity(0)
    else:
        delta=controle.luminosidade-ambiente.luminosidade
        if (delta>2 or delta<-2):#Fora da margem aceitável de erro
            lamp.set_luminosity(lamp.luminosity_set+delta/k_luminosity)
            print(lamp.luminosity_set+delta/k_luminosity)
            
def calibration_routine(lamp,ambiente,k_luminosity):#Rotina de calibração da lâmpada, executada no início de business_rule
    
    lamp.set_luminosity(0)
    tempo=datetime.datetime.utcnow().timestamp()
    while ambiente.tempo_atualizacao<=tempo:
        time.sleep(0.1)
    light_level_turn_off=ambiente.luminosidade
    
    lamp.set_luminosity(lamp.max_luminosity)
    tempo=datetime.datetime.utcnow().timestamp()
    while ambiente.tempo_atualizacao<=tempo:
        time.sleep(0.1)
    light_level_turn_on=ambiente.luminosidade
    if light_level_turn_on-light_level_turn_off==0:
        k_luminosity=1/lamp.max_luminosity
    else:
        k_luminosity=(light_level_turn_on-light_level_turn_off)/lamp.max_luminosity

    return k_luminosity

def atualizar_ambiente(ambiente,servicebus_client,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME):
    telemetria=receive_message(servicebus_client,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME)
    if telemetria!=0:
        ambiente.atualizar_parametros(telemetria)

def atualizar_controle(controle,servicebus_client,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME):
    comandos=receive_message(servicebus_client,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME)
    if comandos!=0:
        controle.atualizar_parametros(comandos)

def thread_atuacao(lampada,controle,ambiente,CONNECTION_STR,TOPIC_NAME_CONTROL,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME):
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    k_luminosity=calibration_routine(lampada,ambiente)
    while 1:
        atualizar_ambiente(ambiente,servicebus_client,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME)
        atualizar_controle(controle,servicebus_client,TOPIC_NAME_CONTROL,SUBSCRIPTION_NAME)
        business_rule(lampada,ambiente,controle,k_luminosity)


ambiente=Classes.Ambiente()
controle=Classes.Controle()
lampada=lamp.Lamp(0)

t_1 = threading.Thread(target=thread_telemetria, args=(CONNECTION_STR,TOPIC_NAME_TELEMETRY))
t_2 = threading.Thread(target=thread_atuacao, args=(lampada,controle,ambiente,CONNECTION_STR,TOPIC_NAME_CONTROL,TOPIC_NAME_TELEMETRY,SUBSCRIPTION_NAME))

t_1.start()

t_2.start()
