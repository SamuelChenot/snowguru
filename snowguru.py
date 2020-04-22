#disable multitouch functionality
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


#import the required kivy dependencies
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from functools import partial
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView


import setup
import zip_find

Builder.load_file('menubar.kv')
Builder.load_file('screens.kv')



class MenuContainer(AnchorLayout):

    #constructor
    def __init__(self, **kwargs):
        super(MenuContainer, self).__init__(**kwargs)

        #load the login popup when the app starts
        Clock.schedule_once(self.getStartupPopup, 0)

    def getStartupPopup(self, inst):
        pop = Popup(title='SnowGuru', title_align='center',content=Image(source='mountain.jpg'),
            size_hint=(None,None), height=400, width=400)
        pop.open()


class MenuManager(ScreenManager):

    #change the current screen to the one with the specified name
    def switchScreens(self, name):
        self.current = name

# TODO split these classes up into multiple different files, for readability
# where all of the screens functions can be stored.

class LoginPopup(Popup):

    #open the signup screen and close the current login screen
    def openSignupPopup(self):
        SignupPopup().open()
        self.dismiss()


class SettingsScreen(Screen):

    #this function will update the user's personal data
    def updateSettings(self):

        user_data = {}
            

        #try to locate the city/state from the given zipcode
        #if it fails, don't write to the data file
        try:
            int(self.zipcode.text)
            city, state = zip_find.zip_to_city_state(self.zipcode.text)

            user_data['zip'] = self.zipcode.text
            user_data['city'] = city
            user_data['state'] = state

            #add the user's data to the file
            setup.write_data(user_data)

            self.city_state_label.text = "Location: " + city + ", " + state
        except:
            self.city_state_label.text = "Error: invalid zip code"
    
        #print the user's city/state to the city_state_label

        return

class HomeMountainScreen(Screen):
    pass

class MountainFinderScreen(Screen):
    
    def getItems(self):
        f = open("mountain.txt", "r")
        list1 = self.list = list(f)
        return list1
class SignupPopup(Popup):
    pass

class MenuButton(Button):
    pass

class MenuApp(App):
    def build(self):
        return MenuContainer()


if __name__=="__main__":
    MenuApp().run()