import json
import machine

import umqtt.simple
import si7021

config = json.load(open('config.json'))

def sleep(seconds):
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after N seconds (waking the device)
    rtc.alarm(rtc.ALARM0, seconds * 1000)

    # put the device to sleep
    machine.deepsleep()

def fetch_and_publish():
    sensor = si7021.Si7021()

    client = umqtt.simple.MQTTClient(config['mqtt']['client_id'],
                                     config['mqtt']['broker']['server'])
    client.connect()

    client.publish(config['mqtt']['topic'].encode('ascii'),
                   json.dumps({
                       'temperature': sensor.readTemp(),
                       'humidity': sensor.readRH()
                    }).encode('ascii')
                   )
    client.disconnect()

try:
    fetch_and_publish()
except Exception as thrown:
    # Handle errors, most likely network, this will just keep us on going to sleep
    # if we leave unhandled we never sleep and battery will die...

    # makes debug easier if printed to serial.
    print(thrown)

if config['period'] is not None:
    sleep(config['period'])
