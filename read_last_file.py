
import pymongo

def read_last_file(db_conn_string,database_name,container_name):#Returns most recent file added to the container
	client = pymongo.MongoClient(db_conn_string)
	db = client[database_name] 
	col = db[container_name]
	x = col.find().sort('_id',-1).limit(1)
	output=[]
	for data in x:
		output.append(data)
	return output[0]


db_conn_string='mongodb://bancodedadosteste:zpqRKVboAwSlLv0ktQULEGPdTGdRd4O6mqUEfNi8NFq9ggJIBqDzhNUPYBLb8BsXIeUXPGcAaOGI6Ja8GDq9wg==@bancodedadosteste.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@bancodedadosteste@'
database_name="bancodedadosiot"
container_name="iot_dados"


out=read_last_file(db_conn_string,database_name,container_name)
print(out)