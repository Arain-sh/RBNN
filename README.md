# RBNN
Reasoning Brain Neural Network Framework

# SuperBrain
Implementation of SuperBrain with documentation.

Ongoing project.

TODO (in order of priority)

Do something about the process leaking
File of constants that match the paper constants ?
OGS / KGS API ?
Use logging instead of prints ?

# CURRENTLY DOING

Optimizations
Clean code, create install script, write documentation

# DONE

Statistics (branch statistics)

Game that are longer than the threshold of moves are now used

MCTS

Tree search

Dirichlet noise to prior probabilities in the rootnode

Adaptative temperature (either take max or proportionally)

Sample random rotation or reflection in the dihedral group

Multithreading of search

Batch size evaluation to save computation

Dihedral group of board for more training samples

Learning without MCTS doesnt seem to work

Resume training

GTP on trained models (human.py, to plug with Sabaki)

Learning rate annealing (see this)

Better display for game (viewer.py, converting self-play games into GTP and then using Sabaki)

Make the 3 components (self-play, training, evaluation) asynchronous

Multiprocessing of games for self-play and evaluation

Models and training without MCTS

Evaluation

Tromp Taylor scoring

Dataset ring buffer of self-play games

Loading saved models

Database for self-play games

# LONG TERM PLAN ?

Compile my own version of Sabaki to watch games automatically while traning

Resignation ?

Training on a big computer / server once everything is ready ?

# Resources

The article for this code

Official AlphaGo Zero paper

Custom environment implementation using pachi_py following the implementation that was originally made on OpenAI Gym

Using PyTorch for the neural networks

Using Sabaki for the GUI

General scheme, cool design

Monte Carlo tree search explaination

Nice tree search implementation

# Statistics, check branch stats

For a 10 layers deep Resnet

9x9 board

soon

19x19 board

# Differences with the official paper

No resignation

PyTorch instead of Tensorflow

Python instead of (probably) C++ / C