#!/bin/bash

git clone https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library.git
cd Adafruit-Motor-HAT-Python-Library
sudo python setup.py install
sudo rm -rf Adafruit-Motor-HAT-Python-Library
