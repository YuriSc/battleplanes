from EchoClientLib import NNPlayer
if __name__ == "__main__":
    # setup config
    player = NNPlayer('localhost', 50007, "ffn-neat-checkpoint-", True, "./config-feedforward-new.txt",
                      'genomes_ffn.csv', 'ffn-winner.pkl')
    player.process()
