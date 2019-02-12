from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
import numpy as np
import atexit
from config import experiment_setup, appearance
from experiment.story import Story
import logging

logger = logging.getLogger('FLASHING_EXPERIMENT')
Config.set('graphics', 'maxfps', experiment_setup.MAX_FPS)
logger.info('Set max FPS to', Config.get('graphics', 'maxfps'))
# Config.set('kivy', 'log_level', 'error')
# Config.set("kivy", "log_enable", "0")
if appearance.FULL_SCREEN:
    Config.set('graphics', 'fullscreen', 'auto')


class Main(App):
    def build(self):
        box = FloatLayout()
        story = Story(box, experiment_setup.story_setup, self.exit_app)

        # Report some statistic of the FPS and Delay
        # when this program is killed / exits
        # atexit.register(lambda: Main.report_statistic(story.tiles))
        return box

    def exit_app(self):
        self.stop()

    @staticmethod
    def report_statistic(tiles):
        logging.info('On Exit Report')
        for tile in tiles:
            logging.info('Tile with %.2f hz:' % (tile.rect_flip_freq / 2))
            logging.info('Average Frequency: %.4f' % (1 / np.mean(tile.statistic['period'])))
            logging.info('Average Absolute Error: %.2f%%' % (np.mean(tile.statistic['error']) * 100))
            logging.info('SD of Frequency: %.2f' % (np.std(tile.statistic['period'])))
            logging.info('Average Absolute FPS: %.2f fps' % np.mean(tile.statistic['fps']))


if __name__ == "__main__":
    Main().run()
