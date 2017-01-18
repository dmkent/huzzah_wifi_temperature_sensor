# This file is executed on every boot (including wake-boot from deepsleep)

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

def do_connect():
    import network
    try:
        ssid = config['wifi']["ssid"]
        password = config['wifi']["password"]
    except KeyError:
        print('failed to read config.json')
        return
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while True:
            status = sta_if.status()
            if status == network.STAT_CONNECTING:
                pass
            elif status == network.STAT_GOT_IP:
                print('network config:', sta_if.ifconfig())
                break
            else:
                # failed
                print('unable to connect to network')
                break

do_connect()
