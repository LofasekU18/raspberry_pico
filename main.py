import uasyncio as asyncio
from machine import Pin, ADC
import time
import network
import socket
import dht

# Configure the sensor (e.g., analog sensor on ADC pin)
senzor_data = dht.DHT11(machine.Pin(28))
senzor_data.measure()
led01 = Pin(15,Pin.OUT)
html = """<!DOCTYPE html>
<html>
    <head>
        <style>
            h1, p {
                font-size: 30px;
                color: #333;
                text-align: center;  /* Center the text */
            }
        </style>
        <title>Pico W</title>
    </head>
    <body>
        <h1>Pico W</h1>
        <p>Temperature: %sC<br>Humidity: %d%%</p>
    </body>
</html>
"""
# Example: Sensor connected to GPIO26 (ADC0)
def connect_to_wifi2(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            ip = "192.168.0.170"  # Set the desired static IP
            subnet = "255.255.255.0"  # Subnet mask
            gateway = "192.168.0.1"  # Default gateway (usually the router's IP)
            dns = "8.8.8.8"  # DNS server (Google DNS in this case)

# Set the network configuration (static IP, subnet, gateway, DNS)
        wlan.ifconfig((ip, subnet, gateway, dns))
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

def save_string_to_file(file_path: str, content: str) -> None:
    with open(file_path, 'a') as file:  # Open the file in append mode
        file.write(content + '\n')  # Add a newline for separation

# Connect to Wi-Fi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ip_config = ('192.168.0.170','255.255.255.0','192.168.0.1','8.8.8.8')
    wlan.ifconfig(ip_config)
    wlan.connect(ssid, password)     
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    
    print("Connected to Wi-Fi:", wlan.ifconfig())
    led01.value(1)
def listening_request(data):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)
    while True:
        try:
            cl, addr = s.accept()
            data.measure()
            print('client connected from', addr)
            request = cl.recv(1024)
            print(request)
            response = html % (data.temperature(),data.humidity())
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()

        except OSError as e:
            print("Error:",e)
            cl.close()
            print('connection closed')
        finally:
            cl.close()
try:
    connect_to_wifi('Hacienda','739402020')
    listening_request(senzor_data)
except KeyboardInterrupt:
    print("Script stopped by user.")
except Exception as ex:
    save_string_to_file('log.txt',ex)
finally:
    led01.value(0)