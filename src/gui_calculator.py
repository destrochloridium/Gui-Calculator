from tkinter import *
from PIL import ImageTk,Image
import random

class Root(Tk):
    def __init__(self,item_image_dict,background_image_dict):
        super().__init__()
         
        self.calculate_value=""
        self.show_value=""
        self.result=""
        self.cursor_state="hidden"
        self.x,self.y=100,500
        self.texts=("C","(",")","÷",
              "7","8","9","×",
              "4","5","6","-",
              "1","2","3","+",
              "•","0","","=")
        
        self.canvas=Canvas(height=1280,width=720,bg="black")
        self.canvas.place(x=0,y=0)
         
        self.background_image_list=[]
        for i in background_image_dict:
            self.img=ImageTk.PhotoImage(background_image_dict[i])
            self.background_image_list.append(self.img)
        
        self.transparant_background_image=ImageTk.PhotoImage(item_image_dict["transparant_background"])
        self.canvas.create_image(0,0,image=random.choice(self.background_image_list),anchor=NW)
        self.canvas.create_image(0,0,image=self.transparant_background_image,anchor=NW)
        self.delete_image=ImageTk.PhotoImage(item_image_dict["delete_icon"]) 
        self.delete_button=self.canvas.create_image(390,1120,image=self.delete_image,anchor=NW)
        self.canvas.tag_bind(self.delete_button,"<Button->",lambda x:self.calculate("d"))
        
        self.cursor=self.canvas.create_text(70,85,text="|",fill="white",font=("Roboto Light",15),state=self.cursor_state,anchor=NW)
        self.cursor_animation()
        self.label=self.canvas.create_text(80,90,text="",fill="white",font=("Roboto Light",15),anchor=NW)
        self.error_text_1=self.canvas.create_text(150,410,text="Invalid Format Used !",state="hidden",fill="black",font=("Roboto Light",10),anchor=NW)
        self.error_text_2=self.canvas.create_text(80,375,text="Maximum Number of Characters\n(50) Has Been Reached !",state="hidden",fill="black",font=("Roboto Light",9),anchor=NW)
        
        for i in range(1,21):
            self.buttons=self.canvas.create_text(self.x,self.y,text=self.texts[i-1],font=("Roboto Black",18),fill=self._from_rgb((54,54,54)),anchor=NW)
            self.canvas.tag_bind(self.buttons,"<Button->",lambda x,i=i:self.calculate(self.texts[i-1]))
            self.x+=150
            if i==4 or i==8 or i==12 or i==16:
                self.x=100
                self.y+=150
                
        self.bind("<KeyPress>",self.key_input_check)
                
    def calculate(self,number):
        if len(self.show_value)==15 or len(self.show_value)==31 or len(self.show_value)==47:
             self.show_value+="\n"
        if number=="=":
            self.show_result()
        elif number=="C":
            self.result=""
            self.calculate_value=""
            self.show_value=""
            self.canvas.itemconfig(self.label,text=self.show_value)
        elif number=="d":
            if len(self.show_value)==16 or len(self.show_value)==32 or len(self.show_value)==48:
                self.calculate_value=self.calculate_value[:-2]
                self.show_value=self.show_value[:-2]
                self.canvas.itemconfig(self.label,text=self.show_value)
            else:
                self.calculate_value=self.calculate_value[:-1]
                self.show_value=self.show_value[:-1]
                self.canvas.itemconfig(self.label,text=self.show_value)
        if len(self.show_value)<53:
            if number=="÷":
                self.calculate_value+="/"
                self.show_value+="÷"
                self.canvas.itemconfig(self.label,text=self.show_value)
            elif number=="×":
                self.calculate_value+="*"
                self.show_value+="×"
                self.canvas.itemconfig(self.label,text=self.show_value)
            elif number=="•":
                self.calculate_value+="."
                self.show_value+="."
                self.canvas.itemconfig(self.label,text=self.show_value)
            elif number in list(("C","d","=")):
                pass
            else:
                self.calculate_value+=str(number)
                self.show_value+=str(number)
                self.canvas.itemconfig(self.label,text=self.show_value)
        else:
            self.canvas.itemconfig(self.error_text_2,state="normal")
            self.after(2000,lambda :self.canvas.itemconfig(
            self.error_text_2,state="hidden"))
            
            
    def show_result(self):
         try:
            self.result=eval(str(self.calculate_value))
            if self.result>999999999999999:
                self.result="{:.2E}".format(self.result)
            if isinstance(self.result, float)==True:
                if len(str(int(self.result)))>9:
                    self.result=round(self.result,1)
                else:
                    self.result=round(self.result,5)
            if str(self.result)[-2:len(str(self.result))]==".0":
                self.result=int(self.result)
            self.canvas.itemconfig(self.label,text=self.result)
         except:
            self.result="error"
            self.canvas.itemconfig(self.error_text_1,state="normal")
            self.after(2000,lambda :self.canvas.itemconfig(
             self.error_text_1,state="hidden"))
         self.calculate_value=""
         self.show_value="" 
     
    def cursor_animation(self):
        if self.result=="" and self.show_value=="":
            if self.cursor_state=="normal":
                self.cursor_state="hidden"
                self.canvas.itemconfig(
                self.cursor,state=self.cursor_state)
            elif self.cursor_state=="hidden":
                self.cursor_state="normal"
                self.canvas.itemconfig(
                self.cursor,state=self.cursor_state)
        else:
            self.cursor_state="hidden"
            self.canvas.itemconfig(
            self.cursor,state=self.cursor_state)
        self.after(500,self.cursor_animation)
        
    def _from_rgb(self,rgb):
        return "#%02x%02x%02x" % rgb
        
    def key_input_check(self,event):
        self.char=""
        if event.keysym=="equal" or event.keysym=="Enter" or event.keysym=="Return":
            self.char="="
        elif event.keysym=="plus":
            self.char="+"
        elif event.keysym=="minus":
            self.char="-"
        elif event.keysym=="times" or event.keysym=="multiply" or event.keysym=="Asterisk":
            self.char="×"
        elif event.keysym=="division" or event.keysym=="divided by":
            self.char="÷"
        elif event.keysym=="period":
            self.char="."
        elif event.keysym=="Delete" or event.keysym=="BackSpace":
            self.char="d"
        elif event.keysym=="c" or event.keysym=="C" or event.keysym=="Clear":
            self.char="C"
        elif event.keysym=="Open Parenthesis" or event.keysym=="Open_Parenthesis":
            self.char="("
        elif event.keysym=="Close Parenthesis" or event.keysym=="Close_Parenthesis":
            self.char=")"
        elif event.keysym in list(("1,2,3,4,5,6,7,8,9,0")):
            self.char=event.keysym
            
        self.calculate(self.char)
        
def start(item_image_dict,background_image_dict):
    root=Root(item_image_dict,background_image_dict)
    icon=ImageTk.PhotoImage(item_image_dict["icon"])
    root.call("wm", "iconphoto", root._w, icon)
    root.tk_setPalette("black")
    root_width = 720
    root_height = 1280
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - root_width / 2)
    center_y = int(screen_height/2 - root_height / 2)
    root.geometry(f"{root_width}x{root_height}+{center_x}+{center_y}")
    root.resizable(False,False)
    root.mainloop()