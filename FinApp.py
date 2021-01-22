from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager,Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty,ListProperty
import sqlite3
from datetime import datetime
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import BooleanProperty
from kivymd.uix.datatables import MDDataTable
from kivy.uix.popup import Popup
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.button import Button
from kivymd.uix.tab import MDTabsBase
from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons
month=""
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout



class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt


class Page_One(MDScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        dropdown=ObjectProperty()


    def Income_Page(self):
        pass




class Page_Two(MDScreen,MDTabsBase):

    dropdown = ObjectProperty()
    amount= StringProperty()
    description = StringProperty
    data_items1 = ListProperty([])

    def __init__(self, **kwargs):
        super(Page_Two, self).__init__(**kwargs)
        #self.show_income_items()
    try:
        # Create Database Connection
        Inc_con = sqlite3.connect("Income.db")
        Inc_cur = Inc_con.cursor()

        Inc_cur.execute("""CREATE TABLE IF NOT EXISTS income(id INTEGER PRIMARY KEY autoincrement,Month text 
        CHECK(Month!=""),Source text CHECK(Source!=""),Amount REAL CHECK(Amount!=""))
        """)
        Inc_con.commit()
        Inc_con.close()

    except sqlite3.IntegrityError: print("Field shouldnt be blank")



    def insert_data(self):
        try:
            current_month= self.m()
            print(current_month)

            Inc_con = sqlite3.connect("Income.db")
            Inc_cur = Inc_con.cursor()
            Inc_cur.execute("""INSERT INTO income(id,Month,Source,Amount) VALUES(NULL,?,?,?)""",(current_month,self.description,self.amount))
            Inc_con.commit()
        except sqlite3.IntegrityError:
            print("Field shouldn't be blank")






    def show_income_items(self,*args):

        current_month = self.m()
        Inc_con = sqlite3.connect("Income.db")
        Inc_cur = Inc_con.cursor()
        Inc_cur.execute("SELECT * from income   WHERE Month=?",(current_month,))
        rows = Inc_cur.fetchall()
        for row in rows:
            for col in row:
                self.data_items1.append(col)


    def get_time(self):
        global x
        x=StringProperty()
        x= datetime.today().strftime("%Y")
        return x


    def on_kv_post(self, base_widget):

        caller = self.ids.caller # This is the MDDropdDownitem from the kivy file
        months=["January","February","March","April","May","June","July","August","September","October","November","December"]
        menu_items = [{"viewclass": "MDMenuItem","icon": "calendar", "text": f" {i}"} for i in months]
        self.dropdown = MDDropdownMenu(caller=caller, items=menu_items,
                                       width_mult=4)
        self.dropdown.bind(on_release=self.set_item)
        self.dropdown.bind(on_release=self.show_income_items) # Make Database Popup once month is selected



    def set_item(self, instance_menu, instance_menu_item):
        # Function meant to get value of month selected in dropdown
        global month
        month = instance_menu_item.text

        a=self.ids.caller.set_item(instance_menu_item.text)

        instance_menu.dismiss()
        return month

    def m(self):
        l=month
        return l


class Tab(MDFloatLayout,MDTabsBase):
    pass



class Page_Three(MDScreen,MDFloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


class Page_Four(MDScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


class ScreenManage(ScreenManager):
    pass



class MainApp(MDApp):

    def build(self):
        self.kv = Builder.load_file("fin.kv")
        title = "Financial Mobile App"
        return self.kv

    def on_start(self):
        #self.kv.get_screen("Income").ids.tabs.add_widget(Tab(text="Camera"))
        pass

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

        instance_tab.ids.budgets.text = tab_text





if __name__ == "__main__":
    MainApp().run()