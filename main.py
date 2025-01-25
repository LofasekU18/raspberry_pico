from machine import Pin
import time
import network
import socket
import dht
import os
import my_func


SSID = 'Hacienda'
PASSWORD = '739402020'
senzor01 = dht.DHT11(machine.Pin(28))
led01 = Pin(15,Pin.OUT)
button01 = machine.Pin(13, machine.Pin.IN,machine.Pin.PULL_UP)
count = 0
socket01 = socket.socket()
interval = 10 * 10 * 1000
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
    measured_history = my_func.load_from_file("measure.txt")
    if my_func.press_button(button01):
                print("3")
                my_func.delete_file("measure.txt")
                measured_history = "<p>Vymazano</p>"
                print("Deleted")
                time.sleep(3)
    start_time = time.ticks_ms()
    my_func.connect_to_wifi(SSID,PASSWORD,led01)
    my_func.listening_request2(socket01)
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
                print("Add")
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
            

# Get the current time in milliseconds

#senzor01.measure()

#my_func.delete_file("test.txt")


#while True:
 #   current_time = time.ticks_ms()
  #  if time.ticks_diff(current_time, start_time) >= interval:
   #     print("1 minutes have passed!")
    #    start_time = time.ticks_ms()  # Reset timer
   # time.sleep(1)  # Sleep to avoid CPU overuse (not required but useful)


#led01.value(0)
#while True:
#    if my_func.press_button(button01):
#        print("Zmacknuto")
#        my_func.state_indicator(led01,5)
#    else:
#        print(time.ticks_ms()) 
#        time.sleep(1)
    
#led01.value(0)
#state_indicator(led01,5)           
#extensions.test_button(count, button01)           
#my_func.connect_to_wifi(SSID,PASSWORD,led01)
#my_func.listening_request(socket,html,senzor)
#except Exception as e:
   # print('Konec sam',e,e.args,type(e))
    #listening_request(senzor)
#except BaseException:
 #   print('Konec uzivatel')
#finally:
 #   led01.value(0)
  #  s.close()
   # print('Finally')
    #machine.soft_reset()