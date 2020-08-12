import re
import urllib.request

# Seattle = term 7
# BI = term 3
# Bremerton = term 4

# Edmonds = 8
# Kingston = 12

departing = "7"
arriving = "3"

# Download raw data from WS DOT
url = "https://www.wsdot.wa.gov/ferries/schedule/scheduledetail.aspx?departingterm=" + departing + "&arrivingterm=" + arriving + "&roundtrip=true"
data = urllib.request.urlopen(url).read().decode('utf-8')

# Extract Date from header
regex = "Sailing Schedule for [0-9a-zA-Z, ]+"
date = re.findall(regex, data)[0]
#print(date)
qt_data = { "date": date }

# Split data into directional sets: Leaving Seattle[1], Leaving BI[2] 
direction_splits = data.split("line-height: 12px;\">")

# For each direction, split data into AM/PM blocks, then extract departure times
for direction in direction_splits:
    # Skip the [0] section that contains no relevant info
    if not "schedgrid\"" in direction:
        continue
    
    # Find out if it is the Seattle or BI crossing
    regex = "Leaving [a-zA-Z ]+"
    destination = re.findall(regex, direction)[0]
    #print(destination)
    if "destination" in qt_data:
        qt_data["destination2"] = destination
    else:
        qt_data["destination"] = destination

    # Possibly create data entry point here to include all AM/PM blocks?

    # Split into AM/PM blocks
    meridian_splits = direction.split("colspan=\"3")

    second_vessel = False
    if "time_list" in qt_data:
        second_vessel = True
    # For each block, determin if AM/PM and extract departure times
    for meridian in meridian_splits:
        if ">AM<" in meridian:
            AM_PM = "AM"
        elif ">PM<" in meridian:
            AM_PM = "PM"
        else:
            continue
        #print(AM_PM)

        # Extract departure times and vessel names from given AM/PM Block
        regex = "([0-9]+:[0-9]+)"
        times = re.findall(regex, meridian)
        
        regex = "id=[0-9]+\">([a-zA-Z /]+)"
        vessels = re.findall(regex, meridian)
        #print(vessels)

        i = 0
        for time in times:
            t = time + ' ' + AM_PM + ' ' + vessels[i]
            #print(t)
            if second_vessel:
                if "time_list2" in qt_data:
                    qt_data["time_list2"].append(t)
                else:
                    qt_data["time_list2"] = [t]
   #print(marker) 
            elif "time_list" in qt_data:
                qt_data["time_list"].append(t)
            else:
                qt_data["time_list"] = [t]
            i += 1

for x, y in qt_data.items():
    print(x, y)
    #print(marker)
