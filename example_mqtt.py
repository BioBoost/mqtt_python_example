# Wat libraries die je moet toevoegen om er gebruik te kunnen van maken
import paho.mqtt.client as mqtt
import time
from uuid import getnode as get_mac

# Als broker kan je gebruik maken van deze gratis publieke broker
BROKER_ADDRESS = "broker.mqttdashboard.com"
BROKER_POORT = 1883
    # Raadplegen via: http://www.mqtt-dashboard.com/

# Onderstaande methodes worden vanuit de mqtt client aangeroepen.
# De mqtt client wordt gemaakt in het hoofdprogramma lager in dit script

# Print wat informatie als de client geconnecteerd is met de broker
def on_connect(client, userdata, flags, rc):
    m = "Connected flags" + str(flags) + "result code " \
        + str(rc) + "client1_id " + str(client)
    print(m)

# Het hoofdprogramma
if __name__ == '__main__':
    # We moeten een ID hebben voor de client dat uniek is
    # Daarom kan je best gebruik maken van het MAC-address van je Ethernet
    # interface dat uniek is
    mac = get_mac()

    # Maak een MQTT client en geef het ID mee
    mqtt_client = mqtt.Client(str(mac) + "-python_robocar")
        # Door achter het ID nog een string toe te voegen kunnen we
        # later nog een andere client indien nodig, zorg dan gewoon
        # dat de string die je achter het MAC address plaats anders is

    # Geef aan dat de methode on_connect moeten worden aangeroepen door de client
    # wanneer de connectie met de broker werd opgezet
    mqtt_client.on_connect = on_connect

    # Zet de connectie op met de broker
    mqtt_client.connect(BROKER_ADDRESS, BROKER_POORT)

    # Even wachten om connectie opzet tijd te geven
    time.sleep(3)

    # Start het luisterproces (gaat luisteren naar berichten van de broker)
    mqtt_client.loop_start()

    # Onderstaande code gaat nu om de x aantal seconden (kies je zelf) het toerental
    # gaan doorgeven via een publish naar de broker. Een client die dan gesubscribed is
    # op het toerental topic krijgt dan de informatie en kan deze afbeelden
    print ('Press Ctrl-C to quit.')
    while True:
        # Versturen van bericht
        toerental = 101
        print "Bezig met versturen van toerental"
        (status, mid) = mqtt_client.publish('robotcar/status/toerental', toerental, 0)
            # Hier sturen we als voorbeeld 101 door. Natuurlijk dat je hier het eigenlijke
            # toerental moeten berekenen en doorsturen
            # Die laatste parameter '0' is de QOS = quality of service,
            # zie http://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels
            # Voor meer info

        # Voor alle zekerheid controle uitvoeren of het gelukt is
        if status != 0:
            print("Kon toerental niet verzenden naar broker")

        # Wacht nu even (hier als voorbeeld 10 seconden, bekijk zelf eens hoelang
        # je best kan wachten)
        time.sleep(10)

    # Als je op CTRL-C geduwt hebt moet de connectie met de broker worden afgesloten
    # en het luister process worden gestopt
    print "Disconnecting"
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
