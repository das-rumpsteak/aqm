from measure import single_reading

[pm25,pm10] = single_reading(5,60,1)

print("PM2.5 concentration = " + str(pm25)[0:6] + " μg/m³")
print("PM10 concentration = " + str(pm10)[0:6] + " μg/m³")
