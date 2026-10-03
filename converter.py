import tkinter as tk
from tkinter import ttk


#convert
def convert():
    mile_input = entry_int.get()
    km_output = mile_input * 1.61
    # print(entry_int.get())
    output_string.set(km_output)

#windon
window = tk.Tk()
window.title('Converter')
window.geometry('300x150')

#title 
title_label = ttk.Label(master= window,text='miles to kilmeters', font= 'Calibri 24 bold')
title_label.pack() 

# input filed
input_frame = ttk.Frame(master= window)
entry_int = tk.IntVar()
entry = ttk.Entry(master= input_frame, textvariable= entry_int)
button =ttk.Button(master= input_frame,text="convert",command= convert)

# position
entry.pack(side= 'left',padx= 10)
button.pack(side= 'left')
input_frame.pack(pady= 10)

#out put
output_string = tk.StringVar()
output_laber = ttk.Label(master= window , 
                         text= "Output",
                         font= 'Calibri 24',
                         textvariable= output_string)
output_laber.pack(pady= 5)

#run
window.mainloop()

