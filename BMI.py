import customtkinter as ctk
from settings  import*
from ctypes import windll, byref, c_int, sizeof

class App(ctk.CTk):
    def __init__(self):


        #window
        super().__init__(fg_color = BACK_GROUNG)
        self.title('')
        self.geometry('400x400')
        self.resizable(False,False)
        self.change_titlebar_color()
        self.iconbitmap("trans_icorn.ico")

        #layout

        self.columnconfigure(0,weight= 1)
        self.rowconfigure((0,1,2,3),weight=1,uniform='a')

        #metric
        self.metric_bool = ctk.BooleanVar(value= True)
     

        #data 
        self.height_int = ctk.IntVar(value= 170)
        self.weight_flote = ctk.DoubleVar(value= 65)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()

        # traceing

        self.height_int.trace_add('write',self.update_bmi)
        self.weight_flote.trace_add('write',self.update_bmi)
        self.metric_bool.trace_add('write', self.change_unit)



       #widgied
        ResultText(self,self.bmi_string)
        self.weight_input = weightInput(self,self.weight_flote, self.metric_bool)
        self.height_input = HightInput(self,self.height_int,self.metric_bool)
        UnitSwicher(self, self.metric_bool)   


        #run
        self.mainloop()

    def change_unit(self, *args):
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()


    def update_bmi(self, *args):
        height_meter = self.height_int.get()/100
        weight_kg = self.weight_flote.get()
        self.bmi_result = round(weight_kg/height_meter **2,1)
        self.bmi_string.set(self.bmi_result)


    def change_titlebar_color(self):
        try: 
            HWND = windll.user32.GetParent(self.winfo_id()) 
            DWMWA_CAPTION_COLOR = 35 
            COLOR = TITLE_HEX_COLOR # e.g. 0x202020 
            windll.dwmapi.DwmSetWindowAttribute( HWND, DWMWA_CAPTION_COLOR, byref(c_int(COLOR)), sizeof(c_int) ) 
        except Exception: 
            pass

class ResultText(ctk.CTkLabel):
     def __init__(self,parent,bmi_string):
         font = ctk.CTkFont(family= FONT,size= MAIN_TEXT_SIZE,weight= 'bold' )
         super().__init__(master= parent,text = 22.5,font= font , text_color= WHITE,textvariable=bmi_string)
         self.grid(column = 0, row = 0, rowspan = 2 , sticky = 'nswe')

