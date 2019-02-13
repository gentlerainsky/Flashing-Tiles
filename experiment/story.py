from experiment.scenario import Scenario
from experiment.start_screen import StartScreen
from experiment.statistics import Statistic
import random
import logging

logger = logging.getLogger('FLASHING_EXPERIMENT')


class ScreenType:
    START_SCREEN = 0
    EXPERIMENT_SCENARIO = 1
    BREAK_TIME = 2


class Story:
    def __init__(self, container, story_setup, callback):
        self.container = container
        self.break_interval = story_setup['break_interval']
        self.scenario_interval = story_setup['scenario_interval']
        self.scenarios = story_setup['scenarios']
        self.enable_random = story_setup['enable_random']
        self.enable_start_screen = story_setup['enable_start_screen']
        self.scenario_order = story_setup['scenario_order']
        self.break_scenario = story_setup['break_scenario']
        self.story_line = []
        self.callback = callback
        self.statistics = Statistic()
        self.generate_story_line()
        self.progress_story()

    def generate_story_line(self):
        # reset story line
        self.story_line = []
        if self.enable_start_screen:
            self.story_line.append({
                'type': ScreenType.START_SCREEN
            })
        if self.enable_random:
            sequence = [i for i in range(len(self.scenarios))]
            random.shuffle(sequence)
        else:
            sequence = self.scenario_order
            # we will reverse this again at the end
            sequence.reverse()
        logger.info(f'start a new experiment with {len(sequence)} scenarios with break time between each scenario')
        for index in range(len(sequence)):
            self.story_line.append({
                'index': index,
                'type': ScreenType.BREAK_TIME
            })
            self.story_line.append({
                'index': index,
                'type': ScreenType.EXPERIMENT_SCENARIO,
                'scenario_id': sequence[index]
            })
        # we reverse this to make it easier to be popped in self.progress_story()
        self.story_line = list(reversed(self.story_line))

    def progress_story(self, statistics=()):
        if statistics is not None and len(statistics) > 0:
            for data in statistics:
                self.statistics.add_data(data)

        # we reverse the story line to make it easier to pop
        # the first scenario in our loop
        if len(self.story_line) > 0:
            scene = self.story_line.pop()
            logger.info(f'playing {scene}')
            if scene['type'] == ScreenType.START_SCREEN:
                StartScreen(self.container, self.progress_story)
            if scene['type'] == ScreenType.EXPERIMENT_SCENARIO:
                logger.info(f'running a scenario id:{scene["scenario_id"]}')
                Scenario(
                    self.container,
                    self.scenarios[scene['scenario_id']],
                    self.scenario_interval,
                    self.progress_story
                ).play()
            elif scene['type'] == ScreenType.BREAK_TIME:
                logger.info(f'break time')
                Scenario(
                    self.container,
                    self.break_scenario,
                    self.break_interval,
                    self.progress_story
                ).play()
        else:
            logger.info(f'finish experiment')
            self.finish()

    def report_statistic(self):
        self.statistics.report()

    def finish(self):
        self.report_statistic()
        self.callback()
