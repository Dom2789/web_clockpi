import paho.mqtt.publish as publish

def mqtt_publish(broker_IP, topic:str, payload:str, logger=None):
    try:
        publish.single(topic, payload, hostname=broker_IP)
        if logger is not None:
            logger.info(f"[broker: {broker_IP}][topic: {topic}][{payload}")
    except Exception as e:
        if logger is not None:
            logger.warning(f"[{e}][broker: {broker_IP}][topic: {topic}][{payload}")
        else:
            print(f"[{e}][broker: {broker_IP}][topic: {topic}][{payload}")
