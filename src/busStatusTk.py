from tkinter import *

import dateutil.parser
from datetime import datetime, timedelta
from pytz import timezone
pac_tz = timezone('America/Los_Angeles')

import state
myStop = state.Stop()

def RefreshClicked():
    print("Refresh Clicked")

def ReverseClicked():
    print("Reverse Clicked")

def refresh(myForm):
    myForm.Title = "VTA Bus @ " + myStop.name + " (" + myStop.departureStopCode + ")"

    if myStop.destinationStopCode is None:
        print ("No Destination Specified")
        myButtonReverse.Visible = False

    myDepartures = myStop.departures
    if myDepartures:
        myDepartureCount = len(myDepartures)
        myBaseTime = dateutil.parser.parse(myStop.time)
        myBaseTimeLocal = pac_tz.normalize(myBaseTime.astimezone(pac_tz))
        myLabelDepart.Text = str(myDepartureCount) + " buses in range on " + str(myBaseTimeLocal) #.strftime("%A, %B %d, %Y @ %I:%m%p")
        myBusStatus.Text = ""
        for myNextDeparture in iter(myDepartures):
            myNextTime = dateutil.parser.parse(myNextDeparture.time)
            myDelta =  myNextTime - myBaseTime
            myNextBusMinutes =  myDelta.seconds/60
            myNextBusTimeLocal = pac_tz.normalize(myNextTime.astimezone(pac_tz))
            myNextBusStr = myNextDeparture.destination_name + " in " + str(round(myNextBusMinutes)) + " min @ " + str(myNextBusTimeLocal) #.strftime("%I:%m%p")
            myBusStatus.Text =  myBusStatus.Text +"\n " + myNextBusStr
    else:
        myLabelDepart.Text = "0"
        myForm.BusStatus.Text = "No current bus"

myForm = Tk()
myForm.title("VTA Next Bus")
myForm.geometry("350x200")
myLabelDepart = Label(myForm, text="departure count")
myLabelDepart.grid(column=0,row=0)

myBusStatus = Label(myForm, text="bus status")
myBusStatus.grid(column=1,row=1)

myButtonRefresh = Button(myForm, text="Refresh", command=RefreshClicked)
myButtonRefresh.grid(column=1,row=2)

myButtonReverse = Button(myForm, text="Reverse", command=ReverseClicked)
myButtonReverse.grid(column=2,row=2)

refresh(myForm)
myForm.mainloop()
