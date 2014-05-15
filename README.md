reversi
=======

A python implementation of the board game reversi - a course project for a python course @ FMI Sofia University.

Reversi is a classic turn based strategy game for two players. It also known as Othello. The game starts on a 8x8 board. Each player is referred to as light and dark, playing with pieces coloured appropriately (white and black).
###Rules:
- Play begins with a defined starting position of four pieces, as given below:
<br>![alt game start](http://cas.ee.ic.ac.uk/people/as999/FPTDesignComp/start_pos.jpg)
- The dark player makes the first move.The dark player must play a dark piece such that there is a continuous line (horizontal, vertical or diagonal) of light pieces between the new piece and another dark piece. The options of where dark can make a first move are illustrated by grey pieces below:
<br>![alt first move](http://cas.ee.ic.ac.uk/people/as999/FPTDesignComp/start_option.jpg)
- A player can make only a move that takes at least one of his opponent's pieces.
- If there are more than one directions in which there are only opponent's pieces followed by a piece of his own then all pieces in all such directions are taken.
- If a player cannot make a valid move then he passes the turn to the other player.
- The game ends when all fields have been taken or when neither player can make a turn. The winner is the player with the most pieces.

###Game modes:
- single player (vs AI) - with 3 difficulty levels - easy, medium and hard
- multiplayer - vs another player of his/her choice on the same server

###Additional info:
During the game both players can see the count of their and their opponent's pieces.
