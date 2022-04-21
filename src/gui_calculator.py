from tkinter import *
from PIL import ImageTk,Image
from urllib.request import*
import json
from io import BytesIO
from configparser import ConfigParser

class Root(Tk):
    def __init__(self):
        super().__init__()
        
        self.load_default_vars()
        self.set_vars()
        self.create_widgets()
        
        self.bind('<Button-1>', self.get_pos)
        self.bind("<KeyPress>",self.keyboard_input_check)
        
    def load_default_vars(self):
        with open('docs/data.json','+r') as text:
            self.data=json.load(text)
        self.items,self.backgrounds,self.light_buttons,self.dark_buttons=self.data["items"],self.data["backgrounds"],self.data["light_buttons"],self.data["dark_buttons"]
        self.item_image_dict,self.background_image_dict,self.light_button_image_dict,self.dark_button_image_dict={},{},{},{}
        data_to_img(self.items,self.item_image_dict)
        data_to_img(self.backgrounds,self.background_image_dict)
        data_to_img(self.light_buttons,self.light_button_image_dict)
        data_to_img(self.dark_buttons,self.dark_button_image_dict)
        
        self.font_size=round(2520/self.winfo_fpixels('1i'))
        self.font="Roboto {}".format(self.font_size)
        
        self.config_data = ConfigParser()
        self.config_data.read("docs/config.ini")
        self.mode = self.config_data["MODE"]["type"]
        if self.mode=="dark":self.background_color,self.text_color=rgb_to_hex((26,26,26)),rgb_to_hex((229,229,229))
        elif self.mode=="light":self.background_color,self.text_color=rgb_to_hex((229,229,229)),rgb_to_hex((26,26,26))
        
    def set_vars(self):
        self.calculated_value,self.displayed_value,self.result,self.cursor_state,self.button_list="","","","hidden",[]
        self.x,self.y,self.button_count,self.background_animation_count=1,126,0,0
        self.content={"C":"C","open_parenthesis":"(","close_parenthesis":")","division":"÷","seven":"7","eight":"8","nine":"9","multiply":"×","four":"4","five":"5","six":"6","minus":"-","one":"1","two":"2","three":"3","plus":"+","period":"•","zero":"0","delete":"d","equal":"=","empty":"","right_corner":"","left_corner":""}
        self.place_list=["left_corner","empty","empty","empty","empty","empty","empty","empty","right_corner","empty","C","empty","open_parenthesis","empty","close_parenthesis","empty","division","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","seven","empty","eight","empty","nine","empty","multiply","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","four","empty","five","empty","six","empty","minus","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","one","empty","two","empty","three","empty","plus","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty","period","empty","zero","empty","delete","empty","equal","empty","empty","empty","empty","empty","empty","empty","empty","empty","empty"]
        self.keyboard_input_dict={ "=":["equal","Enter","Return"],"+":["plus"],"-":["minus"],"×":["times","multiply","Asterisk"],"÷":["division","divided by"],".":["period"],"d":["Delete","BackSpace","d","D"],"C":["c","C","Clear"],"(":["Open Parenthesis","Open_Parenthesis"], ")":["Close Parenthesis","Close_Parenthesis"],"numbers":list(("1,2,3,4,5,6,7,8,9,0"))}
        
    def create_widgets(self):
        self.canvas=Canvas(height=400,width=225,bg=rgb_to_hex((24,31,50)))
        self.canvas.place(x=-1,y=-1)
            
        self.background_image=self.canvas.create_image(0,150,image="",anchor=NW)
        self.background_animation()
            
        self.cursor=Label(text="|",bg=rgb_to_hex((24,31,50)),font=self.font)
        self.cursor.place(x=5,y=30)
        self.cursor_animation()
        self.label=Label(text="",justify=LEFT,bg=rgb_to_hex((24,31,50)),font=self.font)
        self.label.place(x=5,y=30)
        
        self.frame=Frame(relief='raised',bg=self.background_color,bd=0,highlightthickness=0)
        self.frame.place(x=-1,y=-1,width=226,height=30)
        self.close_button=Button(image=self.item_image_dict["close"],bg=self.background_color,fg=self.text_color,activebackground=self.background_color,bd=0,highlightthickness=0,font=self.font,command=self.destroy)
        self.close_button.place(x=196,y=-1,width=30,height=30)
        self.mode_button=Button(image=self.item_image_dict[self.mode],bg=self.background_color,fg=self.text_color,activebackground=self.background_color,bd=0,highlightthickness=0,command=self.update_mode,font=self.font)
        self.mode_button.place(x=160,y=-1,width=30,height=30)
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
            self.button_count+=1
            if self.button_count%9==0:
                self.y+=25
                self.x=1
        
    def calculate(self,number):
        if len(self.displayed_value)==10:
             self.displayed_value+="\n"
        if number=="=":
            self.show_result()
        elif number=="C":
            self.result=""
            self.calculated_value=""
            self.displayed_value=""
            self.label["text"]=self.displayed_value
        elif number=="d":
            if self.displayed_value=="":
                self.result=""
            if len(self.displayed_value)==11:
                self.calculated_value=self.calculated_value[:-2]
                self.displayed_value=self.displayed_value[:-2]
                self.label["text"]=self.displayed_value
            else:
                self.calculated_value=self.calculated_value[:-1]
                self.displayed_value=self.displayed_value[:-1]
                self.label["text"]=self.displayed_value
        if len(self.displayed_value)<21:
            if number=="÷":
                self.calculated_value+="/"
                self.displayed_value+="÷"
                self.label["text"]=self.displayed_value
            elif number=="×":
                self.calculated_value+="*"
                self.displayed_value+="×"
                self.label["text"]=self.displayed_value
            elif number=="•":
                self.calculated_value+="."
                self.displayed_value+="."
                self.label["text"]=self.displayed_value
            elif number in list(("C","d","=")):
                pass
            else:
                self.calculated_value+=str(number)
                self.displayed_value+=str(number)
                self.label["text"]=self.displayed_value
        else:
            self.label["text"]="Max Input\nReached !"
            self.after(1000,lambda :self.label.config(text=self.displayed_value))
            
    def show_result(self):
         try:
            self.result=eval(str(self.calculated_value))
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
            self.calculated_value=""
            self.displayed_value=""
         except:
            self.result="error"
            self.label["text"]="Input Error !"
            self.after(1000,lambda :self.label.config(text=self.displayed_value))
            
    def update_mode(self):
        self.mode_count=0
        if self.mode=="light":
            self.background_color,self.text_color=rgb_to_hex((26,26,26)),rgb_to_hex((229,229,229))
            for x in self.place_list:
                self.canvas.itemconfig(self.button_list[self.mode_count],image=self.dark_button_image_dict[x])
                self.mode_count+=1
            self.mode="dark"
        elif self.mode=="dark":
            self.background_color,self.text_color=rgb_to_hex((229,229,229)),rgb_to_hex((26,26,26))
            for x in self.place_list:
                self.canvas.itemconfig(self.button_list[self.mode_count],image=self.light_button_image_dict[x])
                self.mode_count+=1
            self.mode="light"
        with open("docs/config.ini", "w") as f:
            self.config_data["MODE"] = {"type":self.mode}
            self.config_data.write(f)
        self.frame["bg"]=self.background_color
        self.close_button["bg"]=self.background_color
        self.mode_button["bg"]=self.background_color
        self.mode_button["image"]=self.item_image_dict[self.mode]
        self.title_label["bg"]=self.background_color
        self.close_button["activebackground"]=self.background_color
        self.mode_button["activebackground"]=self.background_color
        self.title_label["fg"]=self.text_color
        
    def cursor_animation(self):
        if self.result=="" and self.displayed_value=="":
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
        if self.background_animation_count==72:
            self.background_animation_count=0
        self.after(100,self.background_animation)
        
    def keyboard_input_check(self,event):
        self.char=""
        for i in self.keyboard_input_dict:
            if event.keysym in self.keyboard_input_dict[i]:
                self.char=event.keysym
        if event.keysym in self.keyboard_input_dict["numbers"]:
            self.char=event.keysym
        self.calculate(self.char)
        
    def get_pos(self,event):
        self.xwin = self.winfo_x()
        self.ywin = self.winfo_y()
        self.startx = event.x_root
        self.starty = event.y_root
        self.ywin = self.ywin - self.starty
        self.xwin = self.xwin - self.startx
        def move_window(event):
            self.config(cursor="fleur")
            self.geometry(f'+{event.x_root + self.xwin}+{event.y_root + self.ywin}')
        def release_window(event):
            self.config(cursor="arrow")
            
        self.bind('<B1-Motion>', move_window)
        self.bind('<ButtonRelease-1>', release_window)
        
def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb
    
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
        
def start():
    root=Root()
    root_width = 225
    root_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - root_width / 2)
    center_y = int(screen_height/2 - root_height / 2)
    root.title("Gui Calculator")
    root.tk_setPalette(rgb_to_hex((24,31,50)))
    root.geometry(f"{root_width}x{root_height}+{center_x}+{center_y}")
    root.overrideredirect(True)
    root.resizable(False,False)
    root.attributes('-topmost', 'true')
    root.mainloop()
