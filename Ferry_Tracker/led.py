import requests
import math
import os
#Tells what route to look for 
ferry_route = 'SEA-BI'

#defining url as link
url = 'https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx?dojo.preventCache'
#pull from the site using requests library function "get"
res = requests.get(url)
#making data into a python dictionary 
wsdot_dict = res.json()
#getting array of dictionaries from 'vessellist' located in the dictionary from wsdot
vessellist_array = wsdot_dict.get("vessellist")
#Checking for service (if ferry is active), then checking for route and then setting ferry_dict = x (remember ferry_dict will be the dictionary for whatever route specified earlier
for x in vessellist_array:
	if x.get('inservice') == 'True': 
		if x.get('route') == ferry_route:
			ferry_dict = x
			break

curr_lat = ferry_dict.get('lat')
curr_lon = ferry_dict.get('lon')

for curr_lat in range(-1000,1000):
	if math.isclose(curr_lat, 47.62241, rel_tol = 0.01):
		if math.isclose(curr_lon, -122.509077, rel_tol = 0.0001): 
			os.system("echo 1 > /sys/class/leds/user-led2/brightness")
		else:
			os.system("echo 0 > /sys/class/leds/user-led2/brightness")
		break
		
				
	
#Translates coordinates to fit imx6ul display

#print the coordinates according to the display as a string
#print(str(curr_lon) + " " +  "," + " " +  str(curr_lat)) 

