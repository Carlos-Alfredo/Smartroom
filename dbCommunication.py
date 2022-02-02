
import pymongo
import datetime
import asyncio

db_conn_string='mongodb://bancodedadosteste:zpqRKVboAwSlLv0ktQULEGPdTGdRd4O6mqUEfNi8NFq9ggJIBqDzhNUPYBLb8BsXIeUXPGcAaOGI6Ja8GDq9wg==@bancodedadosteste.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@bancodedadosteste@'
database_name="bancodedadosiot"
container_telemetry_name="telemetry"
container_target_name="set_target"


def send_to_db(db_conn_string,database_name,container_name,dictionary):
	client = pymongo.MongoClient(db_conn_string)
	db = client[database_name] 
	col = db[container_name]
	x = col.insert_one(dictionary)
	return 1

def send_telemetry(db_conn_string,database_name,container_telemetry_name,attribute_value):
	client = pymongo.MongoClient(db_conn_string)
	telemetry_message={
		"Operacao":"telemetria",
		"temperatura":attribute_value[0],
		"umidade":attribute_value[1],
		"luminosidade":attribute_value[2],
		"presenca":attribute_value[3],
		"EnqueuedTimeUtc":datetime.datetime.utcnow()
	}
	send_to_db(db_conn_string,database_name,container_telemetry_name,telemetry_message)

def send_target(db_conn_string,database_name,container_target_name,attribute_value):
	client = pymongo.MongoClient(db_conn_string)
	telemetry_message={
		"Operacao":"objetivo",
		"temperatura":attribute_value[0],
		"umidade":attribute_value[1],
		"luminosidade":attribute_value[2],
		"presenca":attribute_value[3],
		"EnqueuedTimeUtc":datetime.datetime.utcnow()
	}
	send_to_db(db_conn_string,database_name,container_target_name,telemetry_message)

def read_last_file(db_conn_string,database_name,container_name):#Retorna o mais recente arquivo adicionado ao banco de dados
	client = pymongo.MongoClient(db_conn_string)
	db = client[database_name] 
	col = db[container_name]
	x = col.find().sort('_id',-1).limit(1)
	output=[]
	for data in x:
		output.append(data)
	return output[0]

def read_telemetry(db_conn_string,database_name,container_telemetry_name):
	dictionary=read_last_file(db_conn_string,database_name,container_telemetry_name)
	return [dictionary['temperatura'],dictionary['umidade'],dictionary['luminosidade'],dictionary['presenca'],dictionary['EnqueuedTimeUtc']]#Formato de retorno[telemetrias,tempo da telemetria]

def read_target(db_conn_string,database_name,container_target_name):
	dictionary=read_last_file(db_conn_string,database_name,container_target_name)
	return [dictionary['temperatura'],dictionary['umidade'],dictionary['luminosidade'],dictionary['presenca'],dictionary['EnqueuedTimeUtc']]#Formato de retorno[telemetrias,tempo da telemetria]

#attribute_value=[29,88,205,1]

#send_telemetry(db_conn_string,database_name,container_telemetry_name,attribute_value)

#print(read_telemetry(db_conn_string,database_name,container_telemetry_name))