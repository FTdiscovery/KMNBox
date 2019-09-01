# KMNBox
Silly math problems in a box
proposed by adam bertelli gordon chi and victor luo


1. Player 1 and Player 2 take alternating turns placing white and black stones on a k x m x n grid, k,m,n >= 2. On each turn, a player drops a stone on one of the k x m available slots, such that the stone falls to the very bottom (i.e in Connect4). The game continues until two stones of the same color are placed horizontally or vertically adjacent to each other. The first person who cannot place a stone or places two stones of the same colour adjacent to each other loses the game.

Does either player have a winning strategy?

—

2. (general case) Player 1 and Player 2 take alternating turns placing white and black stones on a k x m x n grid, k,m,n >= 2. On each turn, a player freely places a stone on one of the k x m x n available slots. The game continues until two stones of the same color are placed horizontally or vertically adjacent to each other. The first person who cannot place a stone or places two stones of the same colouradjacent to each other loses the game.

Does either player have a winning strategy?


# Solutions

For Q1 it can be proven that for a k x m x n grid, if either one of the dimensions is even then the game is a forced win for Player 2. The theory is that the game is a forced win for Player 2, but this has to be proven for a odd x odd x odd grid. The minimax code in this repository is an attempt to solve this problem.

<b>case 1</b>: n is even. then the winning strategy for player 2 is to place a stone above the move player 1 makes. <br>
<b>case 2</b>: n is odd, but at least one of k or m is even. then if player 1 plays on a blank slot, player 2 places its stone on the slot rotated 180 degrees around the center of the kxm board. if player 1 does not play on a blank slot, then player 2 places a stone above the move player 1 makes.<br>
<b>case 3</b>: k, m, n are all odd. then tbc

For Q2 reflection works if >=1 dimension of the grid is even.
