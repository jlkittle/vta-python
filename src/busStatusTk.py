from tkinter import *

import dateutil.parser
from datetime import datetime, timedelta
from pytz import timezone
pac_tz = timezone('America/Los_Angeles')

import state
myStop = state.Stop()

def RefreshClicked():
    myStop.refresh(True)
    refresh(myForm)

def ReverseClicked():
    if myStop.destinationStopCode == "":
        raise ValueError("Please set the journey.destinationStop property in config.json")
    else:
        myStop.reverse()
        refresh(myForm)

def refresh(myForm):
    myForm.title ="VTA Bus @ " + myStop.name + " (" + myStop.departureStopCode + ")"

    if myStop.destinationStopCode is None:
        print ("No Destination Specified")
        myButtonReverse.Visible = False

    myDepartures = myStop.departures
    if myDepartures:
        myDepartureCount = len(myDepartures)
        myBaseTime = dateutil.parser.parse(myStop.time)
        myBaseTimeLocal = pac_tz.normalize(myBaseTime.astimezone(pac_tz))
        myLabelDepartText = str(myDepartureCount) + " buses in range on " + str(myBaseTimeLocal) #.strftime("%A, %B %d, %Y @ %I:%m%p")
        myLabelDepartVar.set(myLabelDepartText)

        myBusStatusText = ""
        for myNextDeparture in iter(myDepartures):
            myNextTime = dateutil.parser.parse(myNextDeparture.time)
            myDelta =  myNextTime - myBaseTime
            myNextBusMinutes =  myDelta.seconds/60
            myNextBusTimeLocal = pac_tz.normalize(myNextTime.astimezone(pac_tz))
            myNextBusStr = myNextDeparture.destination_name + " in " + str(round(myNextBusMinutes)) + " min @ " + str(myNextBusTimeLocal) #.strftime("%I:%m%p")
            myBusStatusText =  myBusStatusText +"\n " + myNextBusStr
        myBusStatusText += "\n\n"
        myBusStatusVar.set(myBusStatusText)
    else:
        myLabelDepartVar.set = "0 buses in range"
        myBusStatusVar.set("No current bus")

    myForm.update_idletasks()

myForm = Tk()
myForm.title("VTA Next Bus")
myForm.geometry("400x200")

myLabelDepartVar = StringVar()
myLabelDepartVar.set("departure count")
myLabelDepart = Label(myForm, textvariable=myLabelDepartVar)
myLabelDepart.grid(column=0,row=0)

myBusStatusVar = StringVar()
myBusStatusVar.set("bus status")
myBusStatus = Label(myForm, textvariable=myBusStatusVar)
myBusStatus.grid(column=0,row=1)

myButtonRefresh = Button(myForm, text="Refresh", command=RefreshClicked)
myButtonRefresh.grid(column=0,row=2)

myButtonReverse = Button(myForm, text="Reverse", command=ReverseClicked)
myButtonReverse.grid(column=1,row=2)

refresh(myForm)
myForm.mainloop()
