"""EE 250L Final Project Publisher File: Runs on RPi
Run sub.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt # Publisher/MQTT Code
import time
from datetime import datetime
import socket   # Publisher/MQTT Code
import RPi.GPIO as GPIO # Data Collection Init
import matplotlib.pyplot as plt
import numpy as np

# HARDWARE INITIALIZATION: 
# Import SPI library (for hardware SPI) and MCP3008 library. (Data Collection)
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
    
GPIO.setmode(GPIO.BCM) # Use BCM Configuration
GPIO.setwarnings(False)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Set channels as outputs
led_pin = 17
GPIO.setup(led_pin, GPIO.OUT) # Set LED as an Output; BCM 17


"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))


if __name__ == '__main__':
    #get IP address
    ip_address=0 
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    # print(f"IP Address: {ip_address}") 
    
    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python. For example:
    
    `client.connect("eclipse.usc.edu", 11000, 60)` 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""

    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_start()
    time.sleep(1)
    
    #creating a list to store the baby's noises from sound sensor
    sound_data = []
    
    while True:
        # GET SAMPLE OF DATA
        print("READING DATA....")
        GPIO.output(led_pin, GPIO.HIGH) # Turn on LED Before Reading Sound
        time.sleep(0.5)
        sound_sum = 0 # Reset sound sum to 0
        sound_channel = 1 # Sound sensor on channel 0
        sound_readings = [] # List to store sound readings
        for i in range(50):
            sound_val = mcp.read_adc(sound_channel) # Read Sound Sensor on Channel 0
            print("Value: " + str(sound_val))
            sound_sum = sound_sum + sound_val
            sound_readings.append(sound_val)
            time.sleep(0.2)
        sound_avg = sound_sum/50
        print("Average Value: " + str(sound_avg))
        GPIO.output(led_pin, GPIO.LOW)
        print("NOT READING DATA....")
        client.publish("gtrue/ipinfo", str(sound_avg))  # Publish sound average to broker
        #sound_data.extend(sound_readings) # Add the sound readings to the sound_data list
    
    # i originally put this here but it would not create the plot on the computer, I 
    #could send plot to computer through terminal and this command
    # scp pi@192.168.0.100:/path/to/image.png user@192.168.0.101:/path/to/destination/
    # if you update the name pi and user and change ip addresses
    #plt.plot(np.arange(len(sound_data)), sound_data)
    #plt.title('Baby\'s Noises')
    #plt.xlabel('Time (0.2s intervals)')
    #plt.ylabel('Sound Level')
    #plt.show()
