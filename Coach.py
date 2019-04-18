"""
This class executes the self-play + learning.

It uses the functions defined
in Game and NeuralNet. args are specified in main.py.
"""
from collections import deque
from Arena import Arena
from MCTS import MCTS
import numpy as np
from pytorch_classification.utils import Bar, AverageMeter
import time
import os
import sys
from pickle import Pickler, Unpickler
from random import shuffle
import pdb


class Coach():
    """
    This class executes the self-play + learning.

    It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """

    Buffer = [0]*200

    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.pnet = self.nnet.__class__(self.game)  # the competitor network
        self.args = args
        self.mcts = MCTS(self.game, self.nnet, self.args)
        self.trainExamplesHistory = []    # history of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False  # can be overriden in loadTrainExamples()

    def executePit(self, mctsChoose, board, bins):
        """
        Execute one episode of self-play.

        Starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.

        Returns:
            trainExamples: a list of examples of the form (canonicalBoard,pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually greater than 75 percent of
                           performence in the buffer and stored in it, else -1.

        """
        board = np.copy(board)
        bins = np.copy(bins)
#        pdb.set_trace()
        self.curPlayer = 1
        episodeStep = 0

        while True:
            episodeStep += 1
            canonicalBoard, canbins = self.game.getCanonicalForm(board,
                                                                 bins,
                                                                 self.curPlayer)
            temp = int(episodeStep < self.args.tempThreshold)

            pi = mctsChoose.getActionProb(canonicalBoard, canbins, temp=temp)
            # pdb.set_trace()

            if pi[-1] != 1:
                action = np.random.choice(len(pi), p=pi)
                i = action % 10
                d = int(((action-i)/10) % 2)
                tenxPy = action // 20
                x = (tenxPy//10) % 10
                y = tenxPy % 10
                move = (i, x, y, d)
                # pdb.set_trace()
                board, nextbins, self.curPlayer = self.game.getNextState(board,
                                                                         canbins,
                                                                         self.curPlayer,
                                                                         move)
                bins = nextbins
            else:
                r = self.game.getGameReward(canonicalBoard,
                                            canbins,
                                            self.curPlayer)
                return r

    def executeEpisode(self, mctsChoose):
        """
        Execute one episode of self-play.

        Starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.

        Returns:
            trainExamples: a list of examples of the form (canonicalBoard,pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually greater than 75 percent of
                           performence in the buffer and stored in it, else -1.

        """
        trainExamples = []
        board = self.game.getInitBoard()
        bins = self.game.getInitBins()
#        pdb.set_trace()
        self.curPlayer = 1
        episodeStep = 0

        while True:
            episodeStep += 1
            canonicalBoard, canbins = self.game.getCanonicalForm(board,
                                                                 bins,
                                                                 self.curPlayer)
            temp = int(episodeStep < self.args.tempThreshold)

            pi = mctsChoose.getActionProb(canonicalBoard, canbins, temp=temp)
            # pdb.set_trace()
            if pi is None:
                return [0, 0, -100]

            if pi[-1] != 1:
                action = np.random.choice(len(pi), p=pi)
                i = action % 10
                d = int(((action-i)/10) % 2)
                tenxPy = action // 20
                x = (tenxPy//10) % 10
                y = tenxPy % 10
                move = (i, x, y, d)
                # pdb.set_trace()
                board, nextbins, self.curPlayer = self.game.getNextState(board,
                                                                         canbins,
                                                                         self.curPlayer,
                                                                         move)
                bins = nextbins
                binBoard = [None]*10
                for i in range(10):
                    binBoard[i] = [0]*13

                for i in range(10):
                    binBoard[i] = np.append(board[i], bins[i])

                bBnpa = np.array(binBoard)
                r = self.game.getGameReward(board,
                                            bins,
                                            self.curPlayer)
                trainExamples.append([bBnpa, self.curPlayer, pi, r])
            else:
                r = self.game.getGameEnded(canonicalBoard,
                                           canbins, self.curPlayer)
                if r != 0:
                    # if r > self.Buffer[150]:
                    #     self.Buffer[0] = r
                    #     self.Buffer.sort()
                    binBoard = [None]*10
                    for i in range(10):
                        binBoard[i] = [0]*13
                    for i in range(10):
                        binBoard[i] = np.append(board[i], bins[i])
                    bBnpa = np.array(binBoard)
                    trainExamples.append([bBnpa, self.curPlayer, pi, r])
                    return [(x[0], x[2], r) for x in trainExamples]
                    # else:
                    #    return []

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each iteration.

        After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """
        for i in range(1, self.args.numIters+1):
            # bookkeeping
            print('------ITER ' + str(i) + '------')
            # examples of the iteration
            if not self.skipFirstSelfPlay or i > 1:
                iterationTrainExamples = deque([],
                                               maxlen=self.args.maxlenOfQueue)

                eps_time = AverageMeter()
                bar = Bar('Self Play', max=self.args.numEps)
                end = time.time()

                for eps in range(self.args.numEps):
                    self.mcts = MCTS(self.game, self.nnet, self.args)   # reset search tree
                    iterationTrainExamples += self.executeEpisode(self.mcts)

                    # bookkeeping + plot progress
                    eps_time.update(time.time() - end)
                    end = time.time()
                    bar.suffix = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps+1, maxeps=self.args.numEps, et=eps_time.avg,
                                                                                                               total=bar.elapsed_td, eta=bar.eta_td)
                    bar.next()
                bar.finish()

                # save the iteration examples to the history
                self.trainExamplesHistory.append(iterationTrainExamples)

            if len(self.trainExamplesHistory) > self.args.numItersForTrainExamplesHistory:
                print("len(trainExamplesHistory) =", len(self.trainExamplesHistory), " => remove the oldest trainExamples")
                self.trainExamplesHistory.pop(0)
            # backup history to a file
            # NB! the examples were collected using the model from the previous iteration, so (i-1)
            self.saveTrainExamples(i-1)

            # shuffle examples before training
            trainExamples = []
            for e in self.trainExamplesHistory:
                trainExamples.extend(e)
            shuffle(trainExamples)

            # training new network, keeping a copy of the old one
            self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            self.pnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            pmcts = MCTS(self.game, self.pnet, self.args)

            self.nnet.train(trainExamples)
            nmcts = MCTS(self.game, self.nnet, self.args)

            print('PITTING AGAINST PREVIOUS VERSION')

            pwins = 0
            nwins = 0
            draws = 0
            for i in range(self.args.arenaCompare):
                pitBoard = self.game.getInitBoard()
                pitBins = self.game.getInitBins()
                return_pmcts = self.executePit(pmcts, pitBoard, pitBins)
                return_nmcts = self.executePit(nmcts, pitBoard, pitBins)
                print("Pitting: Game ", i)
                if return_nmcts > return_pmcts:
                    nwins += 1
                elif return_nmcts < return_pmcts:
                    pwins += 1
                else:
                    draws += 1
            # arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
            #               lambda x: np.argmax(nmcts.getActionProb(x, temp=0)),
            #               self.game)
            # pwins, nwins, draws = arena.playGames(self.args.arenaCompare)
            print('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
            if pwins+nwins == 0 or float(nwins)/(pwins+nwins) < self.args.updateThreshold:
                print('REJECTING NEW MODEL')
                self.nnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            else:
                print('ACCEPTING NEW MODEL')
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename=self.getCheckpointFile(i))
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='best.pth.tar')

    def getCheckpointFile(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, iteration):
        folder = self.args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration)+".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed

    def loadTrainExamples(self):
        modelFile = os.path.join(self.args.load_folder_file[0], self.args.load_folder_file[1])
        examplesFile = modelFile+".examples"
        if not os.path.isfile(examplesFile):
            print(examplesFile)
            r = input("File with trainExamples not found. Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            print("File with trainExamples found. Read it.")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            f.closed
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True
