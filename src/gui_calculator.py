from tkinter import *
from PIL import ImageTk,Image
import random

class Root(Tk):
    def __init__(self):
        super().__init__()
         
        self.calculate_value,self.show_value,self.result,self.cursor_state="","","","hidden"
        self.x,self.y,self.n=0,125,0
        self.background_image_list,self.background_animation_count,self.button_image_dict=[],0,{}
        self.content={"C":"C","open_parenthesis":"(","close_parenthesis":")","division":"÷","seven":"7","eight":"8","nine":"9","multiply":"×","four":"4","five":"5","six":"6","minus":"-","one":"1","two":"2","three":"3","plus":"+","period":"•","zero":"0","delete":"d","equal":"=","empty":"","right_corner":"","left_corner":""}
        self.place_list=["left_corner","empty","empty","empty","empty","empty","empty","empty","right_corner","empty","C","empty","open_parenthesis","empty","close_parenthesis","empty","division","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","seven","empty","eight","empty","nine","empty","multiply","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","four","empty","five","empty","six","empty","minus","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","one","empty","two","empty","three","empty","plus","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","period","empty","zero","empty","delete","empty","equal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty"]
        
        self.canvas=Canvas(height=400,width=225,bg=_from_rgb((128,128,128)))
        self.canvas.place(x=0,y=0)
        
        for i in range(72):
            self.image=ImageTk.PhotoImage(file="docs/images/backgrounds/background_{}.jpg".format(i))
            self.background_image_list.append(self.image)
            
        self.background_image=self.canvas.create_image(0,150,image="",anchor=NW)
        self.background_animation()
        
        for i in self.content:
            self.image=Image.open("docs/images/buttons/{}.png".format(i))
            self.image=ImageTk.PhotoImage(self.image)
            self.button_image_dict[i]=self.image
            
        self.cursor=Label(text="|",fg=_from_rgb((26,26,26)),bg=_from_rgb((128,128,128)))
        self.cursor.place(x=5,y=5)
        self.cursor_animation()
        self.label=Label(text="",justify=LEFT,fg=_from_rgb((26,26,26)),bg=_from_rgb((128,128,128)))
        self.label.place(x=5,y=5)
        
        for i in self.place_list:
            self.button=self.canvas.create_image(self.x,self.y,image=self.button_image_dict[i],anchor=NW)
            self.canvas.tag_bind(self.button,"<Button->",lambda x,i=i:self.calculate(self.content[i]))
            self.x+=25
            self.n+=1
            if int(str(self.n/9)[-1])==0:
                self.y+=25
                self.x=0
                
        self.bind("<KeyPress>",self.key_input_check)
                
    def calculate(self,number):
        if len(self.show_value)==10:
             self.show_value+="\n"
        if number=="=":
            self.show_result()
        elif number=="C":
            self.result=""
            self.calculate_value=""
            self.show_value=""
            self.label["text"]=self.show_value
        elif number=="d":
            if len(self.show_value)==11:
                self.calculate_value=self.calculate_value[:-2]
                self.show_value=self.show_value[:-2]
                self.label["text"]=self.show_value
            else:
                self.calculate_value=self.calculate_value[:-1]
                self.show_value=self.show_value[:-1]
                self.label["text"]=self.show_value
        if len(self.show_value)<21:
            if number=="÷":
                self.calculate_value+="/"
                self.show_value+="÷"
                self.label["text"]=self.show_value
            elif number=="×":
                self.calculate_value+="*"
                self.show_value+="×"
                self.label["text"]=self.show_value
            elif number=="•":
                self.calculate_value+="."
                self.show_value+="."
                self.label["text"]=self.show_value
            elif number in list(("C","d","=")):
                pass
            else:
                self.calculate_value+=str(number)
                self.show_value+=str(number)
                self.label["text"]=self.show_value
        else:
            self.label["text"]="Max Input\nReached !"
            self.after(2000,lambda :self.label.config(text=self.show_value))
            
    def show_result(self):
         try:
            self.result=eval(str(self.calculate_value))
            if self.result>999999999:
                self.result="{:.2E}".format(self.result)
            if isinstance(self.result, float)==True:
                if len(str(int(self.result)))>6:
                    self.result=round(self.result,1)
                else:
                    self.result=round(self.result,3)
            if str(self.result)[-2:len(str(self.result))]==".0":
                self.result=int(self.result)
            self.label["text"]=self.result
            self.calculate_value=""
            self.show_value=""
         except:
            self.result="error"
            self.label["text"]="Input Error !"
            self.after(2000,lambda :self.label.config(text=self.show_value))
     
    def cursor_animation(self):
        if self.result=="" and self.show_value=="":
            if self.cursor_state=="normal":
                self.cursor_state="hidden"
                self.cursor.place_forget()
            elif self.cursor_state=="hidden":
                self.cursor_state="normal"
                self.cursor.place(x=5,y=5)
        else:
            self.cursor_state="hidden"
            self.cursor.place_forget()
        self.after(500,self.cursor_animation)
        
    def background_animation(self):
        self.canvas.itemconfig(self.background_image,image=self.background_image_list[self.background_animation_count])
        self.background_animation_count+=1
        if self.background_animation_count==71:
            self.background_animation_count=0
        self.after(100,self.background_animation)
        
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
        
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb
        
def start():
    root=Root()
    icon=ImageTk.PhotoImage(file="docs/images/icon.png")
    root.call("wm", "iconphoto", root._w, icon)
    root.title("Gui Calculator")
    root.tk_setPalette(_from_rgb((128,128,128)))
    root_width = 225
    root_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - root_width / 2)
    center_y = int(screen_height/2 - root_height / 2)
    root.geometry(f"{root_width}x{root_height}+{center_x}+{center_y}")
    root.resizable(False,False)
    root.mainloop()