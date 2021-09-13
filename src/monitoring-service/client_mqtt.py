#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import sys
 
client_name       = "shapes-smart-sensors"
topic_living_room = "zigbee2mqtt/smart-sensors/living-room"
topic_kitchen     = "zigbee2mqtt/smart-sensors/kitchen"
topic_bedroom     = "zigbee2mqtt/smart-sensors/bedroom"
topic_bathroom    = "zigbee2mqtt/smart-sensors/bathroom"    
topic             = "zigbee2mqtt/+/SENSOR"
broker            = "localhost"
port              = 1883
keepalive         = 60
time_day          = 10

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected to MQTT Broker {}:{} with return code {}!'.format(broker, port, rc))
        else:
            print('Failed to connect MQTT Broker, return code {}\n'.format(rc))
        
    client = mqtt.Client(client_name)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive)
    
    return client

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print('Received {} from {} topic!'.format(msg.payload.decode(), msg.topic))
        convert_message(client, msg)

    def convert_message(client, msg):
        sensor_data = json.loads(msg.payload.decode())

        if 'door' in msg.topic:
            if sensor_data["contact"]  == True:
                sensor_data["contact"] = 1
                print_message(msg, sensor_data)
                publish(client, sensor_data, msg)
            else:
                sensor_data["contact"] = 0
                print_message(msg, sensor_data)
                publish(client, sensor_data, msg)

        elif 'motion' in msg.topic:
            if sensor_data["occupancy"] == True:
                sensor_data["occupancy"] = 1
                print_message(msg, sensor_data)
                publish(client, sensor_data, msg)
            else:
                sensor_data["occupancy"] = 0
                print_message(msg, sensor_data)
                publish(client, sensor_data, msg)
        else:
            print_message(msg, sensor_data)
            publish(client, sensor_data, msg)

    def print_message(msg, sensor_data):
        if 'door' in msg.topic:
            print('Sensor data: {}'.format(sensor_data))
        elif 'motion' in msg.topic:
            print('Sensor data: {}'.format(sensor_data))

    client.subscribe(topic)
    client.on_message = on_message

def publish(client, sensor_data, msg):
    def on_publish(client, userdata, result):
        print('Sensor data published to {} topic!\n'.format(topic_publish))

    def check_room(msg):
        if 'living-room' in msg.topic:
            return topic_living_room
        elif 'kitchen' in msg.topic:
            return topic_kitchen
        elif 'bedroom' in msg.topic:
            return topic_bedroom
        elif 'bathroom' in msg.topic:
            return topic_bathroom

    data = json.dumps(sensor_data) 
    topic_publish = check_room(msg)
    client.publish(topic_publish, payload=data, qos=0, retain=False)
    client.on_publish = on_publish
    
def run():
    try:
        client = connect_mqtt()  
        subscribe(client)
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()

run()
