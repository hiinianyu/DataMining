from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from Milestone5 import getRegressionFunction
import pandas as pd
from io import StringIO
import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            df = pd.read_csv(StringIO(stream.read()))
            result = getRegressionFunction(df)
            self.text_input.text = 'y = ' + str(result.M1) + ' * 2 Days moving average + ' + str(result.M2) + ' * 5 days moving average + ' + str(result.C)

        self.dismiss_popup()


class FirstApp(App):

    def build(self):
        return Root()


if __name__ == '__main__':
    FirstApp().run()