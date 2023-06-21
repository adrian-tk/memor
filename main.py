import kivy
import memor
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Window.softinput_mode = 'below_target' #move all when keyboard on android is on

class Memor(App):
    def build(self):
        return MyRoot()

class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def generate_words(self):
        #self.random_label.text = str(random.randint(0, 2000))
        self.label_words.text = memor.search_words(self.input_number.text)

memor_app=Memor()
#memor_app=MyRoot()
memor_app.run()
