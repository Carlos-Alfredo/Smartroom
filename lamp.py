import datetime
import time
import RPi.GPIO as gpio

class Lamp():#Classe lâmpada
	
	def __init__(self,luminosity_set, pin):
		self.luminosity_set=int(luminosity_set)
		self.max_luminosity=255
		self.set_luminosity(luminosity_set)
		
		gpio.setwarnings(False)
		gpio.setmode(gpio.BOARD)
		gpio.setup(pin,gpio.OUT)
		self.pwmLed = gpio.PWM(pin,self.max_luminosity)
		self.pwmLed.start(0)
		
	
	def set_luminosity(self,luminosity_set):#Método para mudar a intensidade do led
		if luminosity_set>self.max_luminosity:
			return self.set_luminosity(self.max_luminosity)
		elif self.luminosity_set==luminosity_set:
			return 1
		self.luminosity_set=luminosity_set
		self.pwmLed.ChangeDutyCycle(luminosity_set)
		return 1
		#
		#

########################################################################################################

def business_rule(lamp,ambiente,controle):#Regra de negócios para a lâmpada, será uma thread
	k_luminosity=calibration_routine(lamp,ambiente)
	print("Constante de luminosidade: ",k_luminosity)
	while 1:
		ambiente_presenca=ambiente.presenca
		ambiente_luminosidade=ambiente.luminosidade
		controle_luminosidade=controle.luminosidade
		lamp_luminosity_set=lamp.luminosity_set
		ambiente_tempo_atualizacao=ambiente.tempo_atualizacao
		if(controle_luminosidade==0 or ambiente_presenca==0):#Caso particular luz off
			lamp.set_luminosity(0)
		else:
			delta=controle_luminosidade-ambiente_luminosidade
			if (delta>2 or delta<-2):#Fora da margem aceitável de erro
				lamp.set_luminosity(lamp_luminosity_set+delta/k_luminosity)
				print(lamp_luminosity_set+delta/k_luminosity)
		old_telemetry_time=ambiente_tempo_atualizacao
		while old_telemetry_time>=ambiente.tempo_atualizacao:
			time.sleep(0.1)
			
def calibration_routine(lamp,ambiente):#Rotina de calibração da lâmpada, executada no início de business_rule
	
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
