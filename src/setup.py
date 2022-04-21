from urllib.request import urlopen
import json
from zipfile import ZipFile
import os
from io import BytesIO
import shutil
from tkinter import *
from PIL import ImageTk,Image
from threading import *
from configparser import ConfigParser

APP_AUTHOR = "destrochloridium"
APP_NAME = "Gui-Calculator"
APP_BRANCH = "main"
VERSION_LINK = "https://raw.githubusercontent.com/" + APP_AUTHOR + "/" + APP_NAME + "/" + APP_BRANCH+ "/docs/version.json"
APP_DIR = os.path.realpath(".")

class Starter:
    def __init__(self):
        
        self.latest_info = self.get_latest_info()
        self.current_info = self.get_current_info()
        self.config_data = ConfigParser()
        self.config_data.read("docs/config.ini")
        self.check_button_station =self.config_data["ON CLOSE"]["message"]
        self.destroy_program=False
        self.font_size=round(2520/get_dpi())

        if self.latest_info!=None and not (self.is_update()) and self.check_button_station== "on":
            with open("docs/main_data.json","+r") as text:
                self.data=json.load(text)
            self.item_dict={}
            self.destroy_program=True
            self.create_update_messagebox()
        else:
            self.run_program() 
         
    def run_program(self):
        if self.destroy_program==True:
            self.master.destroy()
        import src.gui_calculator
        src.gui_calculator.start()

    def get_latest_info(self):
        try:
            url = urlopen(VERSION_LINK)
            latest_info = json.loads(url.read().decode())
            return latest_info
        except:
            return None

    def get_current_info(self):
        try:
            with open("docs/version.json", "r") as f:
                current_info = json.loads(f.read())
            return current_info
        except FileNotFoundError: 
            return {"version" : "", "link" : ""}

    def update(self):
        self.__update_files(".cache/updated_app_data.zip")
        self.show_update_messagebox((186,249),"updated")

    def __update_files(self, zip_file_path):
        self.clear_app_dirs()
        self.fetch_data(zip_file_path)
        self.reconfigure_dirs(zip_file_path)
        shutil.rmtree(".cache")

    def clear_app_dirs(self):
        for _dir in os.listdir():
            if (_dir == "main.py"):
                continue
            if (os.path.isfile(_dir)):
                os.remove(_dir)
            elif (os.path.isdir(_dir)):
                shutil.rmtree(_dir)

    def fetch_data(self, zip_file_path):
        os.mkdir(".cache")
        link = self.latest_info["link"]
        updated_app_data = urlopen(link).read()
        with open(zip_file_path, "wb") as f:
            f.write(updated_app_data)

    def reconfigure_dirs(self, zip_file_path):
        with ZipFile(zip_file_path, "r") as zip_file:
            zip_file.extractall(".cache") 
            CACHE_DIR = os.path.join(APP_DIR, ".cache" , APP_NAME + "-" + APP_BRANCH)
            for _dir in os.listdir(CACHE_DIR):
                if _dir != "main.py":
                    old_path = os.path.join(CACHE_DIR, _dir)
                    new_path = os.path.join(APP_DIR, _dir)
                    os.rename(old_path, new_path)

    def is_update(self):
        return self.current_info["version"] == self.latest_info["version"] 
    
    def save_changes(self):
        if not self.is_update():
            self.current_info = self.latest_info
        with open("docs/version.json", "w") as f:
            f.write(json.dumps(self.current_info, indent = 4))
            
    def create_update_messagebox(self):
        self.master=Tk()
        data_to_img(self.data,self.item_dict)
        self.check_button_station="off"
        self.toplevel = Toplevel(self.master)
        self.toplevel.attributes('-topmost', 'true')
        self.toplevel.tk_setPalette("black")
        self.toplevel.resizable(False, False)
        self.toplevel.overrideredirect (True)
        self.canvas=Canvas(self.toplevel,height=0,width=0,bg="black")
        self.canvas.place(x=-1,y=-1)
        self.show_update_messagebox((186,249),"update")
        self.master.mainloop()
            
    def show_update_messagebox(self,size,station):
        self.master.withdraw()
        self.toplevel_width = size[0]
        self.toplevel_height = size[1]
        self.screen_width = self.toplevel.winfo_screenwidth()
        self.screen_height = self.toplevel.winfo_screenheight() 
        self.center_x = int(self.screen_width/2 - self.toplevel_width / 2)
        self.center_y = int(self.screen_height/2 - self.toplevel_height / 2) 
        self.toplevel.geometry(f"{self.toplevel_width}x{self.toplevel_height}+{self.center_x}+{self.center_y}")
        self.canvas.config(height=self.toplevel_height,width=self.toplevel_width)
        
        if station=="update":
            self.canvas.create_image(0,0,image=self.item_dict["update_message_background"],anchor=NW)
            self.close=self.canvas.create_text(165,-10,text="×",fill="red",font=("Roboto",self.font_size),anchor=NW)
            self.check_button_text=self.canvas.create_text(35,190,text="Do Not Show This Again.",font=("Roboto",int(self.font_size/4)),fill="white",anchor=NW)
            self.check_button=self.canvas.create_image(20,190,image=self.item_dict["check_off"],anchor=NW)
            self.yes_button=self.canvas.create_text(25,206,text="                                 ",font=("Roboto",int(self.font_size/2)) ,fill="cyan",anchor=NW)
            self.rocket=self.canvas.create_image(148,200,image=self.item_dict["rocket_stay"],anchor=NW)
            self.canvas.tag_bind(self.close,"<Button->",lambda x:self.run_program())
            self.canvas.tag_bind(self.check_button,"<Button->",lambda x:self.control_check_button())
            self.canvas.tag_bind(self.yes_button,"<Button->",lambda x:self.show_update_messagebox((186,249),"updating"))
        
        elif station=="updating":
            self.thread_1=Thread(target = lambda:self.movement(False),daemon=True)
            self.thread_1.start()
            self.thread_2=Thread(target=self.update)
            self.thread_2.start()
            
        elif station=="updated":
            self.canvas.create_image(0,0,image=self.item_dict["updated_message_background"],anchor=NW)
            self.start_button=self.canvas.create_text(25,206,text="                                  ",font=("Roboto",int(self.font_size/2)),anchor=NW)
            self.canvas.tag_bind(self.start_button,"<Button->",lambda x:self.run_program())
            
    def movement(self,start):
        if not start:
            self.canvas.itemconfig(self.yes_button,state="disabled")
            self.canvas.itemconfig(self.rocket,image=self.item_dict["rocket_fly"])
            start=True
        self.canvas.move(self.rocket, 0,-1)
        self.canvas.after(20, lambda:self.movement(start))
       
    def control_check_button(self):
        if self.check_button_station=="off":
            self.canvas.itemconfig(self.check_button,image=self.item_dict["check_on"])
            self.canvas.itemconfig(self.check_button_text,font=("Roboto",int(self.font_size/4),"bold"))
            with open("docs/config.ini", "w") as f:
                self.config_data["ON CLOSE"] = {"message":self.check_button_station}
                self.config_data.write(f)
            self.check_button_station="on"
        elif self.check_button_station=="on":
            self.canvas.itemconfig(self.check_button,image=self.item_dict["check_off"])
            self.canvas.itemconfig(self.check_button_text,font=("Roboto",int(self.font_size/4)))
            with open("docs/config.ini", "w") as f:
                self.config_data["ON CLOSE"] = {"message":self.check_button_station}
                self.config_data.write(f)
            self.check_button_station="off"
        
def get_dpi():
    screen = Tk()
    current_dpi = screen.winfo_fpixels('1i')
    screen.destroy()
    return current_dpi
    
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
