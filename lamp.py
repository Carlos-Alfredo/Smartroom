import dbCommunication as db
import datetime

class Lamp:#Classe lâmpada
	
	def __init__(self,luminosity_set):
		self.luminosity_set=luminosity_set
		self.max_luminosity=100
		self.set_luminosity(luminosity_set)
		
		
	
	def set_luminosity(self,luminosity_set):#Método para mudar a intensidade do led
		if luminosity_set>self.max_luminosity:
			return self.set_luminosity(self.max_luminosity)
		elif self.luminosity_set==luminosity_set:
			return 1
		self.luminosity_set=luminosity_set
		#
		#
		#
		#

########################################################################################################

def business_rule(lamp):#Regra de negócios para a lâmpada, será uma thread
	k_luminosity=calibration_routine(lamp)
	telemetry=db.read_telemetry(db.db_conn_string,db.database_name,db.container_telemetry_name)
	target=db.read_target(db.db_conn_string,db.database_name,db.container_target_name)
	while 1:
		if(target[2]==0 or target[3]==0):#Caso particular luz off
			lamp.set_luminosity(0)
		else:
			delta=target[2]-telemetry[2]
			if (delta>2 or delta<-2):#Fora da margem aceitável de erro
				lamp.set_luminosity(lamp.luminosity_set+delta/k_luminosity)
		old_telemetry_time=telemetry[4]
		telemetry=db.read_telemetry(db.db_conn_string,db.database_name,db.container_telemetry_name)
		target=db.read_target(db.db_conn_string,db.database_name,db.container_target_name)
		while old_telemetry_time>=telemetry[4]:
			telemetry=db.read_telemetry(db.db_conn_string,db.database_name,db.container_telemetry_name)
			target=db.read_target(db.db_conn_string,db.database_name,db.container_target_name)
			
def calibration_routine(lamp):#Rotina de calibração da lâmpada, executada no início de business_rule
	
	lamp.set_luminosity(0)
	time=datetime.datetime.utcnow()
	telemetry=db.read_telemetry(db.db_conn_string,db.database_name,db.container_telemetry_name)
	while telemetry[4]<time:
		telemetry=db.read_telemetry(db.db_conn_string,db.database_name,db.container_telemetry_name)
	light_level_turn_off=telemetry[2]
	
	lamp.set_luminosity(lamp.max_luminosity)
	time=datetime.datetime.utcnow()
	telemetry=db.read_telemetry(db.db_conn_string,db.database_name,db.container_telemetry_name)
	while telemetry[4]<time:
		telemetry=db.read_telemetry(db.db_conn_string,db.database_name,db.container_telemetry_name)
	light_level_turn_on=telemetry[2]

	k_luminosity=(light_level_turn_on-light_level_turn_off)/lamp.max_luminosity

	return k_luminosity
