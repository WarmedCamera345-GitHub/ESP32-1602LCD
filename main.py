import time
from machine import Pin,I2C,RTC
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import network
import ntptime
import esp32

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(sda=Pin(22), scl=Pin(21), freq=4000000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect("YOUR_SSID", "YOUR_PASSWORD")
time.sleep(2)
sta_if.isconnected()
lcd.move_to(0, 0)
if sta_if.isconnected():
    lcd.putstr("Connesso alla   rete")
time.sleep(2)
lcd.clear()
    
ntptime.settime() # sincronizzazione con il server NTP

while True:
    rtc = RTC()
    
    data = str(time.gmtime()) # leggi la data
    year, month, day, _, hour, minute, second, _ = rtc.datetime()  # Leggi i componenti della data e dell'ora
    
    formatted_date = "{:02d}/{:02d}/{:02d}".format(day, month, year)  # Formatta la data come "dd/mm/aa"
    lcd.move_to(0, 0)
    lcd.putstr(formatted_date)
    
    formatted_time = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)  # Formatta l'ora come "hh:mm:ss"
    lcd.move_to(0, 1)
    lcd.putstr(formatted_time)
    
    formatted_datetime = "{}  {}".format(formatted_date, formatted_time)  # Combina data e ora nel formato desiderato
    print(formatted_datetime)
    
    temperature = esp32.raw_temperature()
    temperature_celsius = (temperature - 32) / 1.8
    print("Temperature:", temperature_celsius, "°C")
    
    time.sleep(1)
