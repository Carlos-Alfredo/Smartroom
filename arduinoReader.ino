#include "DHT.h"

unsigned long delayEnvio;
#define pinPIR 2
#define pinLDR A0
#define pinDHT 9

#define pinLED 7
#define pinLED2 4

int luminosidade = 0;
float temperatura; // variável para armazenar o valor de temperatura
float umidade; // variável para armazenar o valor de umidade
DHT dht(pinDHT, DHT11); // define o pino e o tipo de DHT

void setup() {
  Serial.begin(9600); // 9600bps

  dht.begin(); // inicializa o sensor DHT
  pinMode(pinPIR, INPUT);
  pinMode(pinLDR, INPUT); 
  pinMode(pinLED, OUTPUT);
  pinMode(pinLED2, OUTPUT);
}

void loop() {
  delay(1000); // 2 segundos (Datasheet)
  
  luminosidade = analogRead(pinLDR);
  bool valorPIR = digitalRead(pinPIR);
  temperatura = dht.readTemperature(); // lê a temperatura em Celsius
  umidade = dht.readHumidity(); // lê a umidade

  if((millis() - delayEnvio) > 50) {
    Serial.println(temperatura);
    Serial.println(umidade);
    Serial.println(luminosidade);
    Serial.println(valorPIR);
  }
}
