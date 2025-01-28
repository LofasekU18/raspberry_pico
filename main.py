from machine import Pin
import time
import network
import socket
import dht
import os
import my_func


SSID = ''
PASSWORD = ''
senzor01 = dht.DHT11(machine.Pin(28))
led01 = Pin(15,Pin.OUT)
button01 = machine.Pin(13, machine.Pin.IN,machine.Pin.PULL_UP)
socket01 = socket.socket()
interval = 60 * 60 * 1000
html = """<!DOCTYPE html>
<html>
    <head>
        <style>
            h1, p
                {
                font-size: 50px;
                color: #333;
                text-align: center; 
                }
            table
                {
                margin-left: auto;
                margin-right: auto;
                }
            th, td
                {
                border: 1px solid #ddd;
                padding: 10px;
                }
        </style>
        <title>Pico W</title>
    </head>
    <body>
        <h1>Pico W</h1>
        <table>
        <thead>
            <tr>
                <th>Teplota</th>
                <th>Vlhkost</th>
                <th>Cas</th>
            </tr>
        </thead>
        <tbody>
            %s
        </tbody>
        </table>
    </body>
    <script>
        console.log("Hello");
    </script>
</html>
"""

def main():
    
    if my_func.press_button(button01):
                print("3")
                my_func.delete_file("measure.txt")
                senzor01.measure()
                measured_history = f"<tr><td>{senzor01.temperature()} C</td><td>{senzor01.humidity()} %</td><td>{my_func.get_current_time()}</td></tr>"
                my_func.state_indicator(led01,3,0.2)
                time.sleep(5)
    else:
        measured_history = my_func.load_from_file("measure.txt")         
    my_func.connect_to_wifi(SSID,PASSWORD,led01)
    my_func.listening_request2(socket01)
    start_time = time.ticks_ms()
    while True:
        try:
            print("1")
            current_time = time.ticks_ms()
            if (time.ticks_diff(current_time, start_time) >= interval):
                print("2")
                senzor01.measure()
                time.sleep(3)
                my_func.save_to_file("measure.txt",f"<tr><td>{senzor01.temperature()} C</td><td>{senzor01.humidity()} %</td><td>{my_func.get_current_time()}</td></tr>")
                time.sleep(3)
                measured_history = my_func.load_from_file("measure.txt")
                start_time = time.ticks_ms()
            else:
                print("4")
                cl, addr = socket01.accept()
                print("5")
                print('client connected from', addr)
                request = cl.recv(1024)
                print(request)
                response = html % measured_history
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
                cl.close()
        except OSError:
            continue
        except Exception as e:
            print(e)
            my_func.state_indicator(led01, 5)
            cl.close()
            
main()