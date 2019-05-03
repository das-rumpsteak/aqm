#!/usr/bin/python3
import numpy as np
import time, datetime
from config import cnf
import serial, struct

def SensorWake(ser):
	bytes = b'0xAA\xB4\x06\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x06\xAB'
	print("Sensor Wake", datetime.datetime.now())
	ser.write(bytes)
		
def SensorSleep(ser):
	bytes = b'\xAA\xB4\x06\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\x05\xAB'
	print("Sensor Sleep", datetime.datetime.now())
	ser.write(bytes)
'''
def ProcessFrame(d):
	r = struct.unpack('<HHxxBBB', d[2:])
	pm25 = r[0]/10.0
	pm10 = r[1]/10.0
	checksum = sum(v for v in d[2:8])%256 #there's an ord in line 130
	#print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))
	data = [pm25, pm10]
	if (checksum==r[2] and r[3]==0xab):
		return dat
	else:
		return None
'''
def SensorRead(ser):
	while True:
		while ord(ser.read(1)) != int("AA", 16):
			pass
		s = ser.read(9)
		isChecksumGood = ((sum(s[1:7]) & 0b11111111) == s[7])
		#print([i for i in s], isChecksumGood)
		if s[0] == 0xC0 and s[8] == 0xAB and isChecksumGood:
			# We have good data
			pm25= (s[1] + s[2]*256)/10
			pm10= (s[3] + s[4]*256)/10
			print("pm25:", pm25, "pm10:", pm10)
			return [pm25, pm10]

def Measure():
	ser = serial.Serial()
	ser.port = cnf['SerialPortName']
	ser.baudrate = cnf['Baudrate']
	ser.open()
	ser.flushInput()
	
	f = open("/home/pi/Desktop/AQM/alldata.csv", "+a") #change the file location here if you want to save all the data
	
	try:
		pm25data = []
		pm10data = []
		SensorWake(ser)
		time.sleep(cnf['WarmUpTime'])
		for i in range(cnf['NumberOfReadoutsPerPoint']):
			t = time.time()
			d = SensorRead(ser)
			pm25data.append(d[0])
			pm10data.append(d[1])
			f.write("{0:s},{1:f},{2:f}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), d[0], d[1]))
			time.sleep(3)
		print("pm25data", pm25data)
		print("pm10data", pm10data)
		
	except Exception as ex:
		print("Exception", ex)
		pass # TODO Perhaps log an error or something.
	f.close()
	
	try:
		SensorSleep(ser)
	except Exception as ex:
		print("Exception", ex)
		pass # TODO Perhaps log an error or something.

	ser.close()
	if len(pm25data) > 0 and len(pm10data) > 0:
		avg = [np.average(pm25data), np.average(pm10data)]
		stddev = [np.std(pm25data), np.std(pm10data)]
		minimum = [np.min(pm25data), np.min(pm10data)]
		maximum = [np.max(pm25data), np.max(pm10data)]
		return [len(pm25data), len(pm10data)], avg, stddev, minimum, maximum

	
def GetCoordinates():
	return cnf['Latitude'], cnf['Longitude'] # Or actually get the coordinates from a GPS or something.

if __name__ == "__main__":
	ser = serial.Serial()
	ser.port = cnf['SerialPortName']
	ser.baudrate = cnf['Baudrate']
	ser.open()
	ser.flushInput()
	SensorWake(ser)
	time.sleep(10)
	SensorSleep(ser)
	ser.close()
	
