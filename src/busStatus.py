import clr
SWF = clr.AddReference("System.Windows.Forms")
#print (SWF.Location)
import System.Windows.Forms as WinForms
from System.Drawing import Size, Point

import state
myStop = state.Stop()

class App(WinForms.Form):
    def __init__(self):
        self.Text = "VTA Next Bus"
        self.AutoScaleBaseSize = Size(5, 13)
        self.ClientSize = Size(400, 117)
        h = WinForms.SystemInformation.CaptionHeight
        self.MinimumSize = Size(200, (200 + h))

        # Create the 1st button
        self.button = WinForms.Button()
        self.button.Location = Point(32, 140)
        self.button.Size = Size(100, 20)
        self.button.TabIndex = 2
        self.button.Text = "Refresh"
        # Register the event handler
        self.button.Click += self.button_Click

        # Create the 1st button
        self.button2 = WinForms.Button()
        self.button2.Location = Point(232, 140)
        self.button2.Size = Size(100, 20)
        self.button2.TabIndex = 2
        self.button2.Text = "Reverse"
        # Register the event handler
        self.button2.Click += self.button_Click

        self.departCount = WinForms.Label()
        self.departCount.Text = "departure count"
        self.departCount.Size = Size(400, 40)
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
        self.Controls.Add(self.button2)
        self.Controls.Add(self.textbox)
        self.Controls.Add(self.departCount)

    def button_Click(self, sender, args):
        #print (sender)
        if sender.Text == "Reverse":
            if myStop.destinationStopCode == "":
                raise ValueError("Please set the journey.destinationStop property in config.json")
            else:
                myStop.reverse()
        else:
            myStop.refresh(True)

        refresh(self)

    def run(self):
        WinForms.Application.Run(self)

def refresh(form):
    myTitle, myLabelDepartText, myBusDeparture = myStop.status()

    form.Text = myTitle
    form.textbox.Text = myBusDeparture
    form.departCount.Text = myLabelDepartText

    if myStop.destinationStopCode is None:
        print ("No Destination Specified")
        form.button2.Visible = False

def main():
    form = App()
    #print ("form created")
    app = WinForms.Application
    #print ("app referenced")
    refresh(form)
    app.Run(form)

if __name__ == '__main__':
    main()
