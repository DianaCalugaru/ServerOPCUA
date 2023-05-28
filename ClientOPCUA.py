from datetime import datetime
import datetime
import pyodbc as pyodbc
from opcua import Client
import time

url = "opc.tcp://169.254.15.16:4840"

client = Client(url)

client.connect()
print("Client Connected")

# Definirea datelor de conectare la baza de date
server = 'DESKTOP-8QAOT1N\SQLEXPRESS'
database = 'IoT'
driver = '{SQL Server}' # driver-ul de conectare

# Conectarea la baza de date
conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
cursor = conn.cursor()


while True:
    led1 = client.get_node("ns=2;i=2")
    Led1 = led1.get_value()
    print(Led1)

    led2 = client.get_node("ns=2;i=3")
    Led2 = led2.get_value()
    print(Led2)

    led3 = client.get_node("ns=2;i=4")
    Led3 = led3.get_value()
    print(Led3)

    led5 = client.get_node("ns=2;i=5")
    Led5 = led5.get_value()
    print(Led5)

    led6 = client.get_node("ns=2;i=6")
    Led6 = led6.get_value()
    print(Led6)

    # modificare pentru tabela Table_LED
    if Led1 == 1:
        led1_state = 'Aprins'
    else:
        led1_state = 'Stins'

    if Led2 == 1:
        led2_state = 'Aprins'
    else:
        led2_state = 'Stins'

    if Led3 == 1:
        led3_state = 'Aprins'
    else:
        led3_state = 'Stins'

    if Led5 == 1:
        led5_state = 'Aprins'
    else:
        led5_state = 'Stins'

    if Led6 == 1:
        led6_state = 'Aprins'
    else:
        led6_state = 'Stins'

    insert_query_led = f"INSERT INTO Table_LED (ID, Nume, Stare, Data) VALUES (1, 'LED1', '{led1_state}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'), (2, 'LED2', '{led2_state}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'), (3, 'LED3', '{led3_state}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'), (4, 'LED5', '{led5_state}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'), (5, 'LED6', '{led6_state}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
    cursor.execute(insert_query_led)

    hum = client.get_node("ns=2;i=9")
    Hum6 = hum.get_value()
    print(Hum6)

    temp = client.get_node("ns=2;i=8")
    Temp = temp.get_value()
    print(Temp)

    insert_query_dht11 = f"INSERT INTO Table_DHT11 (ID, Nume, Valoare, Data) VALUES (1, 'Umiditate', '{Hum6}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'), (2, 'Temperatura', '{Temp}', '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
    cursor.execute(insert_query_dht11)

    time.sleep(2)
    conn.commit()



# Închiderea conexiunii cu baza de date
cursor.close()
conn.close()