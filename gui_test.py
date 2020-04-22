from tkinter import *
import tkinter.messagebox as tm
import tkinter.ttk as ttk
import sql_interactions as db
from PIL import Image

import tkinter as tk
#GLOBAL
UID = 0

def update_user_coords(zipcode):
    global UID
    LAT = 0
    LON = 0


    #Need to implement


    # db.update_user_coordinates(UID, LAT, LON)


"""
Set the user to a unique number identified by the sql system
"""
def set_UID():
    global UID
    #SQL call
    UID_ = db.get_new_uid(0,0)
    UID = UID_

"""
Set a new UID and switch the the front page
"""
def login(master):
    set_UID()
    master.switch_frame(StartPage)

"""
Toggle sql home data table
"""
def toggle_home(MID):
    print("Selected: ", MID)
    global UID
    #SQL call
    db.add_mountain_to_user(UID, MID)
    #Opens popup window to prompt user
    tm.showinfo("Mountain Database", "Mountain Toggled")
    return

"""
Shows all daily infor
"""
def show_info_daily(MID):
    #SQL call
    data = db.get_mountains_daily_info(MID)
    
    #THE FOLLWING IS SUBJECT TO CHANGE, CURRENTLY A & DAY FORCAST
    Outstring = "Today: "+str(data[0][9])+"/"+str(data[0][10])+" Fahrenheight\n"

    for i in range(1, 7):
        Outstring += "Day "+str(i)+": "+str(data[i][9])+"/"+str(data[i][10])+" Fahrenheight\n"

    #Popup window
    tm.showinfo("Mountain Database", Outstring)
    return

"""
Initializes the app and calls the forst window

Note that from here down 

SELF : refers to the current window
MASTER : refers to the entire app

This "tk.Frame.__init__(self, master)" at the beginning of a class
tells the program that that window is part of the "master" application
Note- Popup windows are not part of self or master and do not inherit settings or properties


This class should not have to be touched
"""
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

"""
Shows the Options for the other windows in the program
"""
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Formats the size of the window
        tk.Frame.configure(self,bg='gray77')
        tk.Frame.configure(master,bg='gray77')
        master.geometry('{}x{}'.format(400, 600))
        tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="See All Mountains",
                  command=lambda: master.switch_frame(AllMountains)).pack()
        tk.Button(self, text="See Saved Mountains",
                  command=lambda: master.switch_frame(SavedMountains)).pack()

"""
Window to display all mountains in database
"""
class AllMountains(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Formats the size of the window
        master.geometry('{}x{}'.format(400, 600))
        tk.Frame.configure(self,bg='gray77')
        tk.Label(self, text="All Mountains", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        #Initilize the scroll bar
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        #SQl call
        data = db.get_mountain_Names()

        #Adds items to the canvas which can be scrolled
        canvas = tk.Canvas(self)
        frame = tk.Frame(canvas)
        for i in data:
            tk.Button(canvas, text = str(i[0]), font=('Helvetica', 18, "bold"), \
                command=lambda i=i: toggle_home(str(i[1]))).pack(side="top", fill="x", pady=5)


        #The following adds the canvas to the scrollbar
        canvas.create_window(0, 0, anchor='nw', window=frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), 
                        yscrollcommand=scrollbar.set)
        canvas.pack(fill='both', expand=True, side='left')
        scrollbar.pack(fill='y', side='right')

""" 
Displays all of the users selected mountains stored in HomeMT in the SQL database

"""
class SavedMountains(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Formats the size of the window
        master.geometry('{}x{}'.format(400, 600))
        tk.Frame.configure(self,bg='gray77')
        tk.Label(self, text="SavedMountains", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        #Initilize the scroll bar
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        #SQL call
        data = db.get_user_list(UID)

        #Adds items to the canvas which can be scrolled
        canvas = tk.Canvas(self)
        frame = tk.Frame(canvas)
        for i in data:
            tk.Button(self, text = str(i[0]), font=('Helvetica', 18, "bold"), \
                command=lambda i=i: show_info_daily(str(i[1]))).pack(side="top", fill="x", pady=5)

        #The following adds the canvas to the scrollbar
        canvas.create_window(0, 0, anchor='nw', window=frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), 
                        yscrollcommand=scrollbar.set)           
        canvas.pack(fill='both', expand=True, side='left')
        scrollbar.pack(fill='y', side='right')

"""
Login frame that prompts the creation of the new UID
"""
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #Formats the size of the window
        tk.Frame.configure(self,bg='gray77')
        tk.Frame.configure(master,bg='gray77')
        master.geometry('{}x{}'.format(400, 600))
        self.label_username = Label(self, text = 'Zip Code')

        #Entries
        target_in = tk.StringVar()
        self.entry_username = Entry(self)
        self.label_username.grid(row=0, sticky=E)
        self.entry_username.grid(row=0, column=1)

        #Option the save the location (Unimplemented)
        self.checkbox = Checkbutton(self, text="Save my Location")
        self.checkbox.grid(columnspan=2)

        #Login button, moves user to main screen
        self.logbtn = Button(self, text="Login", command=lambda: login(master))
        self.logbtn.grid(columnspan=2)

        self.pack()


#Run
if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()

