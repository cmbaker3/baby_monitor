"""EE 250L Lab 04 Starter Code
Run vm_pub.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import numpy as np

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """

def on_connect(client, userdata, flags, rc):
    """Once our client has successfully connected, it makes sense to subscribe to
    all the topics of interest. Also, subscribing in on_connect() means that, 
    if we lose the connection and the library reconnects for us, this callback
    will be called again thus renewing the subscriptions"""

    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe("gtrue/ipinfo")
    #client.subscribe("gtrue/ctime")
    
    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("gtrue/ipinfo", on_message_from_ipinfo)
    #client.message_callback_add("gtrue/ctime", on_message_from_ctime)

"""This object (functions are objects!) serves as the default callback for 
messages received when another node publishes a message this client is 
subscribed to. By "default,"" we mean that this callback is called if a custom 
callback has not been registered using paho-mqtt's message_callback_add()."""
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

#Custom message callback.
#def on_message_from_ipinfo(client, userdata, message):
   #print("Custom callback  - IP Message: "+message.payload.decode())
#def on_message_from_ctime(client, userdata, message):
   #print("Custom callback  - Current Time: "+message.payload.decode())

# Store the sound readings
sound_data = []

# Set threshold for crying detection, this is low, might need to be adjusted
threshold = 100

# Custom callback for receiving sound data
def on_message_from_ipinfo(client, userdata, message):
    print("Average Value: " + message.payload.decode())
    # print("Average Value: " + message)
    # print("Average Value: " + client)
    sound_val = message.payload.decode()
    sound_data.append(sound_val)
    if sound_val >= threshold:
        print("Baby is crying!")
    
    # Plot the sound data
    if len(sound_data) == 20:
        # Create a time axis for the plot
        time_axis = np.arange(len(sound_data))

        # Plot the sound data
        plt.plot(time_axis, sound_data)
        plt.xlabel('Time (s)')
        plt.ylabel('Sound Value')
        plt.title('Baby Monitor Sound Data')
        plt.show()



if __name__ == '__main__':
    
    #create a client object
    client = mqtt.Client()
    #attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    
    #IMPORTANT: THIS CODE MIGHT NEED TO BE ADDED IN HERE
    # Attach the on_message_from_ipinfo callback to the client
    #client.message_callback_add("gtrue/ipinfo", on_message_from_ipinfo)
    
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python. For example:
    
    `client.connect("eclipse.usc.edu", 11000, 60)` 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)

    """In our prior labs, we did not use multiple threads per se. Instead, we
    wrote clients and servers all in separate *processes*. However, every 
    program with networking involved generally requires multiple threads to
    make coding simpler. Using MQTT is no different. If you are doing nothing 
    in this thread, you can run 
    
    `client.loop_forever()`
    
    which will block forever. This function processes network traffic (socket 
    programming is used under the hood), dispatches callbacks, and handles 
    reconnecting."""
    client.loop_forever()
