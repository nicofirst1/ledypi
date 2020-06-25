import network
import time

def get_credential():
    with open("website/wifi_credential.txt", "r") as f:
        ssid = f.readline()
        pws = f.readline()

    ssid = ssid.split("=")[1].strip()
    pws = pws.split("=")[1].strip()

    print("SSID='%s'\nPsw='%s'" % (ssid,pws))

    return ssid, pws


def connect():
    print("Connecting to WIFI...")

    sta_if = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)  # create access-point interface
    ap.active(False)  # deactivate the interface
    start = time.ticks_ms()
    to = 10000
    ssid,psw= get_credential()

    while not sta_if.isconnected():
        if time.ticks_diff(time.ticks_ms(), start) > to:
            print('Timeout')
            break
        print('Connecting to %s...' % ssid)
        sta_if.active(True)
        sta_if.connect(ssid, psw)
        while not sta_if.isconnected() and time.ticks_diff(time.ticks_ms(), start) < to:
            print('Connecting to %s...' %ssid)
            time.sleep_ms(500)
    else:
        print('network config:', sta_if.ifconfig())
        a = sta_if.config('mac')
        print('MAC {:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(a[0], a[1], a[2], a[3], a[4]))


    return sta_if.isconnected()