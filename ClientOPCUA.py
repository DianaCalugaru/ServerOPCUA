from datetime import datetime
import datetime
import pyodbc as pyodbc
from opcua import Client
import time

# Variabile pentru a memora valorile anterioare
prev_led1_state = None
prev_led2_state = None
prev_led3_state = None
prev_led5_state = None
prev_led6_state = None
prev_hum_state = None
prev_temp_state = None
prev_flame_state = None
prev_sound_state = None

url = "opc.tcp://169.254.15.16:4840"

client = Client(url)

client.connect()
print("Client Connected")

# Definirea datelor de conectare la baza de date
server = 'DESKTOP-8QAOT1N\SQLEXPRESS'
database = 'IoT'
driver = '{SQL Server}'  # driver-ul de conectare

# Conectarea la baza de date
conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
cursor = conn.cursor()


def insert_led_state(id, name, state):
    insert_query_led = f"INSERT INTO Table_LED (ID, Nume, Stare, Data) VALUES ({id}, '{name}', '{state}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
    cursor.execute(insert_query_led)


def insert_dht11_values(id, name, value):
    insert_query_dht11 = f"INSERT INTO Table_DHT11 (ID, Nume, Valoare, Data) VALUES ({id}, '{name}', '{value}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
    cursor.execute(insert_query_dht11)


def insert_flame_value(name, value):
    insert_query_flame = f"INSERT INTO Table_Flame (Nume, Valoare, Data) VALUES ('{name}', '{value}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
    cursor.execute(insert_query_flame)

def insert_sound_value(name, value):
    insert_query_flame = f"INSERT INTO Table_Sound (Nume, Valoare, Data) VALUES ('{name}', '{value}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
    cursor.execute(insert_query_flame)

while True:
    led1 = client.get_node("ns=2;i=5")
    Led1 = led1.get_value()
    print(Led1)

    led2 = client.get_node("ns=2;i=6")
    Led2 = led2.get_value()
    print(Led2)

    led3 = client.get_node("ns=2;i=7")
    Led3 = led3.get_value()
    print(Led3)

    led5 = client.get_node("ns=2;i=8")
    Led5 = led5.get_value()
    print(Led5)

    led6 = client.get_node("ns=2;i=9")
    Led6 = led6.get_value()
    print(Led6)

    if Led1 != prev_led1_state:
        if Led1 == 1:
            led1_state = 'Aprins'
        else:
            led1_state = 'Stins'
        insert_led_state(1, 'LED1', led1_state)

    if Led2 != prev_led2_state:
        if Led2 == 1:
            led2_state = 'Aprins'
        else:
            led2_state = 'Stins'
        insert_led_state(2, 'LED2', led2_state)

    if Led3 != prev_led3_state:
        if Led3 == 1:
            led3_state = 'Aprins'
        else:
            led3_state = 'Stins'
        insert_led_state(3, 'LED3', led3_state)

    if Led5 != prev_led5_state:
        if Led5 == 1:
            led5_state = 'Aprins'
        else:
            led5_state = 'Stins'
        insert_led_state(4, 'LED5', led5_state)

    if Led6 != prev_led6_state:
        if Led6 == 1:
            led6_state = 'Aprins'
        else:
            led6_state = 'Stins'
        insert_led_state(5, 'LED6', led6_state)


    hum = client.get_node("ns=2;i=10")
    Hum6 = hum.get_value()
    print(Hum6)

    temp = client.get_node("ns=2;i=11")
    Temp = temp.get_value()
    print(Temp)

    if Hum6 != prev_hum_state:
        insert_dht11_values(1, 'Umiditate', Hum6)

    if Temp != prev_temp_state:
        insert_dht11_values(2, 'Temperatura', Temp)


    flame = client.get_node("ns=2;i=12")
    Flame = flame.get_value()
    print(Flame)

    if Flame == 1:
        Flame_state = 'Detectat'
        print(Flame_state)
    else:
        Flame_state = 'Nedetectat'
        print(Flame_state)

    if Flame != prev_flame_state:
        insert_flame_value('Flame', Flame_state)

     #////////////
    sound = client.get_node("ns=2;i=13")
    Sound = sound.get_value()
    print(Sound)

    if Sound == 1:
        Sound_state = 'Detectat'
        print(Sound_state)
    else:
        #Sound_state = 'Nedetectat'
        print(Sound_state)

    if Sound != prev_sound_state:
        insert_sound_value('Sound', Sound_state)


    # Update previous states
    prev_led1_state = Led1
    prev_led2_state = Led2
    prev_led3_state = Led3
    prev_led5_state = Led5
    prev_led6_state = Led6
    prev_hum_state = Hum6
    prev_temp_state = Temp
    prev_flame_state = Flame
    prev_sound_state = Sound

    time.sleep(2)
    conn.commit()

# Închiderea conexiunii cu baza de date
cursor.close()
conn.close()
