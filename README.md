Introduction
============

A simple python app which uses the [M-Bus Master Hat](https://www.packom.net/m-bus-master-hat/) and [pyMeterBus](https://github.com/ganehag/pyMeterBus) to read data from an M-Bus slave.

Setup
=====

```
sudo apt install python-pip
git clone https://github.com/ganehag/pyMeterBus
cd pyMeterBus & sudo python setup.py install & cd ..
sudo python setup.py install
```

Also, if this is the first time using the M-Bus Master Hat, follow the installation instructions [here](https://www.packom.net/m-bus-master-hat-instructions/).

Running
=======

Edit py_mbus_hat.py and change the slave_address to the appropriate value.  Then:

```
python py_mbus_hat.py
```

Operation
=========

* Checks for an M-Bus Master Hat.  If this fails then it is likely you don't have an M-Bus Master Hat installed, or you haven't rebooted the Pi since installing it (remove and then reapply power).

* Turns on the M-Bus.  The M-Bus power led on the Hat should illuminate.

* Reads data from the slave configured above.

* Outputs the data read.

* Turns off the M-Bus, cleans up and exits.

