import datetime
import time

class Lamp():#Classe lâmpada
	
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

def business_rule(lamp,ambiente,controle):#Regra de negócios para a lâmpada, será uma thread
	k_luminosity=calibration_routine(lamp,ambiente)
	while 1:
		if(controle.luminosidade==0 or controle.presenca==0):#Caso particular luz off
			lamp.set_luminosity(0)
		else:
			delta=controle.luminosidade-ambiente.luminosidade
			if (delta>2 or delta<-2):#Fora da margem aceitável de erro
				lamp.set_luminosity(lamp.luminosity_set+delta/k_luminosity)
		old_telemetry_time=ambiente.tempo_atualizacao
		while old_telemetry_time>=ambiente.tempo_atualizacao:
			time.sleep(1)
			
def calibration_routine(lamp,ambiente):#Rotina de calibração da lâmpada, executada no início de business_rule
	
	lamp.set_luminosity(0)
	time=datetime.datetime.utcnow()
	while ambiente.tempo_atualizacao<=time:
		time.sleep(0.1)
	light_level_turn_off=ambiente.luminosidade
	
	lamp.set_luminosity(lamp.max_luminosity)
	time=datetime.datetime.utcnow()
	while ambiente.tempo_atualizacao<time:
		time.sleep(0.1)
	light_level_turn_on=ambiente.luminosidade

	k_luminosity=(light_level_turn_on-light_level_turn_off)/lamp.max_luminosity

	return k_luminosity
