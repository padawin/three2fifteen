from app.game.board import Board


class BoardService(object):
    @staticmethod
    def _make_cell(x, y, value):
        if value == 0:
            cell_type = 'simple'
        elif value == 2:
            cell_type = 'double'
        elif value == 3:
            cell_type = 'triple'
        elif value == 'b':
            cell_type = 'bis'
        return {'x': x, 'y': y, 'type': cell_type}

    def get(self):
        board = Board()
        return [BoardService._make_cell(x, y, cell)
                for y, row in enumerate(board.multipliers)
                for x, cell in enumerate(row)]
