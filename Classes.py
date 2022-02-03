class Ambiente():
	
	def __init__(self):
		self.temperatura=0
		self.umidade=0
		self.luminosidade=0
		self.presenca=0
		self.tempo_atualizacao=0

	def atualizar_parametros(self,dicionario):
		if(self.tempo_atualizacao<dicionario["tempo"]):
			self.temperatura=dicionario["temperatura"]
			self.umidade=dicionario["umidade"]
			self.luminosidade=dicionario["luminosidade"]
			self.presenca=dicionario["presenca"]
			self.tempo_atualizacao<dicionario["tempo"]
			return 1
		return 0

class Controle():

	def __init__(self):
		self.temperatura=0
		self.umidade=0
		self.luminosidade=0
		self.presenca=0
		self.tempo_atualizacao=0
	
	def atualizar_parametros(self,dicionario):
		if(self.tempo_atualizacao<dicionario["tempo"]):
			self.temperatura=dicionario["temperatura"]
			self.umidade=dicionario["umidade"]
			self.luminosidade=dicionario["luminosidade"]
			self.presenca=dicionario["presenca"]
			self.tempo_atualizacao<dicionario["tempo"]
			return 1
		return 0
