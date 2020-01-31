#!/usr/bin/python
#
# Copyright (c) 2020 packom.net
#
# Sample python app using pyMeterBus to control M-Bus Master Hat
#
# pyMeterBus can be found here: https://github.com/ganehag/pyMeterBus
#
# More about the M-Bus Master hat: https://www.packom.net/m-bus-master-hat/
#

import os, time, serial, meterbus
import RPi.GPIO as GPIO

# Address of slave to read from - change this
slave_address = 1

# M-Bus Master Hat constants
mbus_master_product = 'M-Bus Master'
mbus_gpio_bcm = 26  # BCM pin number, not wiringPi or physical pin
serial_dev = '/dev/ttyAMA0'
baud_rate = 2400

# Check we have an M-Bus Master Hat installed
got_hat = False
if os.path.isfile('/proc/device-tree/hat/product'):
  namef = open('/proc/device-tree/hat/product')
  if namef.read().replace('\x00', '') == mbus_master_product:
    print('Found M-Bus Master Hat version ' + open('/proc/device-tree/hat/product_ver').read())
    got_hat = True

if got_hat == False:
  print('Warning: No M-Bus Master hat found')
  exit(1)

# Initialize GPIO handling
GPIO.setmode(GPIO.BCM)
GPIO.setup(mbus_gpio_bcm, GPIO.OUT)  # Strictly this is unnecessary, but belt and braces
GPIO.output(mbus_gpio_bcm, GPIO.LOW)

# Turn M-Bus on
GPIO.output(mbus_gpio_bcm, GPIO.HIGH)
time.sleep(.1)  # Pause briefly to allow the bus time to power up

# Read data from slave
ser = serial.Serial(serial_dev, baud_rate, 8, 'E', 1, 0.5)
try:
  meterbus.send_ping_frame(ser, slave_address)
  frame = meterbus.load(meterbus.recv_frame(ser, 1))
  assert isinstance(frame, meterbus.TelegramACK)
  meterbus.send_request_frame(ser, slave_address)
  frame = meterbus.load(meterbus.recv_frame(ser, meterbus.FRAME_DATA_LENGTH))
  assert isinstance(frame, meterbus.TelegramLong)
  print(frame.to_JSON())
except:
  print('Failed to read data from slave at address %d' % slave_address)

# Turn off M-Bus
GPIO.output(mbus_gpio_bcm, GPIO.HIGH)
GPIO.cleanup()
