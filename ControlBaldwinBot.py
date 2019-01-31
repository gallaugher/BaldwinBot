# ControlBaldwinBot.py

# Added as part of MQTT
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
# import RPi.GPIO as gpio
import time

from adafruit_motorkit import MotorKit
kit = MotorKit()

"""
# Import the Robot.py file (must be in the same directory as this file!).
import Robot

moveDuration = 0.05 # each move will take 1/20th (0.05) of a second.
turnDuration = 0.02 # each turn will take 1/50th (0.02) of a second.
moveSpeed = 150 # needs about 100 to begin to move, max = 255
turnSpeed = 200
"""

# Added as part of MQTT
clientName = "RPI"
# HOME
serverAddress = "10.0.1.186"
# BC
# serverAddress = "136.167.122.187"
# Instantiate Eclipse Paho as mqttClient
mqttClient = mqtt.Client(clientName)

# If the robot veers left or right, add a small amount to the left or right trim, below
# until the bot moves roughly straight. The #s below reflect the bot I'm working with.
# It's probably best to start both trim values at 0 and adjust from there.

# out of 1.0 full power.
LEFT_TRIM   = -0.01
RIGHT_TRIM  = 0.0

leftSpeed = 1.0 + LEFT_TRIM
rightSpeed = 1.0 + RIGHT_TRIM
duration = 0.05
slowTurnBy = 0.5

# move duration is the legnth of time for each move.
# larger values will add delay when releasing a button from
# the iOS app. These values should be the same between this app & the iOS app.

def connectionStatus(client, userdata, flags, rc):
    print("subscribing")
    mqttClient.subscribe("rpi/gpio")
    print("subscribed")

def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    
    if message == "up":
        # gpio.output(21, gpio.HIGH)
        #robot.forward(moveSpeed, moveDuration)   # Move forward at speed 150 for 1/10th of a second.
        kit.motor1.throttle = leftSpeed
        kit.motor2.throttle = rightSpeed
        time.sleep(duration)
        # You need to stop the bot's motion, otherwise wheels will keep spinning
        # kit.motor1.throttle = 0.0
        # kit.motor2.throttle = 0.0
        print("^^^ moving forward!")
    elif message == "stop":
        # gpio.output(21, gpio.LOW)
        # likely not needed, but added anyway:
        kit.motor1.throttle = 0.0
        kit.motor2.throttle = 0.0
        print("!!! stopping!")
    elif message == "down":
        # gpio.output(21, gpio.LOW)
        # robot.backward(moveSpeed, moveDuration)   # Move forward at speed 150 for 1/10th of a second.
        kit.motor1.throttle = -leftSpeed
        kit.motor2.throttle = -rightSpeed
        print("\/ down \/")
        time.sleep(duration)
        # You need to stop the bot's motion, otherwise wheels will keep spinning
        #kit.motor1.throttle = 0.0
        #kit.motor2.throttle = 0.0
    elif message == "left":
        # robot.left(turnSpeed, turnDuration)
        kit.motor1.throttle = -leftSpeed * slowTurnBy
        kit.motor2.throttle = rightSpeed * slowTurnBy
        print("<- left")
        time.sleep(duration)
        # You need to stop the bot's motion, otherwise wheels will keep spinning
        # kit.motor1.throttle = 0.0
        # kit.motor2.throttle = 0.0
    elif message == "right":
        # robot.right(turnSpeed, turnDuration)
        kit.motor1.throttle = leftSpeed * slowTurnBy
        kit.motor2.throttle = -rightSpeed * slowTurnBy
        print("-> right")
        time.sleep(duration)
        # You need to stop the bot's motion, otherwise wheels will keep spinning
        # kit.motor1.throttle = 0.0
        # kit.motor2.throttle = 0.0
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
# robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# Added as part of MQTT
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
