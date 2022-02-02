import streamlit as st
import pandas as pd
from read_last_file import *
from dbCommunication import *
from datetime import datetime, timedelta
pd.set_option('plotting.backend', 'pandas_bokeh')

db_conn_string='mongodb://bancodedadosteste:zpqRKVboAwSlLv0ktQULEGPdTGdRd4O6mqUEfNi8NFq9ggJIBqDzhNUPYBLb8BsXIeUXPGcAaOGI6Ja8GDq9wg==@bancodedadosteste.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@bancodedadosteste@'
database_name="bancodedadosiot"

container_telemetry_name="telemetry"
container_target_name="set_target"

def app():
	out = read_last_file(db_conn_string,database_name,container_telemetry_name)
	data = out['EnqueuedTimeUtc'] - timedelta(hours=3)
	print(data)
	data = data.strftime("%m/%d/%Y, %H:%M:%S")
	st.markdown("<center><h1>Smartroom 📟</h1><center>", unsafe_allow_html=True)
	st.markdown('<center><h4>Apresentação do trabalho da cadeira INTERNET DAS COISAS</h4><center>', unsafe_allow_html=True)
	out=read_last_file(db_conn_string,database_name,container_telemetry_name)
	st.markdown('---')
	st.markdown('<center><h4>Monitoramento - Sensores 📊</h4><center>', unsafe_allow_html=True)
	st.markdown(f'<center><h5>Ultima Atualização: {data}</h5><center><br>', unsafe_allow_html=True)
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
	umidade = 0
	presenca = 0
	attribute_value = [temperatura, umidade, led, presenca]
	send_target(db_conn_string,database_name,container_target_name,attribute_value)
app()