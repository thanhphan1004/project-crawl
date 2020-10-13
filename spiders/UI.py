import os
from tkinter import *
from Collect_vin import *
from tkinter.filedialog import *
root=os.getcwd()
window = Tk()
window.title("VIN's Aggregator")
window.geometry('1000x400')
lbl=Label(window,text="Hello",font=("Arial Bold",50))
lbl.grid(column=0,row=0)
def clicked():
    feedback= askopenfilename()
    pathOld=feedback.find
    os.rename=()
    print(type(feedback))
    VinSpider.run_Vin(VinSpider)
btn=Button(window,text="NHTSA Decode",height=5,width=20,command=clicked)
btn.place(x=200,y=300)

window.mainloop()

