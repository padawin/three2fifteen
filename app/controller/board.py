from app.controller.controller import Controller
from app.service.board import BoardService


class BoardController(Controller):
    def get(self):
        board = BoardService()
        return self.format_response(board.get())
