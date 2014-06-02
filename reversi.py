class InvalidMoveError(Exception):
    pass


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "x = {}, y = {}".format(self.x, self.y)

    def is_in_board(self, coord):
        return min(self.x, self.y) >= 0 and max(self.x, self.y) < 8

class Board:
    def __init__(self, initial_state):
        EMPTY = ' '
        self.board = [[EMPTY for col in range(8)] for row in range(8)]
        for coords, value in initial_state:
            self[coord] = value

    def __getitem__(self, coord):
        return self.board[coord.y][coord.x]

    def __setitem__(self, coord, value):
        self.board[coord.y][coord.x] = value


class Player:
    def __init__(field):
        self.field = field
        self.result = 0


class Reversi:
    DIRECTIONS = [Coord(x, y)
                  for x, y in [(-1, -1), (-1, 0), (0, -1), (1, -1),
                               (-1, 1), (0, 1), (1, 0), (1, 1)]]
    BLACK = 'b'
    WHITE = 'w'
    EMPTY = ' '
    GAME_STATES = {
        "IN_PROGRESS": '<in-progress>',
        "BLACK_WINS": '<black-wins>',
        "WHITE_WINS": '<white-wins>',
        "TIE": '<tie>'
    }


    def __init__(self):
        self.black_player = Player(BLACK)
        self.white_player = Player(WHITE)
        self.board = Board({
            Coord(3, 3) : self.white_player.field,
            Coord(4, 4) : self.white_player.field,
            Coord(3, 4) : self.black_player.field,
            Coord(4, 3) : self.black_player.field
        })
        self._player = black_player

    def is_enemy_disc(self, coord):
        return (coord.is_in_board() and \
            self.board[coord] not in [self._player.field, EMPTY])

    def is_ally_disc(self, coord):
        return coord.is_in_board() and self.board[coord] == self._player.field

    def is_empty_disc(self, coord):
        return coord.is_in_board() and self.board[coord] == EMPTY

    def current_player(self):
        return self._player

    def current_player_discs(self):
        all_coords = [Coord(i, j) for i in range(8) for j in range(8)]
        return [coord for coord in all_coords
            if self.board[coord] == self._player.field]

    def change_current_player(self):
        if self._player is self.black_player:
            self._player = self.white_player
        else:
            self._player = self.black_player

    def available_fields(self):
        discs = self.current_player_discs()
        result = []
        for disc in discs:
            for d in DIRECTIONS:
                coord = disc + d
                while self.is_enemy_disc(coord):
                    coord += d
                if self.is_empty_disc(coord):
                    result += [coord]
        return result

    def valid_move(self, coord):
        return coord in available_fields

    def play(self, coord):
        if not valid_move(coord):
            raise InvalidMoveError("Not valid move")
        won_fields = [coord]

        for d in DIRECTIONS:
            current_coord = coord + d
            if self.is_enemy_disc(current_coord):
                possibly_won_fields = []
                while self.is_enemy_disc(current_coord):
                    possibly_won_fields.append(current_coord)
                    current_coord += d
                if self.is_ally_disc(current_coord):
                    won_fields += possibly_won_fields[:]

        for coord in won_fields:
            self.board[coord] = self.current_player()
            self._player.result = self.current_player_discs()

    def outcome(self):
        if not self.available_fields():
            self.change_current_player()
            if not self.available_fields():
                if self.white_player.result > self.black_player.result:
                    return GAME_STATES["WHITE_WINS"]
                elif self.white_player.result < self.black_player.result:
                    return GAME_STATES["BLACK_WINS"]
                else:
                    return GAME_STATES["TIE"]
        return GAME_STATES["IN_PROGRESS"]


