import paho.mqtt.client as mqtt
from gpiozero import PWMOutputDevice
import json

# Load configuration from config file
config = json.load(open('./config.json'))

# MQTT configuration
broker = config["broker"]
port = config["port"]
device_id = config["device_id"]
on_topic = 'homeassistant/' + device_id + '/on/set'
on_state_topic = 'homeassistant/' + device_id + '/on/state'
speed_topic = 'homeassistant/' + device_id + '/speed/set'
speed_state_topic = 'homeassistant/' + device_id + '/speed/state'

# gpio settings
gpio_pin = config["gpio_pin"]
pwm_freq = config["pwm_freq"] #Fan Specific. Noctua Fans are working with 25kHz


class PwmFan:
  on_state = 'OFF'
  pwm = PWMOutputDevice(gpio_pin,frequency=pwm_freq)
  speed_state = 1

  def switch(self, onoff):
    if onoff == 'ON':
      if self.on_state == 'OFF':
        self.on_state = 'ON'
        self.set_speed(self.speed_state)
    elif onoff == 'OFF':
      if self.on_state == 'ON':
        self.on_state = 'OFF'
        self.pwm.off()

  def set_speed(self,speed):
    speedvalue = float(speed)/100
    if self.on_state == 'ON':
      self.pwm.value=speedvalue
    self.speed_state = speed


fan = PwmFan()

def on_message(client, userdata, message):
  payload = str(message.payload.decode("utf-8"))
  topic = message.topic
  if topic == on_topic:
    print("ON/OF command received")
    if (payload == 'ON') or (payload == 'OFF'):
      print("turning " + payload)
      fan.switch(payload)
      client.publish(on_state_topic, payload)
      if payload == 'ON':
        client.publish(speed_state_topic, fan.speed_state)
  elif message.topic == speed_topic:
    print('Setting speed to ' + payload)
    fan.set_speed(payload)
    if fan.on_state == 'ON':
      client.publish(speed_state_topic, fan.speed_state)

# Send messages in a loop
client = mqtt.Client("myfan")
client.on_message = on_message
# If your homeassistant is protected by as password, uncomment this next line:
client.username_pw_set(config["mqttUser"],config["mqttPassword"])
client.connect(broker, port)
client.subscribe(on_topic)
client.subscribe(speed_topic)
client.loop_forever()
