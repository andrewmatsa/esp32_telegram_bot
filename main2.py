# try:
#     import urequests as requests
# except ModuleNotFoundError:
#     import requests
import urequests as requests
import machine
from machine import Pin, ADC
import network
from time import sleep

TOKEN = "xxxxxxxx"
URL = f"https://api.telegram.org/bot{TOKEN}/"
CHAT_ID = "400948556"
WIFI_USER = 'Andre Archer Connect'
WIFI_PASS = '1234567890abb'


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_USER, WIFI_PASS)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def get_url(url):
    print(f'requesting GET "{url}"')
    response = requests.get(url)
    # response = urequests.request('GET', url)
    content = response.text
    return content


def send_message(text, chat_id):
    url = f"{URL}sendMessage?text={text}&chat_id={chat_id}"
    get_url(url)


def calc_formula():
    pot = ADC(0)
    r1 = 30000
    r2 = 7500
    pot_value = pot.read() * 3.3 / 1023.0
    vin = pot_value / (r2 / (r1 + r2))
    real = f'Voltage: {vin}\n'
    real_fluff = f'Voltage with fluff: {vin - 0.57}\n'
    # average calc
    # aver = (real + (vin - float(0.57)))/2
    aver = "update"
    average_value = f'Voltage average: {aver}\n'
    return {"real": real, "real_fluff": real_fluff, "average_value": average_value}

def execu():
    timer = 20
    import time
    i = int(time.time()) + timer
    while int(time.time()) <= i:
        send_message("bla", CHAT_ID)
        # send_message(((calc_formula().get('real')),
        #                     (calc_formula().get('real_fluff')),
        #                     (calc_formula().get('average_value'))), CHAT_ID)
        sleep(3)
    print(f'Exit on "{timer}" seconds')

if __name__ == '__main__':
    do_connect()
    req = requests.get("https://api.telegram.org/bot{}/sendMessage?text=hallo&chat_id={}").format(TOKEN, CHAT_ID)

    print(req.status_code)
    print(req.text)

    # execu()
