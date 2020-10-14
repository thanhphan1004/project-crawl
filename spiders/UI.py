import os
import shutil
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
    pathOld=feedback.rfind("/")
    path=feedback[0:(int(pathOld)+1)]
    Oldname=feedback[(int(pathOld)+1):int(len(feedback))]    
    os.listdir(path)
    newName="input_VIN.txt"
    os.rename=(path+Oldname,path+newName)
    print(feedback)
    print(newName)
    #VinSpider.run_Vin(VinSpider)
btn=Button(window,text="NHTSA Decode",height=5,width=20,command=clicked)
btn.place(x=200,y=300)

window.mainloop()

