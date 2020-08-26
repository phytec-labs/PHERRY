import re
import urllib.request
import sys
import requests

url = 'https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx?dojo.preventCache' 
try:
        res = requests.get(url)
except:
        print("No internet connection")
        exit()

class Ferry_Sched():
    """
    Ferry_Sched finds the ferry schedule online for a given departing and arriving port and returns them as a dict
    """
    
    def __init__(self, dual_list = False): #departing=7, arriving=3):
        """
        Construct a new "Ferry_Sched" object and initialize.
        """
        
        self.dual_list = dual_list
        self.url = "https://www.wsdot.wa.gov/ferries/schedule/scheduledetail.aspx?departingterm=7&arrivingterm=3&roundtrip=true"
        
    def get_sched(self):
        """
        Using the url provided, grab the website data and parse into a readable ferry schedule,
        Then return to the calling script
        """
        
        # Initialize return string
        qt_data = "Today's Schedule\n"

        # Download raw data from WS DOT
        data = urllib.request.urlopen(self.url).read().decode('utf-8')

        # Extract Date from header
        regex = "Sailing Schedule for ([0-9a-zA-Z ]+)"
        date = re.findall(regex, data)[0]
        qt_data += date + "\n\n"

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
 
            # handles adding destination for BI if 1 vessel, seperator
            second_vessel = False
            if self.dual_list or "Island" in destination:
                if self.dual_list and "Island" in destination:
                    qt_data += "-----\n"
                if "Seattle" in destination:
                    qt_data += destination + "\n"
                if "Island" in destination:
                    qt_data += "Leaving BI\n"
                    second_vessel = True

            if self.dual_list or second_vessel:
                # Split into AM/PM blocks
                meridian_splits = direction.split("colspan=\"3")

                # For each block, determin if AM/PM and extract departure times
                for meridian in meridian_splits:
                    if ">AM<" in meridian:
                        AM_PM = "AM"
                    elif ">PM<" in meridian:
                        AM_PM = "PM"
                    else:
                        continue

                    # Extract departure times and vessel names from given AM/PM Block
                    regex = "([0-9]+:[0-9]+)<"
                    times = re.findall(regex, meridian)
                    
                    regex = "id=[0-9]+\">([a-zA-Z /]+)"
                    vessels = re.findall(regex, meridian)

                    i = 0
                    for time in times:
                        t = time + ' ' + AM_PM + ' ' + vessels[i]
                        qt_data += t + "\n"
                        i += 1
        
        print(qt_data)


## Code for running this module as a standalone test.
if __name__ == '__main__':

    if (len(sys.argv) > 2):
        print("Usage: ./ferry_sched.py [bidirectional]")
        exit(-1)

    if (len(sys.argv) == 2):
        ferry = Ferry_Sched(sys.argv[1])
    else:
        ferry = Ferry_Sched()

    ferry.get_sched()
