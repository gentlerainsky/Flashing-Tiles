from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
import numpy as np
import atexit
from config import experiment_setup
from experiment.flickering_tile import FlickeringTile

Config.set('graphics', 'maxfps', experiment_setup.MAX_FPS)
print('Set max FPS to', Config.get('graphics', 'maxfps'))
# Config.set('kivy', 'log_level', 'error')


class Main(App):
    def build(self):
        box = FloatLayout()
        tiles = []
        for setting in experiment_setup.tile_settings:
            tile = FlickeringTile(setting)
            tiles.append(tile)
            box.add_widget(tile)

        # terminate app after 10 seconds
        if experiment_setup.EXIT_TIME != 0:
            Clock.schedule_interval(lambda tmp: self.exit_app(), experiment_setup.EXIT_TIME)

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
            print('Average Frequency: %.4f' % (1 / np.mean(tile.statistic['period'])))
            print('Average Absolute Error: %.2f%%' % (np.mean(tile.statistic['error']) * 100))
            print('SD of Frequency: %.2f' % (np.std(tile.statistic['period'])))
            print('Average Absolute FPS: %.2f fps' % np.mean(tile.statistic['fps']))


if __name__ == "__main__":
    Main().run()
