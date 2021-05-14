from api.game.board import Board


class BoardService(object):
    @staticmethod
    def _make_cell(x, y, multiplier, effect):
        e = 'simple'
        if effect == 'b':
            e = 'bis'

        m = 'simple'
        if multiplier == 2:
            m = 'double'
        elif multiplier == 3:
            m = 'triple'
        return {'x': x, 'y': y, 'multiplier': m, 'effect': e}

    def get(self):
        board = Board()
        return [BoardService._make_cell(x, y, multiplier, effect)
                for y, (multipliers, effects) in enumerate(zip(board.multipliers, board.effects))
                for x, (multiplier, effect) in enumerate(zip(multipliers, effects))]
