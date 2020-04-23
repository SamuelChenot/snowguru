from tkinter import *
import tkinter.messagebox as tm
import tkinter.ttk as ttk
import sql_interactions as db
from PIL import ImageTk, Image
import zip_find

import tkinter as tk
#GLOBAL
UID = 0
zipc = ""

def update_user(zipcode):
    assert(UID != 0)
    update_user_coords(zipcode.get())
    tm.showinfo("Mountain Database", "Updated")

def update_user_coords(zipcode):
    global UID
    global zipc
    LAT,LON = zip_find.zip_to_coords(str(zipcode))
    print(LAT)
    print(LON)
    db.update_user_coordinates(UID, LAT, LON)

def get_previous_UID(master):

    try:
        file = open("UID.dat", "r")
        global UID 
        UID = int(file.readline())
        print("Loaded User: "+str(UID))
    except:
        set_UID()
    

    master.switch_frame(StartPage)
    

    

"""
Set the user to a unique number identified by the sql system
"""
def set_UID():
    global UID
    #SQL call
    UID_ = db.get_new_uid(0,0)
    UID = UID_
    file = open("UID.dat","w")
    file.write(str(UID))

"""
Set a new UID and switch the the front page
"""
def login(master, zipc):
    zipc = zipc.get()
    set_UID()
    update_user_coords(zipc)
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

    popup = tk.Tk()
    popup.wm_title("Mountain Information")
    #popup.geometry('{}x{}'.format(400, 600))
    B1 = ttk.Button(popup, text="Exit", command = popup.destroy)
    info = ['Name', 'MID', 'DAY', 'SUNRISETIME', 'SUNSETTIME' , 'PRECIPINTENSITY', 'PRECIPINTENSITYMAX', 'PRECIPPROB', 'PRECIPTYPE', 'TEMPHIGH', 'TEMPLOW', 'HUMIDITY', 'WINDSPEED', 'WINDGUST', 'WINDGUSTTIME', 'WINDBEARING', 'VISIBILITY', 'PREDICTEDSNOW']

    scrollbar = Scrollbar(popup)
    scrollbar.pack( side = RIGHT, fill = Y )

    mylist = Listbox(popup, yscrollcommand = scrollbar.set )
    for i in range(len(info)):
        if info[i] == 'DAY':
            mylist.insert(END, 'Today: \n')
        else:
            mylist.insert(END, str(info[i]) +": "+ str(data[0][i]))

    mylist.pack( side = LEFT, fill = BOTH )
    scrollbar.config( command = mylist.yview )
    
    
    B1.pack()
    popup.mainloop()

def show_info_hourly(MID):
    #SQL call
    data = db.get_mountains_hourly_info(MID)

    popup = tk.Tk()
    popup.wm_title("Mountain Information")
    #popup.geometry('{}x{}'.format(400, 600))
    B1 = ttk.Button(popup, text="Exit", command = popup.destroy)
    info = ['Name', 'MID', 'Hour', 'PRECIPINTENSITY', 'PRECIPPROB', 'PRECIPTYPE','TEMPERATURE', 'APPARENTTEMP' ,'HUMIDITY', 'WINDSPEED', 'WINDGUST', 'WINDBEARING', 'VISIBILITY', 'PREDICTEDSNOW']

    scrollbar = Scrollbar(popup)
    scrollbar.pack( side = RIGHT, fill = Y )

    mylist = Listbox(popup, yscrollcommand = scrollbar.set )
    for i in range(len(info)):
        if info[i] == 'Hour':
            mylist.insert(END, 'Weather Now: \n')
        else:
            mylist.insert(END, str(info[i]) +": "+ str(data[0][i]))

    mylist.pack( side = LEFT, fill = BOTH )
    scrollbar.config( command = mylist.yview )
    
    
    B1.pack()
    popup.mainloop()



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
        tk.Frame.configure(self,bg="gray45")
        tk.Frame.configure(master,bg="gray45")
        master.geometry('{}x{}'.format(400, 600))
        tk.Label(self, text="Menu",bg="gray45", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="See All Mountains",bg="gray45",
                  command=lambda: master.switch_frame(AllMountains)).pack()
        tk.Button(self, text="Nearby Mountains",bg="gray45",
                  command=lambda: master.switch_frame(NearbyMountains)).pack()
        tk.Button(self, text="Saved Mountains",bg="gray45",
                  command=lambda: master.switch_frame(SavedMountains)).pack()
        tk.Button(self, text="Hourly Weather",bg="gray45",
                  command=lambda: master.switch_frame(HourlyWeatherMountains)).pack()        
        tk.Button(self, text="Edit User Info",bg="gray45",
                  command=lambda: master.switch_frame(EditUserInfo)).pack()
        self.photo = ImageTk.PhotoImage(Image.open("mountain.jpg"))
        tk.Label(self, image = self.photo, compound="top").pack(side="top", fill="x", pady=5)

