import pytest

from app.game import board


@pytest.mark.parametrize(
    "board_content,expected_return",
    [
        [
            [],
            []
        ],
        [
            [{'x': 8, 'y': 4, 'value': 10}],
            [{'x': 8, 'y': 4, 'value': 10}]
        ],
        [
            [{'x': 12, 'y': 5, 'value': 10}, {'x': 8, 'y': 4, 'value': 10}],
            [{'x': 8, 'y': 4, 'value': 10}, {'x': 12, 'y': 5, 'value': 10}]
        ]
    ],
    ids=["Empty Board",
         "Non empty Board",
         "Return sorted"]
)
def test_get_grid(board_content, expected_return):
    boardInstance = board.Board()
    for token in board_content:
        boardInstance.set_placement(token['x'], token['y'], token['value'])
    assert boardInstance.get_grid() == expected_return


def test_board_rim():
    boardInstance = board.Board()
    assert boardInstance.rim == set()
    boardInstance.set_placement(7, 8, 9)
    assert boardInstance.rim == {(6, 8), (8, 8), (7, 7), (7, 9)}
    boardInstance.set_placement(7, 9, 9)
    assert boardInstance.rim == {
        (6, 8), (8, 8), (7, 7), (6, 9), (8, 9), (7, 10)
    }
    boardInstance.set_placement(0, 0, 9)
    assert boardInstance.rim == {
        (6, 8), (8, 8), (7, 7), (6, 9), (8, 9), (7, 10), (0, 1), (1, 0)
    }
    boardInstance.set_placement(7, 8, 9)
    assert boardInstance.rim == {
        (6, 8), (8, 8), (7, 7), (6, 9), (8, 9), (7, 10), (0, 1), (1, 0)
    }

    board2 = board.Board(data=[
        {'x': 7, 'y': 9, 'value': 9},
        {'x': 0, 'y': 0, 'value': 9},
        {'x': 7, 'y': 8, 'value': 9}
    ])
    assert board2.rim == boardInstance.rim


@pytest.mark.parametrize(
    "board_content,x,y,expected_return",
    [
        [
            [],
            1, 1, None
        ],
        [
            [],
            -1, -1, None
        ],
        [
            [],
            100, 100, None
        ],
        [
            [{'x': 8, 'y': 12, 'value': 5}],
            8, 12, 5
        ]
    ],
    ids=["Empty Board",
         "Out of bound negative coordinates",
         "Out of bound positive coordinates",
         "OK"]
)
def test_get_token_at(board_content, x, y, expected_return):
    boardInstance = board.Board()
    for token in board_content:
        boardInstance.set_placement(token['x'], token['y'], token['value'])
    assert boardInstance.get_token_at(x, y) == expected_return


@pytest.mark.parametrize(
    "board_content,expected_is_empty",
    [
        [
            [],
            True
        ],
        [
            [{'x': 8, 'y': 12, 'value': 5}],
            False
        ]
    ],
    ids=["Empty Board",
         "OK"]
)
def test_is_empty(board_content, expected_is_empty):
    boardInstance = board.Board()
    for token in board_content:
        boardInstance.set_placement(token['x'], token['y'], token['value'])
    assert boardInstance.is_empty() == expected_is_empty


def test_is_empty_initial_data():
    boardInstance = board.Board([{'x': 8, 'y': 12, 'value': 5}])
    assert boardInstance.is_empty() == False


@pytest.mark.parametrize(
    "x,y,expected_multiplier",
    [
        [4, 4, 2],
        [1, 4, 3],
        [4, 3, 0],
        [0, 7, 0]
    ],
    ids=["Double",
         "Triple",
         "None",
         "Bis"]
)
def test_multiplier(x, y, expected_multiplier):
    boardInstance = board.Board()
    multiplier = boardInstance.get_multiplier(x, y)
    assert multiplier == expected_multiplier
