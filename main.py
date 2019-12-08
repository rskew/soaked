import machine
import time
import os
import _thread
import socket


## Set up i/o

pots_solenoid_pin = machine.Pin(16, machine.Pin.OUT)
tomato_solenoid_pin = machine.Pin(17, machine.Pin.OUT)

# Relays to control solenoids are active-low
tomato_solenoid = machine.Signal(tomato_solenoid_pin, invert=True)
pots_solenoid = machine.Signal(pots_solenoid_pin, invert=True)

tomato_solenoid.off()
pots_solenoid.off()


## Start web app
#
# Code mostly lifted from https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/

def web_page():
  if tomato_solenoid.value() == 1:
    tomato_state="ON"
  else:
    tomato_state="OFF"

  if pots_solenoid.value() == 1:
    pots_state="ON"
  else:
    pots_state="OFF"

  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>Irrigation control for front yard</h1> 
  <p>Tomato garden bed: <strong>""" + tomato_state + """</strong></p><p><a href="/?tomatos=on"><button class="button">ON</button></a></p>
  <p><a href="/?tomatos=off"><button class="button button2">OFF</button></a></p>
  <p>Pots and potatos: <strong>""" + pots_state + """</strong></p><p><a href="/?pots=on"><button class="button">ON</button></a></p>
  <p><a href="/?pots=off"><button class="button button2">OFF</button></a></p></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

def server():
    while True:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      request = str(request)
      print('Content = %s' % request)

      tomatos_on = request.find('/?tomatos=on')
      tomatos_off = request.find('/?tomatos=off')
      if tomatos_on == 6:
        print('TOMATOS ON')
        tomato_solenoid.on()
      if tomatos_off == 6:
        print('TOMATOS OFF')
        tomato_solenoid.off()

      pots_on = request.find('/?pots=on')
      pots_off = request.find('/?pots=off')
      if pots_on == 6:
        print('POTS ON')
        pots_solenoid.on()
      if pots_off == 6:
        print('POTS OFF')
        pots_solenoid.off()

      response = web_page()
      try:
          conn.send('HTTP/1.1 200 OK\n')
          conn.send('Content-Type: text/html\n')
          conn.send('Connection: close\n\n')
          conn.sendall(response)
      except Exception as e:
          print(e)
      conn.close()

# Run server in a new thread so that webrepl can still be used
_thread.start_new_thread(server, [])
