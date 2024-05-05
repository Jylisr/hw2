import network
from time import sleep
from umqtt.simple import MQTTClient
import ujson

SSID = "KME761_Group_2"
PASSWORD = "hw1Group2"
BROKER_IP = "192.168.2.253"

# Function to connect to WLAN
def connect_wlan():
    # Connecting to the group WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Attempt to connect once per second
    while wlan.isconnected() == False:
        print("Connecting... ")
        sleep(1)

    # Print the IP address of the Pico
    print("Connection successful. Pico IP:", wlan.ifconfig()[0])
    
def connect_mqtt():
    mqtt_client=MQTTClient("", BROKER_IP)
    mqtt_client.connect(clean_session=True)
    return mqtt_client

measurement = {
 "mean_hr": mean_hr,
 "mean_ppi": mean_ppi,
 "rmssd": rmssd,
 "sdnn": sdnn
}

json_message = measurement.json()


# Main program
if __name__ == "__main__":
    #Connect to WLAN
    connect_wlan()
    
    # Connect to MQTT
    try:
        mqtt_client=connect_mqtt()
        
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")

    # Send MQTT message
    try:
        topic = "pulsepal/hrv"
        message = json_message
        mqtt_client.publish(topic, message)
        print(f"Sending to MQTT: {topic} -> {message}")
            
    except Exception as e:
        print(f"Failed to send MQTT message: {e}")