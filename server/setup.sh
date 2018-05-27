#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y \
	python3 \
	python3-pip

pip3 install \
	numpy

pip3 install \
	dash \
	dash_renderer \
	dash_core_components \
	dash_html_components
