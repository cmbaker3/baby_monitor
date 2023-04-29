"""EE 250L Final Project Publisher File: Runs on RPi
Run sub.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt # Publisher/MQTT Code
import time
from datetime import datetime
import socket   # Publisher/MQTT Code
import RPi.GPIO as GPIO # Data Collection Init

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

    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_start()
    time.sleep(1)

    while True:
        # GET SAMPLE OF DATA
        print("READING DATA....")
 
        GPIO.output(led_pin, GPIO.HIGH) # Turn on LED Before Reading Sound
        time.sleep(0.5)
        sound_sum = 0 # Reset sound sum to 0
        sound_channel = 1 # Sound sensor on channel 0
        for i in range(50):
            sound_val = mcp.read_adc(sound_channel) # Read Sound Sensor on Channel 0
            print("Value: " + str(sound_val))
            sound_sum = sound_sum + sound_val
            time.sleep(0.2)
        sound_avg = sound_sum/50
        print("Average Value: " + str(sound_avg))
        GPIO.output(led_pin, GPIO.LOW)
        print("NOT READING DATA....")

        # GET TIME
        from datetime import date;
        ctime = datetime.now()
        
        # SEND SAMPLE OF DATA
        time.sleep(15) 
        #replace user with your USC username in all subscriptions
        client.publish("gtrue/ipinfo", f"{sound_avg}") #maybe change gtrue? but i think this ip address stuff is this 
        print("Publishing Reading Data.")
        time.sleep(4)
        
        # SEND TIME
        client.publish("gtrue/ctime", f"{ctime}")
        print("Publishing Time.")
        time.sleep(4)
        
        
