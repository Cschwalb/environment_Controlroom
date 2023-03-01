# api for cpp to call sense information
#  By:  Caleb Schwalb
#  6/19/2022
#  Updated 2/20/2023 for database activity with mariadb
from sense_hat import SenseHat
import time
import csv
from datetime import datetime
import mariadb
import sys

def storeToDB():
    try:
        conn = mariadb.connect(user = "root",
                               password = "",
                               host = "localhost",
                               port = 3306,
                               database = "data")
    except mariadb.Error as e:
        print(f"error connecting to mariaDB platform {e}")
        sys.exit(1)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO ENVIRONMENT VALUES(?,?,?,CURRENT_TIME)", (getTemp(), getPressure(), getHumidity()))
    except mariadb.Error as e:
        print(f"Error:{e}")

    conn.commit()

    conn.close()

def GetInfoAndStore():
    Sensor = SenseHat()
    humidity = Sensor.humidity
    temp = Sensor.temp
    TemperatureC = temp / 2.5 + 16
    tempF = TemperatureC * (9/5) + 32
    pressure = Sensor.pressure
    if tempF == 60.8 or humidity == 0 or pressure == 0:
        print(f"Had to restart getInfoAndStore!")
        GetInfoAndStore()

    try:
        conn = mariadb.connect(user = "root",
                                password = "",
                                host = "localhost",
                                port = 3306,
                                database = "data")
    except mariadb.Error as e:
        print(f"error connecting to mariaDB platform {e}")
        sys.exit(1)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO ENVIRONMENT VALUES (?,?,?,CURRENT_TIME)", (tempF, pressure, humidity))
    except mariadb.Error as e:
        print(f"error:{e}")

    conn.commit()
    conn.close()


def getHumidity():
    humiditySensor = SenseHat()
    humidity = humiditySensor.humidity
    return humidity

def getTemp():
    sense = SenseHat()
    temperature = sense.temp
    temperatureC = temperature / 2.5 + 16
    temperatureF = temperatureC * (9/5) + 32 # farenheit temperature
    return temperatureF


def getPressure():
    sense = SenseHat()
    pressure = sense.pressure
    return pressure


def runSensorCSVData():
    dateTimeObj = datetime.microsecond
    fileName = "/home/pi/Warehouse/Sense_data.csv"
    file = open(fileName, 'w+')
    temperature = getTemp()
    pressure = getPressure()
    humidity = getHumidity()
    stringToWrite = str(round(temperature, 2)) + "," + str(round(humidity, 2)) + "," + str(round(pressure, 2)) + "\r\n"
    file.write(stringToWrite)
    file.close()


if __name__ == '__main__':
    GetInfoAndStore()
