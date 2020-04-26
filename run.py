import os
import secrets

MAX_TURNS = 50

map_settings = {
    32: 400,
    40: 425,
    48: 450,
    56: 475,
    64: 500
}


while True:
    map_size = secrets.choice(list(map_settings.keys()))
    commands = [f'halite.exe --replay-directory replays/ --no-timeout --turn-limit {MAX_TURNS} -vvv -v --width {map_size} --height {map_size} "python bot2.py" "python bot2.py"',
                f'halite.exe --replay-directory replays/ --no-timeout --turn-limit {MAX_TURNS} -vvv -v --width {map_size} --height {map_size} "python bot2.py" "python bot2.py" "python bot2.py" "python bot2.py"'
                ]
    command = secrets.choice(commands)
    os.system(command)
