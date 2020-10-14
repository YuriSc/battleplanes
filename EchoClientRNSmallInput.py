from EchoClientLib import NNPlayer
from EchoClientLib import WIDTH_X
from EchoClientLib import HEIGHT_Y

def small_input(gameState):
    encoded = [0.0] * 2 * HEIGHT_Y
    # encodeObject(encoded, gameState["player"], PLAYER_CODE)
    #
    # list(map(lambda x: encodeObject(encoded, x, ENEMY_CODE),
    #          [enemy for enemy in gameState["enemies"] if not enemy["destroyed"]]))
    # list(map(lambda x: encodeObject(encoded, x, BULLET_CODE),
    #          [bullet for bullet in gameState["bullets"] if not bullet["destroyed"]]))

    return encoded


if __name__ == "__main__":
    # setup config
    player = NNPlayer('localhost', 50007, "rn1hlsi-neat-checkpoint-", False, "./config-recurrentnetwork-1hlsi.txt",
                      'genomes_rn1hlsi.csv', 'rn1hlsi-winner.pkl', create_input=small_input)
    player.process()