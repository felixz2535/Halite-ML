import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import secrets
import logging
import random
import math
import numpy as np
import time


game = hlt.Game()
game.ready("Bot")

map_settings = {
    32: 400,
    40: 425,
    48: 450,
    56: 475,
    64: 500
}


TOTAL_TURNS = 50
SAVE_THRESHOLD = 4100
MAX_SHIPS = 1
SIGHT_DISTANCE = 16

direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
training_data = []

while True:

    game.update_frame()

    me = game.me


    game_map = game.game_map


    command_queue = []



    dropoff_positions = [d.position for d in list(me.get_dropoffs()) + [me.shipyard]]
    ship_positions = [s.position for s in list(me.get_ships())]

    for ship in me.get_ships():

        logging.info(f"{ship.position},{ship.position + Position(-3, 3)}")
        logging.info(f"{game_map[ship.position + Position(-3, 3)]}")

        size = SIGHT_DISTANCE
        surroundings = []
        for y in range(-1*size, size+1):
            row = []
            for x in range(-1*size, size+1):
                current_cell = game_map[ship.position + Position(x, y)]

                if current_cell.position in dropoff_positions:

                    drop_friend_foe = 1
                else:

                    drop_friend_foe = -1

                if current_cell.position in ship_positions:
                    ship_friend_foe = 1
                else:
                    ship_friend_foe = -1

                halite = round(current_cell.halite_amount/constants.MAX_HALITE, 2)

                a_ship = current_cell.ship
                a_structure = current_cell.structure

                if halite is None:
                    halite = 0
                if a_ship is None:
                    a_ship = 0
                else:
                    a_ship = round(ship_friend_foe * (a_ship.halite_amount/constants.MAX_HALITE), 2)

                if a_structure is None:
                    a_structure = 0
                else:
                    a_structure = drop_friend_foe

                amounts = (halite, a_ship, a_structure)


                row.append(amounts)
            surroundings.append(row)

        # np.save(f"game_play/{game.turn_number}.npy", surroundings)
        choice = secrets.choice(range(len(direction_order)))
        training_data.append([surroundings, choice])
        command_queue.append(ship.move(direction_order[choice]))

    if len(me.get_ships()) < MAX_SHIPS:
        if me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
            command_queue.append(me.shipyard.spawn())


    if game.turn_number == TOTAL_TURNS:
        if me.halite_amount >= SAVE_THRESHOLD:
            np.save(f'training_data/{me.halite_amount}-{int(time.time()*1000)}.npy', training_data)

    game.end_turn(command_queue)

