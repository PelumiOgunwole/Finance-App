from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager,Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.menu import  MDDropdownMenu
from kivy.properties import ObjectProperty
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import StringProperty
import sqlite3
from datetime import datetime

Inc_con= sqlite3.connect("Income.db")
Inc_cur= Inc_con.cursor()
#Inc_cur.execute("""CREATE TABLE
# income (INT PRIMARY KEY""")

class Page_One(MDScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        dropdown=ObjectProperty()


    def Income_Page(self):
        pass



class Page_Two(MDScreen):
    dropdown = ObjectProperty()

    #x=datetime.time()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


    def on_kv_post(self, base_widget):

        caller = self.ids.caller # This is the MDDropdDownitem from the kivy file
        months=["January","February","March","April","May","June","July","August","September","October","November","December"]
        menu_items = [{"viewclass": "MDMenuItem","icon": "git", "text": f" {i}"} for i in months]
        self.dropdown = MDDropdownMenu(caller=caller, items=menu_items,
                                       width_mult=4)
        #self.dropdown.bind(on_select=lambda instance, x: setattr(months, 'text', x))
        self.dropdown.bind(on_release=self.set_item)
    def set_item(self, instance_menu, instance_menu_item):
        self.screen.ids.caller.set_item(instance_menu_item.text)
        self.menu.dismiss()



class Page_Three(MDScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


class Page_Four(MDScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


class ScreenManage(ScreenManager):
    pass



class MainApp(MDApp):
    def __init__(self,**kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title="Thrift + App"
        self.icon= "pichat.png"
    def build(self):
        kv = Builder.load_file("fin.kv")
        title = "Financial Mobile App"
        return kv




if __name__ == "__main__":
    MainApp().run()