from collections import OrderedDict


class GameHasEndedError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class InvalidCoordRangeStepError(Exception):
    pass


class Coord():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def is_in_board(self):
        return min(self.x, self.y) >= 0 and max(self.x, self.y) < 8

    def to(self, end, step):
        if (end.x - self.x) * step.y != (end.y - self.y) * step.x:
            raise InvalidCoordRangeStepError()

        result = []
        coord = self
        while coord != end:
            result.append(coord)
            coord += step
        return result


class Player:

    def __init__(self, field, AI=False):
        self.field = field
        self.result = 0
        self.AI = AI


class Reversi:
    BLACK = 'b'
    WHITE = 'w'
    EMPTY = ' '

    DIRECTIONS = [Coord(x, y)
                  for x, y in [(-1, -1), (-1, 0), (0, -1), (1, -1),
                               (-1, 1), (0, 1), (1, 0), (1, 1)]]

    GAME_STATES = {
        "IN_PROGRESS": 'In progress',
        "BLACK_WINS": 'Black wins',
        "WHITE_WINS": 'White wins',
        "TIE": 'Tie'
    }

    def __init__(self, single_player=False):
        self.black_player = Player(self.BLACK)
        self.white_player = Player(self.WHITE)
        self.board = OrderedDict((Coord(i, j), self.EMPTY)
                                 for i in range(8) for j in range(8))
        self.board[Coord(3, 3)] = self.white_player.field
        self.board[Coord(4, 4)] = self.white_player.field
        self.board[Coord(3, 4)] = self.black_player.field
        self.board[Coord(4, 3)] = self.black_player.field
        self.player = self.black_player
        self.black_player.result, self.white_player.result = 2, 2
        self.game_state = self.GAME_STATES['IN_PROGRESS']

    def is_enemy_disc(self, coord):
        return (coord.is_in_board() and
                self.board[coord] not in [self.player.field, self.EMPTY])

    def is_ally_disc(self, coord):
        return coord.is_in_board() and self.board[coord] == self.player.field

    def is_empty_disc(self, coord):
        return coord.is_in_board() and self.board[coord] == self.EMPTY

    def current_player_discs(self):
        all_coords = [Coord(i, j) for i in range(8) for j in range(8)]
        return [coord for coord in all_coords
                if self.board[coord] == self.player.field]

    def black_player_discs(self):
        all_coords = [Coord(i, j) for i in range(8) for j in range(8)]
        return [coord for coord in all_coords
                if self.board[coord] == self.black_player.field]

    def white_player_discs(self):
        all_coords = [Coord(i, j) for i in range(8) for j in range(8)]
        return [coord for coord in all_coords
                if self.board[coord] == self.white_player.field]

    def change_current_player(self):
        if self.player == self.black_player:
            self.player = self.white_player
        else:
            self.player = self.black_player

    def available_fields(self):
        discs = self.current_player_discs()
        result = []
        for disc in discs:
            for d in self.DIRECTIONS:
                coord = disc + d
                while self.is_enemy_disc(coord):
                    coord += d
                    if self.is_empty_disc(coord):
                        result += [coord]
        return result

    def is_valid_move(self, coord):
        return coord in self.available_fields()

    def play(self, coord):
        if self.game_state != self.GAME_STATES['IN_PROGRESS']:
            raise GameHasEndedError('Game has already ended')
        if not self.is_valid_move(coord):
            raise InvalidMoveError("Not valid move")

        won_fields = []
        for d in self.DIRECTIONS:
            current_coord = coord + d
            while self.is_enemy_disc(current_coord):
                current_coord += d

            if self.is_ally_disc(current_coord):
                won_fields += coord.to(current_coord, d)

        for coord in won_fields:
            self.board[coord] = self.player.field

        self.black_player.result = len(self.black_player_discs())
        self.white_player.result = len(self.white_player_discs())
        self.change_current_player()
        self.game_state = self.outcome()

    def outcome(self):
        if not self.available_fields():
            self.change_current_player()
            if not self.available_fields():
                if self.white_player.result > self.black_player.result:
                    return self.GAME_STATES["WHITE_WINS"]
                elif self.white_player.result < self.black_player.result:
                    return self.GAME_STATES["BLACK_WINS"]
                else:
                    return self.GAME_STATES["TIE"]
        return self.GAME_STATES["IN_PROGRESS"]

    def print_board(self):
        return '\n'.join(''.join(self.board[Coord(i, j)] for j in range(8))
                         for i in range(8))

    def game_info(self):
        player_map = {
            "b": "black",
            "w": "white"
        }
        return {
            "board": self.print_board(),
            "player": player_map[self.player.field],
            "state": self.game_state,
            "white_count": self.white_player.result,
            "black_count": self.black_player.result
        }
