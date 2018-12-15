#!/usr/bin/env bash
sudo PYTHONPATH=".:/home/pi/rpi_ws281x/python/build/lib.linux-armv7l-2.7:${PYTHONPATH}" AWS_CONFIG_FILE=/home/pi/.aws/config SQS= SQS_URL=$SQS_URL python /home/pi/rpi_ws281x/python/custom/app.py
