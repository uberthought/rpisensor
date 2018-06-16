#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y \
	build-essential \
	python3-dev \
	python3 \
	python3-pip

pip3 install \
	numpy

cd ~
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python3 setup.py install
