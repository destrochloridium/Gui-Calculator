from tkinter import *
from PIL import ImageTk,Image
from urllib.request import*
import json
from io import BytesIO

class Root(Tk):
    def __init__(self):
        super().__init__()
        
        with open('data.json','+r') as text:
            self.data=json.load(text)
        self.items=self.data["items"]
        self.backgrounds=self.data["backgrounds"]
        self.light_buttons=self.data["light_buttons"]
        self.dark_buttons=self.data["dark_buttons"]
        
        self.font_size=round(2520/self.winfo_fpixels('1i'))
        self.font="Roboto {}".format(self.font_size)
        self.mode="dark"
        if self.mode=="dark":self.background_color,self.text_color=_from_rgb((26,26,26)),_from_rgb((229,229,229))
        elif self.mode=="light":self.background_color,self.text_color=_from_rgb((229,229,229)),_from_rgb((26,26,26))
        self.calculate_value,self.show_value,self.result,self.cursor_state="","","","hidden"
        self.x,self.y,self.n=1,126,0
        self.background_animation_count=0
        self.button_list=[]
        
        self.content={"C":"C","open_parenthesis":"(","close_parenthesis":")","division":"÷","seven":"7","eight":"8","nine":"9","multiply":"×","four":"4","five":"5","six":"6","minus":"-","one":"1","two":"2","three":"3","plus":"+","period":"•","zero":"0","delete":"d","equal":"=","empty":"","right_corner":"","left_corner":""}
        self.place_list=["left_corner","empty","empty","empty","empty","empty","empty","empty","right_corner","empty","C","empty","open_parenthesis","empty","close_parenthesis","empty","division","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","seven","empty","eight","empty","nine","empty","multiply","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","four","empty","five","empty","six","empty","minus","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","one","empty","two","empty","three","empty","plus","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","period","empty","zero","empty","delete","empty","equal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty"]
        
        self.canvas=Canvas(height=400,width=225,bg=_from_rgb((24,31,50)))
        self.canvas.place(x=-1,y=-1)
        
        self.item_image_dict={}
        self.background_image_dict={}
        self.light_button_image_dict={}
        self.dark_button_image_dict={}
        data_to_img(self.items,self.item_image_dict)
        data_to_img(self.backgrounds,self.background_image_dict)
        data_to_img(self.light_buttons,self.light_button_image_dict)
        data_to_img(self.dark_buttons,self.dark_button_image_dict)
            
        self.background_image=self.canvas.create_image(0,150,image="",anchor=NW)
        self.background_animation()
            
        self.cursor=Label(text="|",bg=_from_rgb((24,31,50)),font=self.font)
        self.cursor.place(x=5,y=30)
        self.cursor_animation()
        self.label=Label(text="",justify=LEFT,bg=_from_rgb((24,31,50)),font=self.font)
        self.label.place(x=5,y=30)
        
        self.frame=Frame(relief='raised',bg=self.background_color,bd=0,highlightthickness=0)
        self.frame.place(x=-1,y=-1,width=226,height=30)
        self.x_button=Button(image=self.item_image_dict["close"],bg=self.background_color,fg=self.text_color,activebackground=self.background_color,bd=0,highlightthickness=0,font=self.font,command=self.destroy)
        self.x_button.place(x=196,y=-1,width=30,height=30)
        self.tire_button=Button(image=self.item_image_dict["dark"],bg=self.background_color,fg=self.text_color,activebackground=self.background_color,bd=0,highlightthickness=0,command=self.update_mode,font=self.font)
        self.tire_button.place(x=160,y=-1,width=30,height=30)
        self.title_label=Label(text="Gui Calculator",bg=self.background_color,fg=self.text_color,font=("Roboto",int(self.font_size/2)),bd=0)
        self.title_label.place(x=2,y=-1,height=30)
        
        for i in self.place_list:
            if self.mode=="light":
                self.button=self.canvas.create_image(self.x,self.y,image=self.light_button_image_dict[i],anchor=NW)
            elif self.mode=="dark":
                self.button=self.canvas.create_image(self.x,self.y,image=self.dark_button_image_dict[i],anchor=NW)
            self.button_list.append(self.button)
            self.canvas.tag_bind(self.button,"<Button->",lambda x,i=i:self.calculate(self.content[i]))
            self.x+=25
            self.n+=1
            if int(str(self.n/9)[-1])==0:
                self.y+=25
                self.x=1
                
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
            if self.show_value=="":
                self.result=""
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
            
    def update_mode(self):
        self.c=0
        if self.mode=="light":
            self.background_color,self.text_color=_from_rgb((26,26,26)),_from_rgb((229,229,229))
            self.frame["bg"]=self.background_color
            self.x_button["bg"]=self.background_color
            self.tire_button["bg"]=self.background_color
            self.tire_button["image"]=self.item_image_dict["dark"]
            self.title_label["bg"]=self.background_color
            self.x_button["activebackground"]=self.background_color
            self.tire_button["activebackground"]=self.background_color
            self.title_label["fg"]=self.text_color
            for x in self.place_list:
                self.canvas.itemconfig(self.button_list[self.c],image=self.dark_button_image_dict[x])
                self.c+=1
            self.mode="dark"
        elif self.mode=="dark":
            self.background_color,self.text_color=_from_rgb((229,229,229)),_from_rgb((26,26,26))
            self.frame["bg"]=self.background_color
            self.x_button["bg"]=self.background_color
            self.tire_button["bg"]=self.background_color
            self.tire_button["image"]=self.item_image_dict["light"]
            self.title_label["bg"]=self.background_color
            self.x_button["activebackground"]=self.background_color
            self.tire_button["activebackground"]=self.background_color
            self.title_label["fg"]=self.text_color
            for x in self.place_list:
                self.canvas.itemconfig(self.button_list[self.c],image=self.light_button_image_dict[x])
                self.c+=1
            self.mode="light"
        
    def cursor_animation(self):
        if self.result=="" and self.show_value=="":
            if self.cursor_state=="normal":
                self.cursor_state="hidden"
                self.cursor.place_forget()
            elif self.cursor_state=="hidden":
                self.cursor_state="normal"
                self.cursor.place(x=5,y=30)
        else:
            self.cursor_state="hidden"
            self.cursor.place_forget()
        self.after(500,self.cursor_animation)
        
    def background_animation(self):
        self.canvas.itemconfig(self.background_image,image=self.background_image_dict["{}".format(self.background_animation_count)])
        self.background_animation_count+=1
        if self.background_animation_count==2:#71
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
    
def get_pos(event):
    xwin = root.winfo_x()
    ywin = root.winfo_y()
    startx = event.x_root
    starty = event.y_root
    ywin = ywin - starty
    xwin = xwin - startx
    def move_window(event):
        root.config(cursor="fleur")
        root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')
    def release_window(event):
        root.config(cursor="arrow")
        
    root.bind('<B1-Motion>', move_window)
    root.bind('<ButtonRelease-1>', release_window)
    
def data_to_img(from_dict,to_dict):
    for i in from_dict:
        with urlopen(from_dict[i]) as response:
            datam = response.read()
        stream = BytesIO(datam)
        image = Image.open(stream).convert("RGBA")
        stream.close()
        image=ImageTk.PhotoImage(image)
        to_dict[i]=image
    return to_dict
        
        
if __name__=="__main__":
    root=Root()
    root.overrideredirect(True)
    root.bind('<Button-1>', get_pos)
    root.title("Gui Calculator")
    root.tk_setPalette(_from_rgb((24,31,50)))
    root_width = 225
    root_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - root_width / 2)
    center_y = int(screen_height/2 - root_height / 2)
    root.geometry(f"{root_width}x{root_height}+{center_x}+{center_y}")
    root.resizable(False,False)
    root.mainloop()