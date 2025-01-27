import time
import network
import socket
import dht
import os


def state_indicator(led_id, count_blinking, speed):
    count = 0
    led_initial_state = led_id.value()
    led_id.value(0)
    while count < count_blinking:
        if (led_id.value() == 0):
            led_id.value(1)
            count += 1
        else:
            led_id.value(0)
        time.sleep(speed)
    led_id.value(led_initial_state)

#Debug    
def do_measure(data): 
    data.measure()
    print("Merim")

def connect_to_wifi(ssid, password, led_id):
    count_connections = 0
    wlan = network.WLAN(network.STA_IF)
    print(wlan.ipconfig('addr4'))
    wlan.active(True)
    ip_config = ('192.168.0.171','255.255.255.0','192.168.0.1','8.8.8.8')
    wlan.ifconfig(ip_config)
    wlan.connect(ssid, password)     
    while not wlan.isconnected():
        if count_connections > 10:
            state_indicator(led_id, 3)
        print("Connecting to Wi-Fi...")
        time.sleep(1)
        count_connections = count_connections + 1
    print("Connected to Wi-Fi:", wlan.ifconfig())
    led_id.value(1)

def listening_request2(socket1):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    print('listening on', addr)
    socket1.bind(addr)
    socket1.listen(1)
    socket1.settimeout(600)

def listening_request(socket, html, senzor):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    print('listening on', addr)
    socket.bind(addr)
    socket.listen(1)
    while True:
        try:
            cl, addr = socket.accept()
            do_measure(senzor)
            print('client connected from', addr)
            request = cl.recv(1024)
            print(request)
            response = html % (senzor.temperature(),senzor.humidity())
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
        except Exception:
            state_indicator(led_id, 5, 0.75)
            cl.close()
            continue
            
def press_button(button):    
    if not button.value():
        return True
    
def save_to_file(filename, text):
    try:
        with open(filename, 'a') as file:
            file.write(text + '\n')
        print(f"Text successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def load_from_file(filename):
    try:
        with open(filename, 'r') as file: 
            content = file.read()
        return content
    except OSError:
        print(f"Error: File {filename} not found")
        return None
    
def delete_file(filename):
    if filename in os.listdir():
        os.remove(filename)
        print(f"File '{filename}' deleted successfully.")
    else:
        print(f"File '{filename}' does not exist.")

def get_current_time():
    current_time = time.time()
    year, month, mday, hour, minute, second, weekday, yearday = time.localtime()
    return (f"Datum: {year}-{month:02d}-{mday:02d} Cas: {hour:02d}:{minute:02d}:{second:02d}")