import network
import config
from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient       

ledPin = Pin(2, Pin.OUT)
lights = Pin(5, Pin.OUT)

def boardTest():
    print("INFO: Blinking LED")
    global ledPin    
    for i in range(0, 4, 1):
        ledPin.value(not ledPin.value())
        sleep(1)
        i = i + 1
    print("INFO: Board is fine")

def turn_on():
    global lights
    lights.value(1)
    print("INFO: Turning on lights")

def turn_off():
    global lights
    lights.value(0)
    print("INFO: Turning off lights")  

def wifiConnect():
    print("INFO: Connecting to wifi")  
    ssid = config.WIFI_ESSID
    password = config.WIFI_PASSWORD
    station = network.WLAN(network.STA_IF)# create station interface
    station.active(True)# activate the interface
    if station.isconnected():
        print("INFO: Connected to wifi initially")
    else:
        while True:
            try:
                scanned_wifi = station.scan()# scan for access points
                for i in scanned_wifi:
                    if i[0].decode('utf-8') == ssid:
                        station.connect(ssid, password)
                        print("INFO: Connected to wifi")
                        break
                    else:
                        print("INFO: Wifi Not found")
                        wifiConnect()
                break
            except OSError as e:
                print("Error: ", e)
        


def on_message(topic, msg):
    message = msg.decode("utf-8")
    if message == "ON":
        turn_on()
    elif message == "OFF":
        turn_off()


def main():
    boardTest()
    wifiConnect()
    print("INFO: Connecting to MQTT")
    host = config.MQTT_HOST
    port = config.MQTT_PORT
    topic = config.MQTT_TOPIC
    client = MQTTClient("umqtt_client", host, port)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(topic)
    while True:
        client.wait_msg()

if __name__ == "__main__":
    main()