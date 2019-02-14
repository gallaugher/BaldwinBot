//
//  ViewController.swift
//  BaldwinBot
//
//  Created by John Gallaugher on 2/9/19.
//  Copyright © 2019 John Gallaugher. All rights reserved.
//

import UIKit
import CocoaMQTT

class ViewController: UIViewController {
    
    var stop = "stop"
    var direction: [Int: String] = [0: "forward",
                                    1: "backward",
                                    2: "left",
                                    3: "right",
                                    4: "hello",
                                    5: "niceandsmart",
                                    6: "fancylearningapps",
                                    7: "takeaflyer",
                                    8: "seeyouinireland",
                                    9: "thankyou",
                                    10: "thanksalot",
                                    11: "cheers",
                                    12: "imjustarobot"]
    
    let mqttClient = CocoaMQTT(clientID: "BaldwinBotApp", host: "136.167.122.234", port: 1883)
//     let mqttClient = CocoaMQTT(clientID: "BaldwinBotApp", host: "baldwinbot", port: 1883)
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBAction func buttonDown(_ sender: UIButton) {
        print("Sending message: \(direction[sender.tag]!)")
        mqttClient.publish("baldwinbot/move", withString: direction[sender.tag]!)
    }
    
    
    @IBAction func buttonUp(_ sender: UIButton) {
        print("Sending message: \(stop)")
        mqttClient.publish("baldwinbot/move", withString: stop)
    }
    
    @IBAction func talkButtonPressed(_ sender: UIButton) {
        print("Sending message: \(direction[sender.tag]!)")
        mqttClient.publish("baldwinbot/move", withString: direction[sender.tag]!)
    }
    
    @IBAction func connectButtonPressed(_ sender: UIButton) {
        mqttClient.connect()
    }
    
}

