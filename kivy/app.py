from kivy.app import App, Widget
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import (Rectangle)
from kivy.graphics.context_instructions import Color
from kivy.config import Config
import numpy as np
import atexit

Config.set('graphics', 'maxfps', '100')
print('Set max FPS to', Config.get('graphics', 'maxfps'))
# Config.set('kivy', 'log_level', 'error')

# Color value run from 0 to 1 (not 255)
COLOR = {
    'RED': (1, 0, 0),
    'GREEN': (0, 1, 0),
    'BLUE': (0, 0, 1)
}

tile_settings = [
    {'x': 'middle', 'y': 'top', 'hz': 6},
    {'x': 'left', 'y': 'middle', 'hz': 6.57},
    {'x': 'right', 'y': 'middle', 'hz': 7.5},
    {'x': 'middle', 'y': 'bottom', 'hz': 8.57}
]


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
        self.padding = config.get('pad', 30)
        self.rect_event = Clock.schedule_interval(
            lambda time_passed: self.flick(time_passed), 1 / self.rect_flip_freq
        )
        self.canvas.clear()

        # Use for further analysis on statistic of diff and fps
        self.statistic = {
            'error': [],
            'fps': []
        }
        # self.add_widget(
        #     Label(text=str(self.rect_flip_freq), font_size=50)
        # )

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

    def get_size(self):
        if self.rect_width and self.rect_height:
            return self.rect_width, self.rect_height
        return self.width * self.rect_relative_size, self.width * self.rect_relative_size

    def flick(self, time_passed):
        self.statistic['error'].append(((1 / time_passed - self.rect_flip_freq) / self.rect_flip_freq))
        fps = Clock.get_rfps()
        # Ignore FPS of a few first frames which are 0
        # (fps of Kivy needs some initial frame before reporting the value for us)
        if fps > 0:
            self.statistic['fps'].append(fps)
        size = self.get_size()
        pos = self.get_pos()
        with self.canvas:
            self.canvas.clear()
            if self.state:
                Color(*COLOR['BLUE'])
            else:
                Color(*COLOR['GREEN'])
            self.state = not self.state
            Rectangle(pos=pos, size=size)


class Main(App):
    def build(self):
        box = FloatLayout()
        tiles = []
        for setting in tile_settings:
            tile = FlickeringTile(setting)
            tiles.append(tile)
            box.add_widget(tile)
        # Report some statistic of the FPS and Delay
        # when this program is killed / exits
        atexit.register(lambda: Main.report_statistic(tiles))
        return box

    @staticmethod
    def report_statistic(tiles):
        print('On Exit Report')
        for tile in tiles:
            print('Tile with %.2f hz:' % (tile.rect_flip_freq / 2))
            print('Average Error: %.2f%%' % (np.mean(tile.statistic['error']) * 100))
            print('Average FPS: %.2f fps' % np.mean(tile.statistic['fps']))


if __name__ == "__main__":
    Main().run()
