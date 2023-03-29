try:
    import urequests as requests
except ModuleNotFoundError:
    import requests
import machine
import network
from time import sleep
import dht
from machine import Pin

TOKEN = "xxxxxxxx"
URL = f"https://api.telegram.org/bot{TOKEN}/"
CHAT_ID = "400948556"
WIFI_USER = 'Andre Archer Connect'
WIFI_PASS = '1234567890abb'
p2 = machine.Pin(2, machine.Pin.OUT)

sensor = dht.DHT11(Pin(14))

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_USER, WIFI_PASS)
        while not sta_if.isconnected():
            pass
    p2.value(1)
    sleep(0.5)
    p2.value(0)
    print('network config:', sta_if.ifconfig())


def send_message(text, chat_id):
    url = f"{URL}sendMessage?text={text}&chat_id={chat_id}"
    response = requests.get(url)
    content = response.text
    return content


def measure_temp_and_hum():
    sensor.measure()
    print('measuring...')
    temp = sensor.temperature()
    hum = sensor.humidity()
    return {'temp': temp, 'hum': hum}


if __name__ == '__main__':
    do_connect()
    mth = measure_temp_and_hum()
    send_message(f"Temperature: {mth.get('temp')}", CHAT_ID)

