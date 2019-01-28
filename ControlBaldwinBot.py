# ControlBaldwinBot.py

# Added as part of MQTT
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

import time

# Import the Robot.py file (must be in the same directory as this file!).
import Robot

moveDuration = 0.05 # each move will take 1/20th (0.05) of a second.
turnDuration = 0.02 # each turn will take 1/50th (0.02) of a second.
moveSpeed = 150 # needs about 100 to begin to move, max = 255
turnSpeed = 200

# Added as part of MQTT
clientName = "RPI"
serverAddress = "10.0.1.186"
# Instantiate Eclipse Paho as mqttClient
mqttClient = mqtt.Client(clientName)

# If the robot veers left or right, add a small amount to the left or right trim, below
# until the bot moves roughly straight. The #s below reflect the bot I'm working with.
# It's probably best to start both trim values at 0 and adjust from there.

LEFT_TRIM   = 0
RIGHT_TRIM  = 20

def connectionStatus(client, userdata, flags, rc):
    mqttClient.subscribe("rpi/gpio")

def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    
    if message == "up":
        # gpio.output(21, gpio.HIGH)
        robot.forward(moveSpeed, moveDuration)   # Move forward at speed 150 for 1/10th of a second.
        print("^^^ moving forward!")
    elif message == "stop":
        # gpio.output(21, gpio.LOW)
        robot.stop()
        print("!!! stopping!")
    elif message == "down":
        # gpio.output(21, gpio.LOW)
        robot.backward(moveSpeed, moveDuration)   # Move forward at speed 150 for 1/10th of a second.
        print("\/ down \/")
    elif message == "left":
        robot.left(turnSpeed, turnDuration)
        print("<- left")
    elif message == "right":
        robot.right(turnSpeed, turnDuration)
        print("-> right")
    else:
        print("?!? Unknown message?!?")

# Set up calling functions to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

# Create an instance of the robot with the specified trim values.
# Not shown are other optional parameters:
#  - addr: The I2C address of the motor HAT, default is 0x60.
#  - left_id: The ID of the left motor, default is 1.
#  - right_id: The ID of the right motor, default is 2.
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# Added as part of MQTT
mqttClient.connect(serverAddress)
mqttClient.loop_forever()

