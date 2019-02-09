from kivy.app import App, Widget
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import (Rectangle)
from kivy.graphics.context_instructions import Color
from kivy.core.text import Label as CoreLabel
from kivy.config import Config
import numpy as np
import atexit
import random
from random_words import words
import math


Config.set('graphics', 'maxfps', '100')
print('Set max FPS to', Config.get('graphics', 'maxfps'))
# Config.set('kivy', 'log_level', 'error')

# Color value run from 0 to 1 (not 255)
COLOR = {
    'BLACK': (0, 0, 0),
    'WHITE': (1, 1, 1),
    'RED': (1, 0, 0),
    'GREEN': (0, 1, 0),
    'BLUE': (0, 0, 1)
}

# Color value run from 0 to 1 (not 255)
LABEL_COLOR = {
    'BLACK': [0, 0, 0, 1],
    'WHITE': [1, 1, 1, 1],
    'RED': [1, 0, 0, 1],
    'GREEN': [0, 1, 0, 1],
    'BLUE': [0, 0, 1, 1]
}

tile_settings = [
    {'x': 'middle', 'y': 'top', 'hz': 6},
    {'x': 'left', 'y': 'middle', 'hz': 6.57},
    {'x': 'right', 'y': 'middle', 'hz': 7.5},
    {'x': 'middle', 'y': 'bottom', 'hz': 8.57}
]
# app will terminate after specify time
# set to 0 to disable auto exit
EXIT_TIME = 10


class FlickeringTile(Widget):
    def __init__(self, config, **kwargs):
        super(FlickeringTile, self).__init__(**kwargs)
        self.state = True
        # x, y start from bottom left
        self.rect_x = config['x']
        self.rect_y = config['y']
        self.rect_width = config.get('width')
        self.rect_height = config.get('height')
        self.rect_relative_size = config.get('size', 0.2)
        # 1 hz has 2 flips (eg. black -> white -> black is called 1 time)
        self.rect_flip_freq = config['hz'] * 2
        self.hz = config['hz']
        self.padding = config.get('pad', 30)
        self.rect_event = Clock.schedule_interval(
            lambda time_passed: self.flick(time_passed), 1 / self.rect_flip_freq
        )
        self.change_text_event = Clock.schedule_interval(
            lambda time_passed: self.change_text(), 1
        )
        self.canvas.clear()

        # Use for further analysis on statistic of diff and fps
        self.statistic = {
            'error': [],
            'fps': []
        }
        self.label_frequency = Label(text=str(self.hz) + ' Hz', font_size=30)
        self.label_1 = Label(text=str(self.rect_flip_freq), font_size=100)
        self.label_2 = Label(text=str(self.rect_flip_freq), font_size=100)

        # self.flick(0.5)
        # self.bind(pos=lambda a,b:self.flick(0.5), size=lambda a,b:self.flick(0.5))

    # try to make the tiles look most pretty by calculate to position of it
    # base on screen size and tile size
    def get_pos(self):
        width, height = self.get_size()
        if self.rect_x == 'middle' and self.rect_y == 'top':
            return self.width/2 - width/2, self.height - height - self.padding
        if self.rect_x == 'left' and self.rect_y == 'middle':
            return 0 + self.padding, self.height/2 - height/2
        if self.rect_x == 'right' and self.rect_y == 'middle':
            return self.width - width - self.padding, self.height/2 - height/2
        if self.rect_x == 'middle' and self.rect_y == 'bottom':
            return self.width/2 - width/2, 0 + self.padding
        if self.rect_x and self.rect_y:
            return self.rect_x, self.rect_y

    def get_label_pos(self):
        x, y = self.get_pos()
        width, height = self.get_size()
        return (x + width / 2 - self.padding), (y + height / 2 - self.padding)

    def get_size(self):
        if self.rect_width and self.rect_height:
            return self.rect_width, self.rect_height
        return self.width * self.rect_relative_size, self.width * self.rect_relative_size

    def change_text(self):
        # self.label_1.text = self.label_2.text = str(random.randint(0, 100))
        self.label_1.text = self.label_2.text = random.choice(words)

    def flick(self, time_passed):
        self.statistic['error'].append(math.fabs((1 / time_passed - self.rect_flip_freq) / self.rect_flip_freq))
        fps = Clock.get_rfps()
        # Ignore FPS of a few first frames which are 0
        # (fps of Kivy needs some initial frame before reporting the value for us)
        if fps > 0:
            self.statistic['fps'].append(fps)
        size = self.get_size()
        pos = self.get_pos()
        label_pos = self.get_label_pos()
        with self.canvas:
            self.canvas.clear()
            if self.state:
                Color(*COLOR['WHITE'])
            else:
                Color(*COLOR['BLACK'])
            Rectangle(pos=pos, size=size)

            if self.state:
                self.remove_widget(self.label_2)
                # self.label_1.text = str(randint(0, 100))
                self.label_1.pos = label_pos
                self.label_1.font_size = size[1] / 5
                self.label_1.color = LABEL_COLOR['BLACK']
                self.add_widget(
                    self.label_1
                )
            else:
                self.remove_widget(self.label_1)
                # self.label_2.text =
                self.label_2.pos = label_pos
                self.label_2.font_size = size[1] / 5
                self.label_2.color = LABEL_COLOR['WHITE']
                self.add_widget(
                    self.label_2
                )
            self.remove_widget(self.label_frequency)
            self.label_frequency.pos = pos
            self.add_widget(
                self.label_frequency
            )
            self.state = not self.state


class Main(App):
    def build(self):
        box = FloatLayout()
        tiles = []
        for setting in tile_settings:
            tile = FlickeringTile(setting)
            tiles.append(tile)
            box.add_widget(tile)

        # terminate app after 10 seconds
        if EXIT_TIME != 0:
            Clock.schedule_interval(lambda tmp: self.exit_app(), EXIT_TIME)

        # Report some statistic of the FPS and Delay
        # when this program is killed / exits
        atexit.register(lambda: Main.report_statistic(tiles))
        return box

    def exit_app(self):
        self.stop()

    @staticmethod
    def report_statistic(tiles):
        print('On Exit Report')
        for tile in tiles:
            print('Tile with %.2f hz:' % (tile.rect_flip_freq / 2))
            print('Average Absolute Error: %.2f%%' % (np.mean(tile.statistic['error']) * 100))
            print('Average Absolute FPS: %.2f fps' % np.mean(tile.statistic['fps']))


if __name__ == "__main__":
    Main().run()
