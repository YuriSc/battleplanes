import csv
import glob
import json
import os
import pickle
import socket
from json.decoder import JSONDecodeError

import neat

from DataInputStream import DataInputStream
from DataOutputStream import DataOutputStream
from ExecTime import getTimerStat
from ExecTime import startTimer

BULLET_CODE = 299.0
ENEMY_CODE = 150.0
PLAYER_CODE = 1.0

HEIGHT_Y = 24
WIDTH_X = 80


# boom.height = 1 - по Y
# boom.width = 1 - по X

# bullet.height = 1 - по Y
# bullet.width = 1 - по X

# enemy.height = 3 - по Y
# enemy.width = 5 - по X

# player.height = 5 - по Y
# player.width = 4 - по X


class PlayerAction:
    MOVE_UP = "MOVE_UP"
    MOVE_DOWN = "MOVE_DOWN"
    SHOOT = "SHOOT"
    RESTART = "EXIT"
    NONE = "NONE"

    def __init__(self) -> None:
        super().__init__()
        self.action = PlayerAction.NONE

    def set(self, action):
        self.action = action

    def get(self):
        res = self.action
        self.action = PlayerAction.NONE
        return res


class PlaneClient:
    def __init__(self, address) -> None:
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        self.dos = DataOutputStream(self.socket)
        self.dis = DataInputStream(self.socket)
        self.playerAction = PlayerAction()

    def process_game_state_and_get(self):
        t = startTimer("process_game_state")
        try:
            self.dos.write_utf(self.playerAction.get())
            gsjson = self.dis.read_utf()
            return json.loads(gsjson)
        except JSONDecodeError as e:
            print(len(gsjson), gsjson)
            raise e
        finally:
            t.stop()

    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()


def setValByCoordinates(data, x, y, val):
    if x + y * WIDTH_X < len(data) and x >= 0 and y >= 0:
        data[x + y * WIDTH_X] = val


def encodeObject(data, object, code):
    for dx in range(object["width"] + 1):
        for dy in range(object["height"] + 1):
            setValByCoordinates(data, object['x'] + dx, object['y'] + dy, code)


def createInput(gameState):
    encoded = [0.0] * WIDTH_X * HEIGHT_Y
    encodeObject(encoded, gameState["player"], PLAYER_CODE)

    list(map(lambda x: encodeObject(encoded, x, ENEMY_CODE),
             [enemy for enemy in gameState["enemies"] if not enemy["destroyed"]]))
    list(map(lambda x: encodeObject(encoded, x, BULLET_CODE),
             [bullet for bullet in gameState["bullets"] if not bullet["destroyed"]]))

    return encoded
    # gameState["player"]["y"]
    # gameState["player"]["width"]
    # gameState["player"]["height"]
    # gameState["player"]["distance"]
    # gameState["enemies"][0]["x"]
    # gameState["enemies"][0]["y"]
    # gameState["enemies"][0]["destroyed"]
    # gameState["enemies"][0]["width"]
    # gameState["enemies"][0]["height"]
    # gameState["bullets"][0]["x"]
    # gameState["bullets"][0]["y"]
    # gameState["bullets"][0]["destroyed"]
    # gameState["bullets"][0]["width"]
    # gameState["bullets"][0]["height"]


def getDistance(gameState):
    return gameState["player"]["distance"]


def get_files_ordered_by_ctime_desc(pattern):
    list_of_files = glob.glob(pattern)
    if not list_of_files:
        return []
    return sorted(list_of_files, key=os.path.getctime, reverse=True)


def get_latest_file(pattern):
    """Returns the name of the latest (most recent) file
    of the joined path(s)"""
    files = get_files_ordered_by_ctime_desc(pattern)
    if not files:
        return None
    _, filename = os.path.split(files[0])
    return filename


