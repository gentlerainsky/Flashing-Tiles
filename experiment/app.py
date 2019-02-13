from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
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
        Story(box, experiment_setup.story_setup, self.exit_app)
        return box

    def exit_app(self):
        self.stop()


if __name__ == "__main__":
    Main().run()
