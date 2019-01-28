//
//  ViewController.swift
//  BaldwinBot
//
//  Created by John Gallaugher on 1/21/19.
//  Copyright © 2019 John Gallaugher. All rights reserved.
//

import UIKit
import CocoaMQTT

class ViewController: UIViewController {
    @IBOutlet weak var upButton: UIButton!
    @IBOutlet weak var downButton: UIButton!
    @IBOutlet weak var leftButton: UIButton!
    @IBOutlet weak var rightButton: UIButton!
    @IBOutlet weak var stopButton: UIButton!
    
    @IBOutlet weak var connectButton: UIButton!
    @IBOutlet weak var disconnectButton: UIButton!
    
    // let mqttClient = CocoaMQTT(clientID: "iOS Device", host: "192.168.0.X", port: 1883)
    let mqttClient = CocoaMQTT(clientID: "iOS Device", host: "10.0.1.186", port: 1883)
    var timer: Timer?
    var messageString = "stop"
    var moveDuration = 0.05
    var turnDuration = 0.02
    var duration: Double!
    var currentButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    func sendMessage(gesture: UILongPressGestureRecognizer) {
        if gesture.state == .began {
            currentButton.isHighlighted = true
            timer = Timer.scheduledTimer(timeInterval: moveDuration, target: self, selector: #selector(handleTimer), userInfo: nil, repeats: true)
        } else if gesture.state == .ended || gesture.state == .cancelled {
            currentButton.isHighlighted = false
            timer?.invalidate()
            timer = nil
            mqttClient.publish("rpi/gpio", withString: "stop")
        }
    }

    @IBAction func upButtonPressed(_ gesture: UILongPressGestureRecognizer) {
        messageString = "up"
        currentButton = upButton
        duration = moveDuration
        sendMessage(gesture: gesture)
    }
    
    @IBAction func downPressed(_ gesture: UILongPressGestureRecognizer) {
        messageString = "down"
        currentButton = downButton
        duration = moveDuration
        sendMessage(gesture: gesture)
    }
    
    @IBAction func leftPressed(_ gesture: UILongPressGestureRecognizer) {
        messageString = "left"
        currentButton = leftButton
        duration = turnDuration
        sendMessage(gesture: gesture)
    }
    
    @IBAction func rightPressed(_ gesture: UILongPressGestureRecognizer) {
        messageString = "right"
        currentButton = rightButton
        duration = turnDuration
        sendMessage(gesture: gesture)
    }
    
    @IBAction func stopButtonPressed(_ sender: UIButton) {
        mqttClient.publish("rpi/gpio", withString: "stop")
    }
    
    @objc func handleTimer(timer: Timer) {
        mqttClient.publish("rpi/gpio", withString: messageString)
        print(messageString)
    }
    
    @IBAction func connectPressed(_ sender: UIButton) {
        mqttClient.connect()
    }
    
    @IBAction func disconnectPressed(_ sender: UIButton) {
        mqttClient.disconnect()
    }
}

