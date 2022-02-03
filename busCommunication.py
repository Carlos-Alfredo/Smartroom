from azure.servicebus import ServiceBusClient, ServiceBusMessage
import ast
import json

CONNECTION_STR = "Endpoint=sb://testeiotbroker.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Tig31UtDJ9LY+epBCrzehYnPtM3KvbLjxMU9SycGcKY="
TOPIC_NAME_TELEMETRY = "telemetria"
TOPIC_NAME_CONTROL = "comandos_usuarios"



def send_message(servicebus_client,TOPIC_NAME,message):
    with servicebus_client:
        sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
        msg = ServiceBusMessage(json.dumps(message))
    # send the message to the topic
        with sender:
            sender.send_messages(msg)

def receive_message(servicebus_client,TOPIC_NAME,SUBSCRIPTION_NAME):
    message=0
    with servicebus_client as client:
        receiver = servicebus_client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5)
        with receiver:
            for msg in receiver:
                message=ast.literal_eval(str(msg))
    return message