from EchoClientLib import NNPlayer
if __name__ == "__main__":
    # setup config
    player = NNPlayer('localhost', 50007, "rn1hl-neat-checkpoint-", False, "./config-recurrentnetwork-1hl.txt",
                      'genomes_rn1hl.csv', 'rn1hl-winner.pkl')
    player.process()