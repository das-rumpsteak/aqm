#!/usr/bin/python3
import time, datetime
from pathlib import Path
from config import cnf
from measure import Measure, GetCoordinates
import json
import http.client

def SendDataToServer():
	print("Sending data to the server:")
	arr = []
	with open(cnf['LocalDataFileName'], 'r') as f:
		for line in f:
			arr.append(line.split(','))

	transferred_rows_count = 0
	try:
		json_data = json.dumps({"device_name": cnf['DeviceName'], "password": cnf['Password'], "data": arr})
		connection = http.client.HTTPSConnection(cnf['ServerName'])
		headers = {'Content-type': 'application/json'}
		connection.request('POST', cnf['ServerReceiveLocation'], json_data, headers)
		response = connection.getresponse()
		transferred_rows_count = int(response.read())
	except Exception as e:
		print("Error during data transfer:", e)
	
	if transferred_rows_count == len(arr):
		# Delete the contents of the file.
		with open(cnf['LocalDataFileName'], 'w') as f:
			pass
		print("{0:d} rows were transferred.".format(transferred_rows_count), datetime.datetime.now())
		
if __name__ == "__main__":
	last_server_submit_time = 0
	while True:
		# Collect new data
		start_time = time.time()
		count, avg, stddev, minimum, maximum = Measure()
		end_time = time.time()
		duration = end_time - start_time
		latitude, longitude = GetCoordinates()
		pm25data = [cnf['QuantityIDs'][0], end_time, duration, latitude, longitude, count[0], avg[0], stddev[0], minimum[0], maximum[0]]
		pm10data = [cnf['QuantityIDs'][1], end_time, duration, latitude, longitude, count[1], avg[1], stddev[1], minimum[1], maximum[1]]

		# Store data in the data file
		with open(cnf['LocalDataFileName'], 'a') as f:
			f.write(','.join(str(e) for e in pm25data)+'\n')
			f.write(','.join(str(e) for e in pm10data)+'\n')
	
		# Send data to the server
		if time.time() - last_server_submit_time > cnf['SendDataToServerInterval']:
			SendDataToServer()
			last_server_submit_time = time.time()
	
		if time.time() - start_time < cnf['MeasurementInterval']:
			time.sleep(cnf['MeasurementInterval'] - time.time() + start_time)

