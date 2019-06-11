# KMNBox
A silly math problem in a box


1. Player 1 and Player 2 take alternating turns placing white and black stones on a k x m x n grid, k,m,n >= 2. On each turn, a player drops a stone on one of the k x m available slots, such that the stone falls to the very bottom (i.e in Connect4). The game continues until two stones of the same color are placed horizontally or vertically adjacent to each other. The first person who cannot place a stone or places two stones adjacent to each other loses the game.

Does either player have a winning strategy?

—

2. (general case) Player 1 and Player 2 take alternating turns placing white and black stones on a k x m x n grid, k,m,n >= 2. On each turn, a player freely places a stone on one of the k x m x n available slots. The game continues until two stones of the same color are placed horizontally or vertically adjacent to each other. The first person who cannot place a stone or places two stones adjacent to each other loses the game.

Does either player have a winning strategy?


# Solutions

For Q1 it can be proven that for a k x m x n grid, if either one of the dimensions is even then the game is a forced win for Player 2. The theory is that the game is a forced win for Player 2, but this has to be proven for a odd x odd x odd grid. The minimax code in this repository is an attempt to solve this problem.

For Q2 haven't started lol