class weightInput(ctk.CTkFrame):
    def __init__(self, parent,weight_flote,metric_bool):
        super().__init__(master = parent,fg_color = WHITE,corner_radius= 20)
        self.grid(column = 0, row =2 ,sticky ='news',padx = 10,pady = 10)

        self.weight_flote = weight_flote
        self.metric_bool = metric_bool
        #update
        self.output_string = ctk.StringVar()
        self.update_weight()
    
        #layout\
        self.rowconfigure(0, weight = 1, uniform = 'b')
        self.columnconfigure(0, weight = 2, uniform = 'b')
        self.columnconfigure(1, weight = 1, uniform = 'b')
        self.columnconfigure(2, weight = 3, uniform = 'b')
        self.columnconfigure(3, weight = 1, uniform = 'b')
        self.columnconfigure(4, weight = 2, uniform = 'b')




        #text
        font = ctk. CTkFont(family = FONT, size = INPUT_FONT_SIZE)
        label = ctk. CTkLabel(self, textvariable= self.output_string, text_color = BLACK, font = font)
        label.grid(row = 0, column = 2)

        #buttons
        min_btn = ctk.CTkButton(self, command= lambda: self.update_weight(('minus','larege')) ,text = '-', font = font , text_color= BLACK,corner_radius=  25 , border_color= GRAY,fg_color= LIGHT_GRAY , hover_color= GRAY)
        min_btn.grid(row = 0 ,column = 0, sticky = 'ns', padx = 8, pady = 8,)
        
        plus_btn = ctk.CTkButton(self,  command= lambda: self.update_weight(('plus','larege')) ,text = '+', font = font , text_color= BLACK,corner_radius=  25 , border_color= GRAY,fg_color= LIGHT_GRAY , hover_color= GRAY)
        plus_btn.grid(row = 0 ,column = 4, sticky = 'ns', padx = 8, pady = 8,)
        
        small_min_btn = ctk.CTkButton(self, text = '-', font = font ,  command= lambda: self.update_weight(('minus','small')) ,text_color= BLACK,corner_radius=  10 , border_color= GRAY,fg_color= LIGHT_GRAY , hover_color= GRAY)
        small_min_btn.grid(row = 0 ,column = 1, padx = 8, pady = 4,)
                
        small_plus_btn = ctk.CTkButton(self, text = '+', command= lambda: self.update_weight(('plus','small'))  ,font = font , text_color= BLACK,corner_radius=  10 , border_color= GRAY,fg_color= LIGHT_GRAY , hover_color= GRAY)
        small_plus_btn.grid(row = 0 ,column = 3, padx = 8, pady = 4,)


    def update_weight(self, info = None):
      if info:

        if self.metric_bool.get():
            amount = 1 if info[1] == 'larege' else 0.1
        else:
          amount = 0.453592 if info[1] == 'larege' else 0.453592/16
          
        if info[0] == 'plus':
            self.weight_flote.set(self.weight_flote.get() + amount)
        else:
            self.weight_flote.set(self.weight_flote.get() - amount)


      if self.metric_bool.get():
       self.output_string.set(f'{round(self.weight_flote.get(),1)}kg')
      else:
          raw_ounces = self.weight_flote.get()* 2.20462 * 16
          pounds , ounces = divmod(raw_ounces,16)
          self.output_string.set(f'{int(pounds)}lb {int(ounces)}oz')
               
class HightInput(ctk.CTkFrame):
    def __init__(self, parent,height_int,metric_bool):
        super().__init__(master = parent,fg_color= WHITE,corner_radius= 20,)
        self.grid(row = 3, column = 0 , sticky = 'nsew' , padx = 10 , pady = 10)

        self.metric_bool = metric_bool



        #slider
        slider = ctk.CTkSlider(master=self, button_color= BACK_GROUNG , command = self.update_text,button_hover_color= TITLE_BACK_GROUNG, progress_color= BACK_GROUNG, fg_color= LIGHT_GRAY,variable = height_int,from_=100,to=250)
        slider.pack(side ='left', fill= 'x', pady= 10, padx = 10, expand = True)

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())


        output_text = ctk.CTkLabel(self,textvariable = self.output_string ,text_color= BLACK, font= ctk.CTkFont(family=   FONT,size= INPUT_FONT_SIZE))
        output_text.pack(side = 'left', padx = 20)

    def update_text(self,amount):
     if self.metric_bool.get():
        text_string = str(int(amount))
        meter = text_string[0]
        cm = text_string[1:]
        self.output_string.set(f'{meter}.{cm}m')
     else:
        total_inches = amount / 2.54 
        feet, inches = divmod(total_inches, 12) 
        self.output_string.set(f'{int(feet)}\'{round(inches)}"')


class UnitSwicher(ctk.CTkLabel):
    def __init__(self,parent,metric_bool):
        super().__init__(master = parent, text='metric', text_color= TITLE_BACK_GROUNG,font= ctk.CTkFont(family= FONT, size= SWITCH_FONT_SIZE) , cursor = 'hand2')
        self.place(relx = 0.98, rely = 0.01 , anchor ='ne')

        self.metric_bool = metric_bool
        self.bind('<Button>',self.change_units)

    def change_units(self, event):
        self.metric_bool.set(not self.metric_bool.get())

        if self.metric_bool.get():
            self.configure(text = 'metric')
        else:
            self.configure(text = 'imperial')    


if __name__ == '__main__':
    App()