# This file is executed on every boot (including wake-boot from deepsleep)

import network
import json
config = json.load(open('config.json'))

if config.get('debug', False):
    import esp
    esp.osdebug(None)

if config.get('webrepl', True):
    import gc
    import webrepl
    webrepl.start()
    gc.collect()

def wait_for_connection(sta_if):
    import utime
    while True:
        status = sta_if.status()
        if status == network.STAT_CONNECTING:
            pass
        elif status == network.STAT_GOT_IP:
            print('network config:', sta_if.ifconfig())
            return True
        else:
            # failed
            print('unable to connect to network')
            return False
        utime.sleep_us(100)

def do_connect():
    try:
        ssid = config['wifi']["ssid"]
        password = config['wifi']["password"]
    except KeyError:
        print('failed to read config.json')
        return

    sta_if = network.WLAN(network.STA_IF)
    if not wait_for_connection(sta_if):
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        wait_for_connection(sta_if)
    else:
        print('automatic reconnect successful')

do_connect()
