
import pymongo
import datetime
import asyncio


def send_to_db(db_conn_string,database_name,container_name,dictionary):
	client = pymongo.MongoClient(db_conn_string)
	db = client[database_name] 
	col = db[container_name]
	x = col.insert_one(dictionary)
	return 1

def send_telemetry(db_conn_string,database_name,container_name,attribute_value,attribute_name):
	client = pymongo.MongoClient(db_conn_string)
	telemetry_message={}
	for i in range (0,len(attribute_value)):
		telemetry_message[attribute_name[i]]=attribute_value[i]
	#dt = datetime.datetime.now(timezone.utc)
	#utc_time = dt.replace(tzinfo=timezone.utc)
	#utc_timestamp = utc_time.timestamp()
	telemetry_message["EnqueuedTimeUtc"]=datetime.datetime.utcnow()
	send_to_db(db_conn_string,database_name,container_name,telemetry_message)

db_conn_string='mongodb://bancodedadosteste:zpqRKVboAwSlLv0ktQULEGPdTGdRd4O6mqUEfNi8NFq9ggJIBqDzhNUPYBLb8BsXIeUXPGcAaOGI6Ja8GDq9wg==@bancodedadosteste.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@bancodedadosteste@'
database_name="bancodedadosiot"
container_name="iot_dados"
attribute_value=[29,88,205,1]
attribute_name=['temperatura','umidade','luminosidade','presenca']

send_telemetry(db_conn_string,database_name,container_name,attribute_value,attribute_name)