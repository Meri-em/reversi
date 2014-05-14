reversi
=======

A python implementation of the board game reversi - a course project for a python course @ FMI Sofia University.

Reversi is a classic turn based strategy game for two players. It also known as Othello. The game starts on a 8x8 board.
###Rules:
- The games starts in this position
      <br><img alt="game start" width="200" height="200">
- If a player puts a piece so that between that piece and another one of his pieces there are only enemy pieces without an empty field then those enemy pieces become his own.
      <br><img alt="taken pieces example" width="200" height="200">
- A player can make only a move that takes at least one of his opponent's pieces.
- If there are more than one directions in which there are only opponent's pieces followed by a piece of his own then all pieces in all such directions are taken.
- If a player cannot make a valid move then he passes the turn to the other player.
- The game ends when all fields have been taken or when neither player can make a turn. The winner is the player with the most pieces.

###Game modes:
- single player (vs AI) - with 3 difficulty levels - easy, medium and hard
- multiplayer - vs another player of his/her choice on the same server

###Additional info:
During the game both players can see the count of their and their opponent's pieces.
