# Copyright (c) 2012 Matthew Kirk
# Licenced under MIT Licence.
# See http://www.cl.cam.ac.uk/freshers/raspberrypi/tutorials/temperature/LICENCE

# Modified by Jakob Papirov
# Course: "Environmental measuring techniques"
# Date: December 2013

import RPi.GPIO as GPIO
import time
import os

# RDY = ready
# WRK = working
# !! DS18B20 has to be pin #4 (on BCM) for the time being;  not used in program !!
	# For some reason the DS18B20 is hardcoded as being pin #4 in the RPi.GPIO code
LED_RDY_GPIO_PIN = 22
LED_WRK_GPIO_PIN = 23
BUTTON_GPIO_PIN = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_RDY_GPIO_PIN, GPIO.OUT)
GPIO.setup(LED_WRK_GPIO_PIN, GPIO.OUT)
GPIO.setup(BUTTON_GPIO_PIN, GPIO.IN)  # , pull_up_down=GPIO.PID_DOWN) Wasn't needed
GPIO.output(LED_RDY_GPIO_PIN, GPIO.HIGH)

while True:
	if GPIO.input(BUTTON_GPIO_PIN):
		break
	while GPIO.input(BUTTON_GPIO_PIN):
		pass

GPIO.output(LED_RDY_GPIO_PIN, GPIO.LOW)
GPIO.output(LED_WRK_GPIO_PIN, GPIO.HIGH)

timestamp = time.strftime("%Y-%m-%d-%H-%M")
directory = "".join(["/home/pi/project/data/", timestamp, "/"])
filename = "".join([directory, "temperaturedata.log"])

if not os.path.exists(os.path.dirname(filename)):
	os.makedirs(os.path.dirname(filename))

datafile = open(filename, "w", 1)

measurement_wait = 10

button_pressed = False

dir_pre = "/sys/bus/w1/devices/"
dir_sen = "28-000004f7c7bf"
dir_suf = "/w1_slave"
dir_temp = "".join(dir_pre + dir_sen + dir_suf)

while True:
	time_1 = time.time()
	tfile = open(dir_temp)
	text = tfile.read()
	tfile.close()

	temperature_data = text.split()[-1]
	temperature = float(temperature_data[2:])
	temperature = temperature / 1000
	datafile.write(str(temperature) + "\n")

	time_2 = time.time()

	if (time_2 - time_1) < measurement_wait:
		no_of_sleeps = int(round((measurement_wait - (time_2 - time_1)) / 0.1))
		for i in range(no_of_sleeps):
			time.sleep(0.1)
			if GPIO.input(BUTTON_GPIO_PIN):
				button_pressed = True
				break
	if button_pressed:
			break
datafile.close()

GPIO.output(LED_WRK_GPIO_PIN, GPIO.LOW)

GPIO.cleanup()
