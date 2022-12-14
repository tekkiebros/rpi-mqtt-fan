<div align="center">
    <a href="https://tekkiebros.de">
        <img height="150" src="https://www.tekkiebros.de/wp-content/uploads/TekkieBros-Logo_small-Kopie.jpg">
    </a>
    <br>
    <br>
    <h1>Raspberry MQTT Fan</h1>
    <p>
        Python Script to control a PWM fan with MQTT
    </p>
    <a href="https://github.com/tekkiebros/rpi-mqtt-fan/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/tekkiebros/rpi-mqtt-fan"></a>
</div>

## Introduction
This repository is based on a GitHub Gist from <a href="https://gist.github.com/SqyD/a927ab612df767a0cc892bcde23d025c">@SqyD</a>. Unfortunately the code was not maintained and finally migrated to a WEMOS/ESPHome solution.
I still wanted to use my Raspberry Pi to controle my fan rather to install additional hardware like a WEMOS. In addition I want to controll everything with Home Assistant via MQTT.

## Hardware
- Raspbery Pi (I used a Raspberry Pi 4)
- MQTT Fan (like Noctua 4 Pin 5V PWM Fan)
- Some Jumper Wires
- (Optional) Temperatur Sensor

## Install
First prepare your Raspberry Pi and perform the following lines of code:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip python3-dev python3-gpiozero
sudo pip3 install paho-mqtt
```
Clone Repository to /home/pi/Scripts
```
mkdir /home/pi/Scripts
cd /home/pi/Scripts
git clone https://github.com/tekkiebros/rpi-mqtt-fan.git
```
Open config.json file and change the values to your fits
```
cd rpi-mqtt-fan
nano config.yaml
```

```
{
    "broker": "192.168.10.4",
    "port": 1883,
    "device_id": "serverfan",
    "gpio_pin": 18,
    "pwm_freq": 25000,
    "mqttUser": "YourUser",
    "mqttPassword": "ChangeMe"
}
```

Finally copy mqttFan.service to the systemd folder and enable everything
```
sudo cp mqttFan.service /lib/systemd/system/mqttFan.service
sudo chmod 644 /lib/systemd/system/mqttFan.service
sudo systemctl daemon-reload
sudo systemctl enable mqttFan.service
sudo systemctl start mqttFan.service
```

## Home Assistant
Open your configuration.yaml and paste the following lines of code:
```
mqtt:

  fan:
    - name: "Serverschrank Luefter"
      command_topic: "homeassistant/serverfan/on/set"
      state_topic: "homeassistant/serverfan/on/state"
      percentage_command_topic: "homeassistant/serverfan/speed/set"
      percentage_state_topic: "homeassistant/serverfan/speed/state"
```
This will add a fan to your Home Assistant. Now you are able to power on/off your fan as well as set you fan speed. You can also create some automations to power on/off your fan based on a temperatur sensor.