class CheckpointerWithDelete(neat.Checkpointer):

    def save_checkpoint(self, config, population, species_set, generation):
        super().save_checkpoint(config, population, species_set, generation)
        self.delete_old_checkpoint(self.filename_prefix + "*")

    @staticmethod
    def delete_old_checkpoint(filename_pattern):
        list(map(os.remove, get_files_ordered_by_ctime_desc(filename_pattern)[5:]))


class NNPlayer:

    def __init__(self, host, port, restore_filename_prefix, is_ffn, config_path, csv_filename, winner_filename,
                 create_input=None) -> None:
        self.restore_filename_prefix = restore_filename_prefix
        self.restore_file_pattern = self.restore_filename_prefix + "*"
        self.is_ffn = is_ffn
        self.csv_filename = csv_filename
        self.winner_filename = winner_filename
        self.createInput = createInput if create_input is None else create_input
        # setup config
        config = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    config_path)

        # init NEAT
        file = get_latest_file(self.restore_file_pattern)

        if file:
            print(f"Loading population from file {file}")
            self.p = CheckpointerWithDelete.restore_checkpoint(file)
        else:
            print(f"Loading population from config")
            self.p = neat.Population(config)

        self.p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.p.add_reporter(stats)
        self.p.add_reporter(CheckpointerWithDelete(100, filename_prefix=self.restore_filename_prefix))

        self.csvfile = open(self.csv_filename, 'a', newline='')
        self.csv_writer = csv.writer(self.csvfile)
        self.client = PlaneClient((host, port))
        # keyboard.add_hotkey("up", lambda: playerAction.set(PlayerAction.MOVE_UP))
        # keyboard.add_hotkey("down", lambda: playerAction.set(PlayerAction.MOVE_DOWN))
        # keyboard.add_hotkey("tab", lambda: playerAction.set(PlayerAction.SHOOT))
        # keyboard.add_hotkey("esc", lambda: playerAction.set(PlayerAction.RESTART))

    def process(self) -> None:
        # run NEAT
        winner = self.p.run(self.run_generation)
        # while True:
        #     playerAction.set(PlayerAction.SHOOT)
        #     gameState = client.process_game_state_and_get()
        with open(self.winner_filename, 'wb') as output:
            pickle.dump(winner, output, 1)
        print("game done")
        self.client.close()
        self.csvfile.close()

    def run_generation(self, genomes, config):
        gen_t = startTimer("generation")
        self.csvfile.flush()

        for idx, genome in genomes:
            genom_t = startTimer("genome")
            # init genome
            if self.is_ffn:
                net = neat.nn.FeedForwardNetwork.create(genome, config)
            else:
                net = neat.nn.RecurrentNetwork.create(genome, config)
            genome.fitness = 0  # every genome is not successful at the start

            # the LOOP
            self.client.playerAction.set(PlayerAction.RESTART)
            self.client.process_game_state_and_get()
            prev_distance = 0
            while True:
                gameState = self.client.process_game_state_and_get()
                nn_t = startTimer("nn_process")
                input_data = self.createInput(gameState)
                curr_distance = getDistance(gameState)
                if curr_distance < prev_distance:
                    print(f"Genome {idx} end round with result {prev_distance}")
                    self.csv_writer.writerow([idx, prev_distance, ])
                    nn_t.stop()
                    genom_t.stop()
                    break
                prev_distance = curr_distance
                output = net.activate(input_data)
                i = output.index(max(output))

                if i == 0:
                    self.client.playerAction.set(PlayerAction.MOVE_UP)
                elif i == 1:
                    self.client.playerAction.set(PlayerAction.SHOOT)
                elif i == 2:
                    self.client.playerAction.set(PlayerAction.MOVE_DOWN)
                elif i == 3:
                    self.client.playerAction.set(PlayerAction.NONE)

                genome.fitness = float(curr_distance)
                nn_t.stop()
            genom_t.stop()
        gen_t.stop()
        print("Current statistics")
        list(map(
            lambda q: print(
                f"{q[0]}: at all={q[1][0]}, count={q[1][1]} ,avg={'N/A' if q[1][1] == 0 else q[1][0] / q[1][1]}"),
            getTimerStat()))
