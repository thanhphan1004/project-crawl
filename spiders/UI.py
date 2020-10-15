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
    data=[]
    with open(feedback,"r") as f:
        chuoi=f.read()
    chuoi=chuoi.split('\n')
    f.close()
    filename=root+"\input_VIN.txt"
    i=0
    with open(filename,'w') as f:
        for s in chuoi:
            f.write(s)
            i=i+1
            if(i<len(chuoi)):
                f.write('\n')
    f.close()
    VinSpider.run_Vin(VinSpider)
btn=Button(window,text="NHTSA Decode",height=5,width=20,command=clicked)
btn.place(x=200,y=300)

window.mainloop()

