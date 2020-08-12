import requests
import math

ferry_route = 'SEA-BI'

#defining url as link
url = 'https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx?dojo.preventCache'
#pull from the site
res = requests.get(url)
#making data into a python dictionary
wsdot_dict = res.json()
# array of dictionaries from 'vessellist'
vessellist_array = wsdot_dict.get("vessellist")

#Checking for service, then checking for route and then setting ferry_dict = x
for x in vessellist_array:
	if x.get('inservice') == 'True': 
		if x.get('route') == ferry_route:
			ferry_dict = x
			break
#Translates coordinates to fit imx6ul display
curr_lat = ferry_dict.get('lat')
curr_lon = ferry_dict.get('lon')
#curr_lat = ferry_dict.get('lat')*0.387174065
#curr_lon = ferry_dict.get('lon')*(-1.49402326)
#print the coordinates according to the display
#print(str(curr_lon) +  "," + str(curr_lat)) 

max_lat = 47.66388
max_lon = 122.603672

lat_factor = 3218.182
lon_factor = 1660.58806

px_lat = math.floor((max_lat - curr_lat)*lat_factor)
px_lon = math.floor((max_lon + curr_lon)*lon_factor)

print(str(px_lon) +  "," + str(px_lat))
