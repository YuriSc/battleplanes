from EchoClientLib import NNPlayer
if __name__ == "__main__":
    # setup config
    player = NNPlayer('localhost', 50007, "neat-checkpoint-", False, "./config-recurrentnetwork.txt",
                      'genomes.csv', 'rn-winner.pkl')
    player.process()