#!/usr/bin/python
#
# Copyright (c) 2025 packom.net
#
# Sample python app using pyMeterBus to control M-Bus Master Hat and paho-mqtt
# to publish data to an MQTT broker.
#
# pyMeterBus can be found here: https://github.com/ganehag/pyMeterBus
#
# More about the M-Bus Master hat: https://www.packom.net/m-bus-master-hat/
#
# To use this script:
# - install the required libraries:
#   ```bash
#   sudo pip install --break-system-packages paho-mqtt pyMeterBus RPi.GPIO
#   ```
# - change `slave_address` to the address of your M-Bus slave
# - change `mqtt_broker`` to your MQTT broker address
# - (optional) change `mqtt_port` if your broker uses a different port
# - (optional) change `mqtt_username` and `mqtt_password`` if your broker requires
#   authentication
# - change `mqtt_topic_base` to the base topic you want to use for publishing
# - change the `parse_meter_data()` and `publish_to_mqtt()` functions to provide the
#   desired data and format for your application
# - make sure you run the script as root "sudo python3 /path/to/this/script.py"
# - once it's behaving as you would like, add calling this script to sudo's crontab to run it periodically, for example:
#   ```bash
#   */5 * * * * /usr/bin/python3 /path/to/this/script.py
#   ```

import os, time, serial, meterbus, json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Address of slave to read from - change this
slave_address = 1

# M-Bus Master Hat constants
mbus_master_product = 'M-Bus Master'
mbus_gpio_bcm = 26  # BCM pin number, not wiringPi or physical pin
serial_dev = '/dev/ttyAMA0'
baud_rate = 2400

# MQTT configuration
mqtt_broker = "mosquitto"  # Change to your broker address
mqtt_port = 1883
mqtt_client_id = "mbus_meter_client"
mqtt_username = None       # Set if your broker requires authentication
mqtt_password = None       # Set if your broker requires authentication
mqtt_topic_base = "home/meter/"  # Base topic, we'll append meter ID

# Parse meter data from JSON
def parse_meter_data(json_data):
    data = json.loads(json_data)
    parsed_data = {}
    
    # Extract key information
    if "body" in data and "records" in data["body"]:
        # Get meter ID if available
        if "id_bcd" in data["body"]:
            parsed_data["meter_id"] = data["body"]["id_bcd"]
        
        # Get manufacturer if available
        if "manufacturer" in data["body"]:
            parsed_data["manufacturer"] = data["body"]["manufacturer"]
        
        # Process all records
        measurements = {}
        ii = 0
        for record in data["body"]["records"]:
            if "value" in record and "unit" in record:
                # Create key from value type or function
                key = record.get("function", "unknown")
                if "quantity" in record:
                    key = f"{record['quantity']}_{key}"
                
                # Store value and unit
                measurements[ii] = {
                    "type": record["type"],
                    "value": record["value"],
                    "unit": record["unit"]
                }
                
                # Add timestamp if available
                if "timestamp" in record:
                    measurements[key]["timestamp"] = record["timestamp"]

                ii += 1
        
        parsed_data["measurements"] = measurements
    
    return parsed_data

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {mqtt_broker}")
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message ID: {mid} published to MQTT broker")

def publish_to_mqtt(client, topic, payload):
    result = client.publish(topic, json.dumps(payload), qos=1, retain=True)
    result.wait_for_publish()
    return result.rc

# Check we have an M-Bus Master Hat installed
got_hat = False
if os.path.isfile('/proc/device-tree/hat/product'):
    namef = open('/proc/device-tree/hat/product')
    if namef.read().replace('\x00', '').startswith(mbus_master_product):
        print('Found M-Bus Master Hat version ' + open('/proc/device-tree/hat/product_ver').read())
        got_hat = True
if got_hat == False:
    print('Warning: No M-Bus Master hat found')
    exit(1)

# Initialize GPIO handling
GPIO.setmode(GPIO.BCM)
GPIO.setup(mbus_gpio_bcm, GPIO.OUT)  # Strictly this is unnecessary, but belt and braces
GPIO.output(mbus_gpio_bcm, GPIO.LOW)

# Setup MQTT client
client = mqtt.Client(client_id=mqtt_client_id)
client.on_connect = on_connect
client.on_publish = on_publish

if mqtt_username and mqtt_password:
    client.username_pw_set(mqtt_username, mqtt_password)

# Connect to MQTT broker
try:
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Turn M-Bus on
GPIO.output(mbus_gpio_bcm, GPIO.HIGH)
time.sleep(.1)  # Pause briefly to allow the bus time to power up

# Read data from slave
ser = serial.Serial(serial_dev, baud_rate, 8, 'E', 1, 0.55)
try:
    meterbus.send_ping_frame(ser, slave_address)
    frame = meterbus.load(meterbus.recv_frame(ser, 1))
    assert isinstance(frame, meterbus.TelegramACK)
    
    meterbus.send_request_frame(ser, slave_address)
    frame = meterbus.load(meterbus.recv_frame(ser, meterbus.FRAME_DATA_LENGTH))
    assert isinstance(frame, meterbus.TelegramLong)
    
    # Get raw JSON data
    json_data = frame.to_JSON()
    print("Raw meter data:")
    print(json_data)
    
    # Parse the data
    parsed_data = parse_meter_data(json_data)
    print("\nParsed meter data:")
    print(json.dumps(parsed_data, indent=2))
    
    # Determine MQTT topic
    # Use meter ID if available, otherwise use slave address
    if "meter_id" in parsed_data:
        topic = f"{mqtt_topic_base}{parsed_data['meter_id']}"
    else:
        topic = f"{mqtt_topic_base}slave_{slave_address}"
    
    # Publish to MQTT
    print(f"\nPublishing to MQTT topic: {topic}")
    publish_result = publish_to_mqtt(client, topic, parsed_data)
    
    if publish_result == 0:
        print("Data successfully published to MQTT")
    else:
        print(f"Failed to publish to MQTT, return code: {publish_result}")
    
except Exception as e:
    print(f'Failed to read or publish data from slave at address {slave_address}: {str(e)}')

# Turn off M-Bus
GPIO.output(mbus_gpio_bcm, GPIO.LOW)
GPIO.cleanup()

# Disconnect MQTT client
client.loop_stop()
client.disconnect()