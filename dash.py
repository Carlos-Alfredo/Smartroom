import streamlit as st
import pandas as pd
import ast
from azure.servicebus import ServiceBusClient
from busCommunication import *
from datetime import datetime, timedelta
import threading
pd.set_option('plotting.backend', 'pandas_bokeh')

CONNECTION_STR = "Endpoint=sb://testeiotbroker.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Tig31UtDJ9LY+epBCrzehYnPtM3KvbLjxMU9SycGcKY="
TOPIC_NAME_TELEMETRIA = "telemetria"
TOPIC_NAME_CONTROLE = "comandos_usuarios"
SUBSCRIPTION_NAME = "Interface_do_usuario"
def app():
	out = 0
	servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
	while out==0:
		out=receive_message(servicebus_client,TOPIC_NAME_TELEMETRIA,SUBSCRIPTION_NAME)
	st.markdown("<center><h1>Smartroom 📟</h1><center>", unsafe_allow_html=True)
	st.markdown('<center><h4>Apresentação do trabalho da cadeira INTERNET DAS COISAS</h4><center>', unsafe_allow_html=True)
	st.markdown('---')
	st.markdown('<center><h4>Monitoramento - Sensores 📊</h4><center>', unsafe_allow_html=True)
	#st.markdown(f'<center><h5>Ultima Atualização: {data}</h5><center><br>', unsafe_allow_html=True)
	left_column, right_column = st.columns(2)
	# You can use a column just like st.sidebar:
	#COLOCAR AS UNIDADES DE MEDIDAS
	with left_column:
		st.markdown("<center><h5>Luminosidade</h5><center>", unsafe_allow_html=True)
		st.markdown(f"<center><h5>{out['luminosidade']}</h5><center>", unsafe_allow_html=True)
		st.markdown("<center><h5>Presença</h5><center>", unsafe_allow_html=True)
		st.markdown(f"<center><h5>{out['presenca']}</h5><center>", unsafe_allow_html=True)
	# Or even better, call Streamlit functions inside a "with" block:
	with right_column:
		st.markdown("<center><h5>Temperatura</h5><center>", unsafe_allow_html=True)
		st.markdown(f"<center><h5>{out['temperatura']}</h5><center>", unsafe_allow_html=True)
		st.markdown("<center><h5>Umidade</h5><center>", unsafe_allow_html=True)
		st.markdown(f"<center><h5>{out['umidade']}</h5><center>", unsafe_allow_html=True)
	st.sidebar.title('Atuadores')
	led = st.sidebar.slider('Nivel de Luminosidade: ', 0, 100, 0)
	temperatura = st.sidebar.slider('Temperatura: ', 0, 100, 0)
	message = {
            "temperatura": temperatura,
            "umidade": 0,
            "luminosidade": led,
            "presenca": 0,
            "tempo": datetime.datetime.utcnow().timestamp()
        }
	send_message(servicebus_client,TOPIC_NAME_CONTROLE,message)
	print(message)
	

app()