class EditUserInfo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Formats the size of the window
        master.geometry('{}x{}'.format(400, 600))
        tk.Frame.configure(self,bg="gray45")
        tk.Label(self, text="Edit User Info", bg = "gray45", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        
        zipc = tk.StringVar()
        label1 = tk.Label(self, text= "Enter Zipcode").pack()
        ZIP = tk.Entry(self, textvariable = zipc).pack()

        #Add button
        self.logbtn = Button(self, text="Update", bg = "gray45", command=lambda: update_user(zipc)).pack()

        self.pack()


"""
Window to display all mountains in database
"""
class AllMountains(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Formats the size of the window
        master.geometry('{}x{}'.format(400, 600))
        tk.Frame.configure(self,bg='gray45')
        tk.Label(self, text="All Mountains", bg = "gray45", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        
        
        #SQl call
        data = db.get_mountain_Names()

        #Adds items to the canvas which can be scrolled
        container = ttk.Frame(self)
        canvas = tk.Canvas(container, width=380, height=550, bg = "gray45")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.photos = []
        for i in range(1, 70):
            photo = ImageTk.PhotoImage(Image.open("But_Pics/"+str(i)+".jpg"))
            self.photos.append(photo)

        photo = ImageTk.PhotoImage(Image.open("But_Pics/"+str(1)+".jpg"))
        self.photos.append(photo)

        for i in data:
            tk.Button(scrollable_frame, text = str(i[0]), image = self.photos[i[1]], compound="top", font=('Helvetica', 18, "bold"), \
                command=lambda i=i: toggle_home(str(i[1]))).pack(side="top", fill="x", pady=5)


        #The following adds the canvas to the scrollbar
        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class NearbyMountains(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Formats the size of the window
        master.geometry('{}x{}'.format(400, 600))
        tk.Frame.configure(self,bg='gray45')
        tk.Label(self, text="All Mountains", bg = "gray45", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        
        
        #SQl call
        global UID
        data = db.sort_distence_all(UID)
        # data = db.get_mountain_Names()

        #Adds items to the canvas which can be scrolled
        container = ttk.Frame(self)
        canvas = tk.Canvas(container, width=380, height=550, bg = "gray45")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.photos = []
        for i in range(1, 70):
            photo = ImageTk.PhotoImage(Image.open("But_Pics/"+str(i)+".jpg"))
            self.photos.append(photo)

        photo = ImageTk.PhotoImage(Image.open("But_Pics/"+str(1)+".jpg"))
        self.photos.append(photo)

        for i in data:
            tk.Button(scrollable_frame, text = str(i[0]), image = self.photos[i[1]], compound="top", font=('Helvetica', 18, "bold"), \
                command=lambda i=i: toggle_home(str(i[1]))).pack(side="top", fill="x", pady=5)


        #The following adds the canvas to the scrollbar
        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
""" 
Displays all of the users selected mountains stored in HomeMT in the SQL database
"""
class SavedMountains(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Formats the size of the window
        master.geometry('{}x{}'.format(400, 600))
        tk.Frame.configure(self,bg='gray45')
        tk.Label(self, text="SavedMountains", bg = "gray45", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        #Initilize the scroll bar
        # scrollbar = Scrollbar(self)
        # scrollbar.pack(side=RIGHT, fill=Y)

        #SQL call
        data = db.get_user_list(UID)

        # #Adds items to the canvas which can be scrolled

        container = ttk.Frame(self)
        canvas = tk.Canvas(container, width=380, height=550, bg = "gray45")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)


        self.photos = []
        for i in range(1, 70):
            photo = ImageTk.PhotoImage(Image.open("But_Pics/"+str(i)+".jpg"))
            self.photos.append(photo)



        for i in data:
            b = tk.Button(scrollable_frame, text = str(i[0]), image = self.photos[i[1]], compound="top", font=('Helvetica', 18, "bold"), \
                command=lambda i=i: show_info_daily(str(i[1]))).pack(side="top", fill="x", pady=5)

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")



"""
Login frame that prompts the creation of the new UID
"""
class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)


        #Formats the size of the window
        tk.Frame.configure(self,bg='gray45')
        tk.Frame.configure(master,bg='gray45')
        master.geometry('{}x{}'.format(400, 600))

        self.back_img = ImageTk.PhotoImage(Image.open("mountain.jpg"))



        self.label_username = Label(self, text = 'Zip Code', bg = "gray45")

        #Entries
        zipc = tk.StringVar()
        self.entry_username = Entry(self, textvariable=zipc, bg = "gray45")
        self.label_username.grid(row=1, sticky=E)
        self.entry_username.grid(row=1, column=1)
        #Option the save the location (Unimplemented)
        self.checkbox = Button(self, text="Returning user", bg = "gray45", command=lambda: get_previous_UID(master))
        self.checkbox.grid(columnspan=2, row=0)

        #Login button, moves user to main screen
        # self.login_button = ImageTk.PhotoImage(Image.open("login_button.png"))
        self.logbtn = Button(self, text="Create User", bg = "gray45", command=lambda: login(master, zipc))
        self.logbtn.grid(columnspan=2)

        self.pack()

class HourlyWeatherMountains(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #Formats the size of the window
        master.geometry('{}x{}'.format(400, 600))
        tk.Frame.configure(self,bg='gray45')
        tk.Label(self, text="SavedMountainsHourly", bg = "gray45", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        #Initilize the scroll bar
        # scrollbar = Scrollbar(self)
        # scrollbar.pack(side=RIGHT, fill=Y)

        #SQL call
        data = db.get_user_list(UID)

        # #Adds items to the canvas which can be scrolled

        container = ttk.Frame(self)
        canvas = tk.Canvas(container, width=380, height=550, bg = "gray45")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.photos = []
        for i in range(1, 70):
            photo = ImageTk.PhotoImage(Image.open("But_Pics/"+str(i)+".jpg"))
            self.photos.append(photo)


        for i in data:
            b = tk.Button(scrollable_frame, text = str(i[0]), image = self.photos[i[1]], compound="top", font=('Helvetica', 18, "bold"), \
                command=lambda i=i: show_info_hourly(str(i[1]))).pack(side="top", fill="x", pady=5)

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

#Run
if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()