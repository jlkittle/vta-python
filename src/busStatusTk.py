from tkinter import *

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
    myTitle, myLabelDepartText, myBusDeparture = myStop.status()

    myForm.title = myTitle
    myLabelDepartVar.set(myLabelDepartText)
    myBusStatusVar.set(myBusDeparture)

    if myStop.destinationStopCode is None:
        print ("No Destination Specified")
        myButtonReverse.Visible = False

    myForm.update_idletasks()

myForm = Tk()
myForm.title("VTA Next Bus")
myForm.geometry("500x200")

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
