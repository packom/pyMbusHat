# pyMbusHat

## Introduction

Simple python scripts which uses the [M-Bus Master Hat](https://www.packom.net/m-bus-master-hat/) and [pyMeterBus](https://github.com/ganehag/pyMeterBus) to read data from an M-Bus slave.

* [`py_mbus_hat.py`](py_mbus_hat.py) - Retrieves data from a slave and prints it out
* [`hat_mqtt.py`](hat_mqtt.py) - Retrieves data from a slave and sends it to an MQTT broker

## Setup

```
sudo apt install python-pip
sudo pip install --break-system-packages -r requirements.txt
```

Also, if this is the first time using the M-Bus Master Hat, follow the installation instructions [here](https://www.packom.net/m-bus-master-hat-instructions/).

## Running

Edit [`py_mbus_hat.py`](py_mbus_hat.py) and change the slave_address to the appropriate value.  Then:

```
sudo python3 py_mbus_hat.py
```

See the comment at the beginning of [`hat_mqtt.py`](hat_mqtt.py) for details on what to change in that script.

## Operation

* Checks for an M-Bus Master Hat.  If this fails then it is likely you don't have an M-Bus Master Hat installed, or you haven't rebooted the Pi since installing it (remove and then reapply power).

* Turns on the M-Bus.  The M-Bus power led on the Hat should illuminate.

* Reads data from the slave configured above.

* If [`hat_mqtt.py`](hat_mqtt.py), parse the data and send it to the MQTT broker.

* Prints the data read.

* Turns off the M-Bus, cleans up and exits.

## Errors

You will likely need to run both scripts as root (use `sudo`).

If you have been using the serial port using other software you may get a warning that the serial channel is already in use.  You can suppress the warning by adding:

```
GPIO.setwarnings(False) 
```

You may find that the bus needs to be left powered longer than 0.1s (the default in the script) to allow successful reads of the bus.  This is likely to be more prevalent in bus powered meters, as they need some time to power on and stabilise after the bus is powered.

## Sample Output

Here is sample output from [`hat_mqtt.py`](hat_mqtt.py):

```
Found M-Bus Master Hat version 0x0006
Connected to MQTT broker at mosquitto
Raw meter data:
{
    "body": {
        "header": {
            "access_no": 85,
            "identification": "0x99, 0x99, 0x99, 0x99",
            "manufacturer": "___",
            "medium": "0x2",
            "sign": "0x0, 0x0",
            "status": "0x0",
            "type": "0x72",
            "version": "0x1"
        },
        "records": [
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnit.ENERGY_WH",
                "unit": "MeasureUnit.WH",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            },
            {
                "function": "FunctionType.INSTANTANEOUS_VALUE",
                "storage_number": 0,
                "type": "VIFUnitExt.DIMENSIONLESS",
                "unit": "MeasureUnit.NONE",
                "value": 0
            }
        ]
    },
    "head": {
        "a": "0x1",
        "c": "0x8",
        "crc": "0x27",
        "length": "0x5d",
        "start": "0x68",
        "stop": "0x16"
    }
}

Parsed meter data:
{
  "measurements": {
    "0": {
      "type": "VIFUnit.ENERGY_WH",
      "value": 0,
      "unit": "MeasureUnit.WH"
    },
    "1": {
      "type": "VIFUnit.ENERGY_WH",
      "value": 0,
      "unit": "MeasureUnit.WH"
    },
    "2": {
      "type": "VIFUnit.ENERGY_WH",
      "value": 0,
      "unit": "MeasureUnit.WH"
    },
    "3": {
      "type": "VIFUnit.ENERGY_WH",
      "value": 0,
      "unit": "MeasureUnit.WH"
    },
    "4": {
      "type": "VIFUnit.ENERGY_WH",
      "value": 0,
      "unit": "MeasureUnit.WH"
    },
    "5": {
      "type": "VIFUnit.ENERGY_WH",
      "value": 0,
      "unit": "MeasureUnit.WH"
    },
    "6": {
      "type": "VIFUnitExt.DIMENSIONLESS",
      "value": 0,
      "unit": "MeasureUnit.NONE"
    },
    "7": {
      "type": "VIFUnitExt.DIMENSIONLESS",
      "value": 0,
      "unit": "MeasureUnit.NONE"
    },
    "8": {
      "type": "VIFUnitExt.DIMENSIONLESS",
      "value": 0,
      "unit": "MeasureUnit.NONE"
    },
    "9": {
      "type": "VIFUnitExt.DIMENSIONLESS",
      "value": 0,
      "unit": "MeasureUnit.NONE"
    },
    "10": {
      "type": "VIFUnitExt.DIMENSIONLESS",
      "value": 0,
      "unit": "MeasureUnit.NONE"
    },
    "11": {
      "type": "VIFUnitExt.DIMENSIONLESS",
      "value": 0,
      "unit": "MeasureUnit.NONE"
    }
  }
}

Publishing to MQTT topic: home/meter/slave_1
Message ID: 1 published to MQTT broker
Data successfully published to MQTT
```