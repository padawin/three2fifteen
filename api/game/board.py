class Board(object):
    def __init__(self, data=[]):
        n = None
        self.grid = [
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n],
            [n, n, n, n, n, n, n, n, n, n, n, n, n, n, n]
        ]

        self.multipliers = [
            [0,   0,  0, 0, 0, 0, 0, 'b', 0, 0, 0, 0, 0,  0,  0],
            [0,  'b', 0, 0, 3, 0, 0,  0,  0, 0, 3, 0, 0, 'b', 0],
            [0,   0,  0, 0, 0, 0, 0,  0,  0, 0, 0, 0, 0,  0,  0],
            [0,   0,  0, 0, 0, 0, 0,  2,  0, 0, 0, 0, 0,  0,  0],
            [0,   3,  0, 0, 2, 0, 0,  0,  0, 0, 2, 0, 0,  3,  0],
            [0,   0,  0, 0, 0, 0, 0,  0,  0, 0, 0, 0, 0,  0,  0],
            [0,   0,  0, 0, 0, 0, 0,  0,  0, 0, 0, 0, 0,  0,  0],
            ['b', 0,  0, 2, 0, 0, 0,  2,  0, 0, 0, 2, 0,  0, 'b'],
            [0,   0,  0, 0, 0, 0, 0,  0,  0, 0, 0, 0, 0,  0,  0],
            [0,   0,  0, 0, 0, 0, 0,  0,  0, 0, 0, 0, 0,  0,  0],
            [0,   3,  0, 0, 2, 0, 0,  0,  0, 0, 2, 0, 0,  3,  0],
            [0,   0,  0, 0, 0, 0, 0,  2,  0, 0, 0, 0, 0,  0,  0],
            [0,   0,  0, 0, 0, 0, 0,  0,  0, 0, 0, 0, 0,  0,  0],
            [0,  'b', 0, 0, 3, 0, 0,  0,  0, 0, 3, 0, 0, 'b', 0],
            [0,   0,  0, 0, 0, 0, 0, 'b', 0, 0, 0, 0, 0,  0,  0]
        ]
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.rim = set()
        self.count_tokens = len(data)
        for token in data:
            self.set_placement(**token)

    def get_grid(self):
        return [
            {'x': x, 'y': y, 'value': value}
            for y, row in enumerate(self.grid)
            for x, value in enumerate(self.grid[y])
            if value is not None
        ]

    def get_token_at(self, x, y, raise_error=False):
        if x < 0 or y < 0:
            if raise_error:
                raise ValueError()
            return None
        try:
            return self.grid[y][x]
        except IndexError:
            if raise_error:
                raise ValueError()
            return None

    def is_bis(self, x, y):
        return self.multipliers[y][x] == 'b'

    def set_placement(self, x, y, value):
        self.grid[y][x] = value
        self.count_tokens += 1
        for d in ((0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)):
            key = (x + d[0], y + d[1])
            try:
                token = self.get_token_at(key[0], key[1], raise_error=True)
            except ValueError:
                continue
            if token is None:
                self.rim.add(key)
            elif key in self.rim:
                self.rim.remove(key)

    def is_empty(self):
        return self.count_tokens == 0

    def coordinates_in_bound(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_multiplier(self, x, y):
        return (self.multipliers[y][x]
                if type(self.multipliers[y][x]) is int
                else 0)
