import RPi.GPIO as GPIO
import time
import serial
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import json
import asyncio

IOTHUB_DEVICE_CONNECTION_STRING = 'HostName=ServidorIoT.azure-devices.net;DeviceId=DispositivoTeste;SharedAccessKey=vI0U2HxL1HV/60SVzXoskPCAhNZpmmN28r1ilGaiKfs='

arduino = serial.Serial('/dev/ttyUSB0', 9600)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

async def send_telemetry(conn_str, attribute_value, attribute_name, component_name):
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    
    await device_client.connect()
    
    telemetry_message = attribute_value
    msg = Message(json.dumps(telemetry_message))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    msg.custom_properties["$.sub"] = component_name
    await device_client.send_message(msg)
    
    await device_client.shutdown()

while(True):
    temperatura = arduino.readline()
    temperatura = temperatura.decode("utf-8")
    temperatura = float(temperatura)
    print(temperatura)
    umidade = arduino.readline()
    umidade = umidade.decode("utf-8")
    umidade = float(umidade)
    print(umidade)
    luminosidade = arduino.readline()
    luminosidade = luminosidade.decode("utf-8")
    luminosidade = int(luminosidade)
    print(luminosidade)
    presenca = arduino.readline()
    presenca = presenca.decode("utf-8")
    presenca = int(presenca)
    print(presenca)
    dispositivo = "Raspberry Pi + Arduino"
    
    dados = {
        "temperatura": temperatura,
        "umidade": umidade,
        "luminosidade": luminosidade,
        "presenca": presenca
    }
    
    asyncio.run(send_telemetry(IOTHUB_DEVICE_CONNECTION_STRING, dados, "SmartRoom", "Sensores"))
    
    '''
    if(luminosidade < "159"):
        GPIO.output(27, 1)
    if(luminosidade >= "150"):
        GPIO.output(27, 0)
        
    if(presenca == "1"):
        GPIO.output(23, 1)
    if(presenca == "0"):
        GPIO.output(23, 0)
    '''
        
    time.sleep(1)