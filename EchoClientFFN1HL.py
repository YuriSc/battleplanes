from EchoClientLib import NNPlayer
if __name__ == "__main__":
    # setup config
    player = NNPlayer('localhost', 50007, "ffn1hl-neat-checkpoint-", True, "./config-feedforward-hl.txt",
                      'genomes_ffn1hl.csv', 'ffn1hl-winner.pkl')
    player.process()