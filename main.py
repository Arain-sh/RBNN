"""
RBNN implementation.

Training
"""

from Coach import Coach
from binpacking.BinPacking import BinPacking as Game
from binpacking.pytorch.NNet import NNetWrapper as nn
from utils import dotdict


args = dotdict({
    'numIters': 1000,
    'numEps':   400,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 50,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': '/home/arain/data/checkpoint/',
    'load_model': True,
    'load_folder_file': ('/home/arain/data/checkpoint/model/', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 25,  # 20

})


if __name__ == "__main__":
    g = Game(10)
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0],
                             args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
