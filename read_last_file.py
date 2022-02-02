
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