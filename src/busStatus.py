import clr
SWF = clr.AddReference("System.Windows.Forms")
#print (SWF.Location)
import System.Windows.Forms as WinForms
from System.Drawing import Size, Point

import state
myStop = state.Stop()

import dateutil.parser
from datetime import datetime, timedelta
from pytz import timezone
pac_tz = timezone('America/Los_Angeles')

class App(WinForms.Form):
    def __init__(self):
        self.Text = "VTA Next Bus"
        self.AutoScaleBaseSize = Size(5, 13)
        self.ClientSize = Size(400, 117)
        h = WinForms.SystemInformation.CaptionHeight
        self.MinimumSize = Size(200, (200 + h))

        # Create the button
        self.button = WinForms.Button()
        self.button.Location = Point(32, 140)
        self.button.Size = Size(100, 20)
        self.button.TabIndex = 2
        self.button.Text = "Refresh"

        # Register the event handler
        self.button.Click += self.button_Click

        self.departCount = WinForms.Label()
        self.departCount.Text = "departure count"
        self.departCount.Size = Size(200, 40)
        self.departCount.Location = Point(8, 12)

        # Create the text box
        self.textbox = WinForms.Label()
        self.textbox.Text = "bus details should be here"
        self.textbox.TabIndex = 1
        self.textbox.Size = Size(400, 400)
        self.textbox.Location = Point(16, 32)

        # Add the controls to the form
        self.AcceptButton = self.button
        self.Controls.Add(self.button)
        self.Controls.Add(self.textbox)
        self.Controls.Add(self.departCount)

    def button_Click(self, sender, args):
        print ("Click")

        refresh(self)
        #WinForms.MessageBox.Show("Need to Refresh from Server Here.")

    def run(self):
        WinForms.Application.Run(self)

def refresh(form):
    form.Text = "VTA Bus @ " + myStop.name + " (" + myStop.code + ")"
    #print (departures)
    departures = myStop.departures

    if departures:
        departureCount = len(departures)
        form.departCount.Text = str(departureCount) + " buses in range"
        form.textbox.Text = ""
        for nextDeparture in iter(departures):
            nextTime = dateutil.parser.parse(nextDeparture.time)
            delta =  nextTime - dateutil.parser.parse(myStop.time)
            nextBusMinutes =  delta.seconds/60
            pac_dt = pac_tz.normalize(nextTime.astimezone(pac_tz))
            form.textbox.Text = form.textbox.Text +"\n " + nextDeparture.destination_name + " in " + str(round(nextBusMinutes, 0)) + " min @ " + str(pac_dt)
    else:
        form.departCount.Text = "0"
        form.textbox.Text = "No current bus"

def main():
    form = App()
    print ("form created")
    app = WinForms.Application
    print ("app referenced")
    refresh(form)
    app.Run(form)

if __name__ == '__main__':
    main()
