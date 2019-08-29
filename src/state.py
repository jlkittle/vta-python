import json
import requests
import os
import dateutil.parser
from datetime import datetime, timedelta
from pytz import timezone
pac_tz = timezone('America/Los_Angeles')

def loadConfig():
    with open('config.json', 'r') as jsonConfig:
        return json.load(jsonConfig)

myConfig = loadConfig()
myApiKey = myConfig["511Api"]["apiKey"]

def loadDeparturesForStop (myRefresh, myAgency, myStopCode):
    if myStopCode == "":
        raise ValueError("Please set the journey.departureStop property in config.json")

    if myApiKey == "":
        raise ValueError("Please complete the 511Api section of your config.json file")

    myStopCache = "data\\" + myStopCode + ".json"

    if os.path.exists(myStopCache) and not myRefresh:
        print ("using cached stop for " + myStopCode)
        with open(myStopCache, 'r') as f:
            myResponseJson = json.load(f)
    else:
        URL = f"http://api.511.org/transit/StopMonitoring"

        PARAMS = {'api_key': myApiKey,
                  'agency': myAgency,
                  'stopCode': myStopCode}

        myResponse = requests.get(url=URL, params=PARAMS, headers={'content-type':'application/json'})
        myResponse.encoding = 'utf-8-sig'
        myResponseJson = json.loads(myResponse.text)

        if "error" in myResponseJson:
           raise ValueError(myResponseJson["error"])
        else:
            with open(myStopCache, "w") as f:
                json.dump(myResponseJson,f)

    return myResponseJson["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"], \
           myResponseJson["ServiceDelivery"]["ResponseTimestamp"]

def loadStop(myRefresh,myAgency,myStopCode):
    departures, timestamp = loadDeparturesForStop(myRefresh,myAgency,myStopCode)

    if len(departures) == 0:
        return False, False, timestamp

    name = departures[0]["MonitoredVehicleJourney"]["MonitoredCall"]["StopPointName"]

    return name, departures, timestamp

class Stop():
    def __init__(self):
        self.departureStopCode = myConfig.get("journey").get("departureStop")
        self.agency = myConfig.get("journey").get("agency")
        self.destinationStopCode = myConfig.get("journey").get("destinationStop")
        self.refresh(False)

    def refresh(self,refresh):
        self.name, departures, self.time = loadStop(refresh,self.agency,self.departureStopCode)
        self.departures = list()
        for departure in iter(departures):
            self.departures.append(Departure(departure))

    def status(self):
        myTitle = "VTA Bus @ " + self.name + " (" + self.departureStopCode + ")"

        myDepartures = self.departures
        if myDepartures:
            myDepartureCount = len(myDepartures)
            myBaseTime = dateutil.parser.parse(self.time)
            myBaseTimeLocal = pac_tz.normalize(myBaseTime.astimezone(pac_tz))
            myLabelDepartText = str(myDepartureCount) + " buses in range on " + str(myBaseTimeLocal) #.strftime("%A, %B %d, %Y @ %I:%m%p")

            myBusStatusText = ""
            for myNextDeparture in iter(myDepartures):
                myNextTime = dateutil.parser.parse(myNextDeparture.time)
                myDelta =  myNextTime - myBaseTime
                myNextBusMinutes =  myDelta.seconds/60
                myNextBusTimeLocal = pac_tz.normalize(myNextTime.astimezone(pac_tz))
                myNextBusStr = myNextDeparture.destination_name + " in " + str(round(myNextBusMinutes)) + " min @ " + str(myNextBusTimeLocal) #.strftime("%I:%m%p")
                myBusStatusText =  myBusStatusText +"\n " + myNextBusStr
            myBusStatusText += "\n\n"
        else:
            myLabelDepartText = "0 buses in range"
            myBusStatusText = "No current bus"

        return myTitle, myLabelDepartText, myBusStatusText

    def reverse(self):
        tmpCode = self.departureStopCode
        self.departureStopCode= self.destinationStopCode
        self.destinationStopCode = tmpCode
        self.refresh(True)

class Departure():
    def __init__(self,departure):
        self.route_id = departure["MonitoredVehicleJourney"]["LineRef"]
        self.route_name = departure["MonitoredVehicleJourney"]["PublishedLineName"]
        self.origin_name = departure["MonitoredVehicleJourney"]["OriginName"]
        self.destination_name = departure["MonitoredVehicleJourney"]["DestinationName"]
        self.time = departure["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedDepartureTime"]


