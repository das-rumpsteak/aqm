#!/usr/bin/python3
cnf = {
	"SerialPortName":		"/dev/ttyUSB0",
	"Baudrate":			9600,
	"DeviceName":			"XXXX",
	"Password":			"YYYY",
	"ServerName":			"pollution.msamani.ca",
	"ServerReceiveLocation":	"/ReceiveData.php",
	"Latitude":			+43.0,	# degrees https://www.findlatitudeandlongitude.com/
	"Longitude":			-79.0,	# degrees
	"MeasurementInterval":		3600,	# seconds time between measurements
	"WarmUpTime":			120,
	"NumberOfReadoutsPerPoint":	20,
	"LocalDataFileName":		"./data.csv",
	"SendDataToServerInterval":	7200,	# seconds
	"QuantityIDs":			[1,2]
}

