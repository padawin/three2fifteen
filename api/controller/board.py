from api.controller.controller import Controller
from api.service.board import BoardService


class BoardController(Controller):
    def get(self):
        board = BoardService()
        print(board, board.get())
        return self.format_response(board.get())
