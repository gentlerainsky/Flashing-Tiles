from config.random_words import words


calibrate_time = 0
scenarios = [{
    "scene": {
        "word_list": words,
        "word_change_frequency": 1,
    },
    "tiles": [
        {'x': 'middle', 'y': 'top', 'frequency': 6},
        {'x': 'left', 'y': 'middle', 'frequency': 6.57},
        {'x': 'right', 'y': 'middle', 'frequency': 7.5},
        {'x': 'middle', 'y': 'bottom', 'frequency': 8.57}
    ]
}, {
    "scene": {
        "word_list": None,
    },
    "tiles": [
        {'x': 'middle', 'y': 'top', 'frequency': 6},
        {'x': 'left', 'y': 'middle', 'frequency': 6.57},
        {'x': 'right', 'y': 'middle', 'frequency': 7.5},
        {'x': 'middle', 'y': 'bottom', 'frequency': 8.57}
    ]
}, {
    "scene": {
        "word_list": None,
    },
    "tiles": []
}]

break_scenario = {
    "word_list": None,
    "tiles": []
}

story_setup = {
    "enable_start_screen": True,
    "enable_random": True,
    "scenario_order": [],
    # in second
    "break_interval": 5,
    # in second
    "scenario_interval": 10,
    "scenarios": scenarios,
    "break_scenario": break_scenario
}

# maximum frame per second for Kivy this will affect how often
# Clock.schedule_interval check if it needs to run its callback
MAX_FPS = 200
