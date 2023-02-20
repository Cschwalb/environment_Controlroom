# api for cpp to call sense information
#  By:  Caleb Schwalb
#  6/19/2022
from sense_hat import SenseHat
import time
import csv
from datetime import datetime
import mariadb
import sys

def storeToDB():
    try:
        conn = mariadb.connect(user = "root",
                               password = "toor",
                               host = "localhost",
                               port = 3306,
                               database = "ENVIRONMENT")
    except mariadb.Error as e:
        print(f"error connecting to mariaDB platform {e}")
        sys.exit(1)
    cur = conn.cursor()
    cur.execute("select * from ENVIRONMENT")
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
    runSensorCSVData()