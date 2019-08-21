import json
import requests
import os

def loadConfig():
    with open('config.json', 'r') as jsonConfig:
        return json.load(jsonConfig)

config = loadConfig()
# print (config)

def loadDeparturesForStop (apiKey,journeyConfig):
    if journeyConfig["departureStop"] == "":
        raise ValueError(
            "Please set the journey.departureStop property in config.json")

    if apiKey == "":
        raise ValueError(
            "Please complete the 511Api section of your config.json file")

    departureStop = journeyConfig["departureStop"]

    localStop = "data\\" + departureStop + ".json"

    if os.path.exists(localStop):
        print ("using cached stop for " + departureStop)
        with open(localStop, 'r') as f:
            data = json.load(f)
    else:
        URL = f"http://api.511.org/transit/StopMonitoring"

        PARAMS = {'api_key': apiKey,
                  'agency': journeyConfig["agency"],
                  'stopCode': departureStop}

        r = requests.get(url=URL, params=PARAMS, headers={'content-type':'application/json'})
        r.encoding = 'utf-8-sig'
        data = json.loads(r.text)

        if "error" in data:
           raise ValueError(data["error"])
        else:
            with open(localStop, "a") as f:
                json.dump(data,f)

    return data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"], \
           data["ServiceDelivery"]["ResponseTimestamp"]

def loadStop(apiConfig, journeyConfig):
    departures, timestamp = loadDeparturesForStop(apiConfig["apiKey"],journeyConfig)

    if len(departures) == 0:
        return False, False, timestamp

    firstTrip = departures[0]
    name = firstTrip["MonitoredVehicleJourney"]["MonitoredCall"]["StopPointName"]

    return name, departures, timestamp

class Stop():
    def __init__(self):
        self.code = config.get("journey").get("departureStop")
        self.name, departures, self.time = loadStop(config["511Api"], config["journey"])
        self.departures = list()
        for departure in iter(departures):
            self.departures.append(Departure(departure))

class Departure():
    def __init__(self,departure):
        self.route_id = departure["MonitoredVehicleJourney"]["LineRef"]
        self.route_name = departure["MonitoredVehicleJourney"]["PublishedLineName"]
        self.origin_name = departure["MonitoredVehicleJourney"]["OriginName"]
        self.destination_name = departure["MonitoredVehicleJourney"]["DestinationName"]
        self.time = departure["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedDepartureTime"]


