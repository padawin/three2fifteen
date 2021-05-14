import pytest

from api.game import rules
from api.game import board


@pytest.mark.parametrize(
    "board_content,x,y,token_value,valid",
    [
        # valid
        # Single token middle
        [[], 7, 7, 10, True],
        # Single token not middle
        [[], 1, 1, 10, True],
        # Valid top
        [
            [
                {'x': 1, 'y': 1, 'value': 9},
                {'x': 1, 'y': 2, 'value': 1}
            ],
            1, 0, 5, True
        ],
        # Valid bottom
        [
            [
                {'x': 0, 'y': 0, 'value': 4},
                {'x': 0, 'y': 1, 'value': 8}
            ],
            0, 2, 3, True
        ],
        # Valid left
        [
            [
                {'x': 1, 'y': 0, 'value': 1},
                {'x': 2, 'y': 0, 'value': 1}
            ],
            0, 0, 13, True
        ],
        # Valid right
        [
            [
                {'x': 0, 'y': 1, 'value': 4},
                {'x': 1, 'y': 1, 'value': 4}
            ],
            2, 1, 7, True
        ],

        # Valid 2 top
        [[{'x': 1, 'y': 2, 'value': 1}], 1, 1, 5, True],
        # Valid 2 bottom
        [[{'x': 2, 'y': 1, 'value': 8}], 2, 2, 3, True],
        # Valid 2 left
        [[{'x': 2, 'y': 0, 'value': 1}], 1, 0, 13, True],
        # Valid 2 right
        [[{'x': 1, 'y': 1, 'value': 4}], 2, 1, 7, True],

        # Valid 2 15 top
        [[{'x': 1, 'y': 2, 'value': 1}], 1, 1, 14, True],
        # Valid 2 15 bottom
        [[{'x': 2, 'y': 1, 'value': 8}], 2, 2, 7, True],
        # Valid 2 15 left
        [[{'x': 2, 'y': 0, 'value': 1}], 1, 0, 14, True],
        # Valid 2 15 right
        [[{'x': 1, 'y': 1, 'value': 4}], 2, 1, 11, True],

        # Valid vertical
        [
            [
                {'x': 0, 'y': 0, 'value': 1},
                {'x': 2, 'y': 0, 'value': 1}
            ],
            1, 0, 13, True
        ],
        # Valid horizontal
        [
            [
                {'x': 0, 'y': 1, 'value': 4},
                {'x': 2, 'y': 1, 'value': 4}
            ],
            1, 1, 7, True
        ],

        # Valid cross
        [
            [
                {'x': 0, 'y': 1, 'value': 4},
                {'x': 1, 'y': 0, 'value': 4},
                {'x': 2, 'y': 1, 'value': 4},
                {'x': 1, 'y': 2, 'value': 4}
            ],
            1, 1, 7, True
        ],


        # invalid
        # Already used space
        [
            [{'x': 1, 'y': 0, 'value': 5}],
            1, 0, 10, False
        ],

        # Overflow
        # 15 overflow vertical top
        [
            [{'x': 1, 'y': 0, 'value': 6}],
            1, 1, 10, False
        ],
        # 15 overflow vertical bottom
        [
            [{'x': 1, 'y': 2, 'value': 6}],
            1, 1, 10, False
        ],
        # 15 overflow horizontal left
        [
            [{'x': 0, 'y': 1, 'value': 6}],
            1, 1, 10, False
        ],
        # 15 overflow horizontal right
        [
            [{'x': 2, 'y': 1, 'value': 6}],
            1, 1, 10, False
        ],

        # 15 overflow vertical
        [
            [
                {'x': 1, 'y': 0, 'value': 9},
                {'x': 1, 'y': 2, 'value': 1}
            ],
            1, 1, 6, False
        ],
        # 15 overflow horizontal
        [
            [
                {'x': 0, 'y': 1, 'value': 4},
                {'x': 2, 'y': 1, 'value': 8}
            ],
            1, 1, 5, False
        ],

        # > 3 tokens in a row
        # Too many tokens top
        [
            [
                {'x': 1, 'y': 0, 'value': 1},
                {'x': 1, 'y': 1, 'value': 1},
                {'x': 1, 'y': 2, 'value': 1}
            ],
            1, 3, 1, False
        ],
        # Too many tokens bottom
        [
            [
                {'x': 1, 'y': 1, 'value': 1},
                {'x': 1, 'y': 2, 'value': 1},
                {'x': 1, 'y': 3, 'value': 1}
            ],
            1, 0, 1, False
        ],
        # Too many tokens left
        [
            [
                {'x': 0, 'y': 0, 'value': 1},
                {'x': 1, 'y': 0, 'value': 1},
                {'x': 2, 'y': 0, 'value': 1}
            ],
            3, 0, 1, False
        ],
        # Too many tokens right
        [
            [
                {'x': 1, 'y': 0, 'value': 1},
                {'x': 2, 'y': 0, 'value': 1},
                {'x': 3, 'y': 0, 'value': 1}
            ],
            0, 0, 1, False
        ],
        # Too many tokens vertical
        [
            [
                {'x': 1, 'y': 0, 'value': 1},
                {'x': 1, 'y': 1, 'value': 1},
                {'x': 1, 'y': 3, 'value': 1}
            ],
            1, 2, 1, False
        ],
        # Too many tokens horizontal
        [
            [
                {'x': 0, 'y': 0, 'value': 1},
                {'x': 1, 'y': 0, 'value': 1},
                {'x': 3, 'y': 0, 'value': 1}
            ],
            2, 0, 1, False
        ],

        # Out of bound coordinates negative
        [[], -1, -1, 1, False],
        # Out of bound coordinates overflow
        [[], 15, 15, 1, False]
    ],
    # valids
    ids=['Single token middle',
         'Single token',
         'Valid top',
         'Valid bottom',
         'Valid left',
         'Valid right',

         'Valid 2 top',
         'Valid 2 bottom',
         'Valid 2 left',
         'Valid 2 right',

         'Valid 2 15 top',
         'Valid 2 15 bottom',
         'Valid 2 15 left',
         'Valid 2 15 right',

         'Valid vertical',
         'Valid horizontal',

         'Valid cross',

         # invalids
         'Already used space',

         '15 overflow vertical top',
         '15 overflow vertical bottom',
         '15 overflow horizontal left',
         '15 overflow horizontal right',

         '15 overflow vertical',
         '15 overflow horizontal',

         'Too many tokens top',
         'Too many tokens bottom',
         'Too many tokens left',
         'Too many tokens right',
         'Too many tokens vertical',
         'Too many tokens horizontal',

         'Out of bound coordinates negative',
         'Out of bound coordinates overflow']
)
def test_analyse_placement(board_content, x, y, token_value, valid):
    boardInstance = board.Board()
    for token in board_content:
        boardInstance.set_placement(token['x'], token['y'], token['value'])

    analyse = rules.analyse_placement(boardInstance, x, y, token_value)
    assert analyse['valid'] == valid


@pytest.mark.parametrize(
    "board_content,play,complete,score_play,scores,valid,valid_reason",
    [
        # valid
        # 1 Token first turn center
        [
            [],
            [{'x': 7, 'y': 7, 'value': 1}],
            False, 1,
            [],
            True, "OK"
        ],
        # 2 Token first turn center
        [
            [],
            [{'x': 7, 'y': 7, 'value': 1}, {'x': 6, 'y': 7, 'value': 1}],
            False, 2,
            [{'score': 2, 'count': 2}],
            True, "OK"
        ],
        # 3 Token first turn center
        [
            [],
            [
                {'x': 7, 'y': 6, 'value': 3},
                {'x': 7, 'y': 7, 'value': 4},
                {'x': 7, 'y': 8, 'value': 8}
            ],
            True, 15,
            [{'score': 15, 'count': 3}],
            True, "OK"
        ],

        # valid from paper rules
        # no 1
        [
            [{'x': 0, 'y': 0, 'value': 10}],
            [{'x': 1, 'y': 0, 'value': 3}],
            False, 3,
            [{'score': 13, 'count': 2}],
            True, "OK"
        ],

        # no 2
        [
            [
                {'x': 0, 'y': 0, 'value': 1},
                {'x': 0, 'y': 1, 'value': 10},
                {'x': 0, 'y': 2, 'value': 4},
                {'x': 1, 'y': 1, 'value': 3}
            ],
            [{'x': 1, 'y': 2, 'value': 9}],
            False, 9,
            [{'score': 12, 'count': 2}, {'score': 13, 'count': 2}],
            True, "OK"
        ],

        # no 3
        [
            [
                {'x': 1, 'y': 0, 'value': 1},
                {'x': 1, 'y': 1, 'value': 10},
                {'x': 2, 'y': 1, 'value': 3},
                {'x': 1, 'y': 2, 'value': 4},
                {'x': 2, 'y': 2, 'value': 9}
            ],
            [{'x': 0, 'y': 2, 'value': 2}],
            True, 2,
            [{'score': 15, 'count': 3}],
            True, "OK"
        ],

        # no 4
        [
            [
                {'x': 1, 'y': 0, 'value': 1},
                {'x': 1, 'y': 1, 'value': 10},
                {'x': 2, 'y': 1, 'value': 3},
                {'x': 0, 'y': 2, 'value': 2},
                {'x': 1, 'y': 2, 'value': 4},
                {'x': 2, 'y': 2, 'value': 9}
            ],
            [{'x': 2, 'y': 0, 'value': 3}],
            True, 3,
            [{'score': 15, 'count': 3}, {'score': 4, 'count': 2}],
            True, "OK"
        ],

        # no 5
        [
            [
                {'x': 0, 'y': 0, 'value': 5},
                {'x': 2, 'y': 0, 'value': 9},
                {'x': 3, 'y': 0, 'value': 5},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 7},
                {'x': 2, 'y': 1, 'value': 6},
                {'x': 0, 'y': 2, 'value': 8},
                {'x': 1, 'y': 2, 'value': 7}
            ],
            [{'x': 2, 'y': 2, 'value': 0}],
            True, 0,
            [{'score': 15, 'count': 3}, {'score': 15, 'count': 3}],
            True, "OK"
        ],

        # no 6
        [
            [{'x': 1, 'y': 0, 'value': 9}, {'x': 2, 'y': 0, 'value': 5}],
            [{'x': 0, 'y': 1, 'value': 7}, {'x': 1, 'y': 1, 'value': 6}],
            False, 13,
            [{'score': 15, 'count': 2}, {'score': 13, 'count': 2}],
            True, "OK"
        ],

        # no 7
        [
            [{'x': 0, 'y': 1, 'value': 10}, {'x': 1, 'y': 1, 'value': 3}],
            [{'x': 0, 'y': 0, 'value': 1}, {'x': 0, 'y': 2, 'value': 4}],
            True, 5,
            [{'score': 15, 'count': 3}],
            True, "OK"
        ],

        # no 8
        [
            [{'x': 0, 'y': 0, 'value': 15}, {'x': 0, 'y': 1, 'value': 0}],
            [{'x': 1, 'y': 0, 'value': 0}, {'x': 2, 'y': 0, 'value': 0}],
            True, 0,
            [{'score': 15, 'count': 3}],
            True, "OK"
        ],

        # no 9
        [
            [
                {'x': 0, 'y': 0, 'value': 6},
                {'x': 1, 'y': 0, 'value': 7},
                {'x': 1, 'y': 1, 'value': 1},
                {'x': 1, 'y': 2, 'value': 7}
            ],
            [{'x': 2, 'y': 1, 'value': 12}, {'x': 2, 'y': 2, 'value': 0}],
            False, 12,
            [
                {'count': 2, 'score': 13},
                {'count': 2, 'score': 7},
                {'count': 2, 'score': 12}
            ],
            True, "OK"
        ],

        # no 11
        [
            [
                {'x': 2, 'y': 0, 'value': 9},
                {'x': 3, 'y': 0, 'value': 5},
                {'x': 1, 'y': 1, 'value': 7},
                {'x': 2, 'y': 1, 'value': 6}
            ],
            [{'x': 0, 'y': 0, 'value': 5}, {'x': 0, 'y': 1, 'value': 2}],
            False, 7,
            [{'count': 3, 'score': 15}, {'count': 2, 'score': 7}],
            True, "OK"
        ],

        # no 13
        [
            [
                {'x': 0, 'y': 0, 'value': 5},
                {'x': 2, 'y': 0, 'value': 9},
                {'x': 3, 'y': 0, 'value': 5},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 7},
                {'x': 2, 'y': 1, 'value': 6}
            ],
            [{'x': 0, 'y': 2, 'value': 8}, {'x': 1, 'y': 2, 'value': 7}],
            False, 15,
            [
                {'count': 3, 'score': 15},
                {'count': 2, 'score': 14},
                {'count': 2, 'score': 15}
            ],
            True, "OK"
        ],

        # no 14
        [
            [
                {'x': 2, 'y': 0, 'value': 12},
                {'x': 1, 'y': 1, 'value': 6},
                {'x': 2, 'y': 1, 'value': 2},
                {'x': 1, 'y': 2, 'value': 5}
            ],
            [{'x': 0, 'y': 2, 'value': 9}, {'x': 2, 'y': 2, 'value': 1}],
            True, 10,
            [{'count': 3, 'score': 15}, {'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 15
        [
            [
                {'x': 0, 'y': 0, 'value': 9},
                {'x': 1, 'y': 0, 'value': 4},
                {'x': 1, 'y': 1, 'value': 8},
                {'x': 2, 'y': 1, 'value': 7},
                {'x': 1, 'y': 2, 'value': 3}
            ],
            [{'x': 2, 'y': 0, 'value': 2}, {'x': 2, 'y': 2, 'value': 6}],
            True, 8,
            [
                {'count': 3, 'score': 15},
                {'count': 2, 'score': 9},
                {'count': 3, 'score': 15}
            ],
            True, "OK"
        ],

        # no 16
        [
            [{'x': 0, 'y': 0, 'value': 10}, {'x': 1, 'y': 0, 'value': 3}],
            [
                {'x': 0, 'y': 1, 'value': 4},
                {'x': 1, 'y': 1, 'value': 8},
                {'x': 2, 'y': 1, 'value': 3}
            ],
            True, 15,
            [
                {'count': 2, 'score': 14},
                {'count': 2, 'score': 11},
                {'count': 3, 'score': 15}
            ],
            True, "OK"
        ],

        # no 17
        [
            [{'x': 0, 'y': 2, 'value': 11}, {'x': 1, 'y': 2, 'value': 4}],
            [
                {'x': 2, 'y': 0, 'value': 5},
                {'x': 2, 'y': 1, 'value': 10},
                {'x': 2, 'y': 2, 'value': 0}
            ],
            True, 15,
            [{'count': 3, 'score': 15}, {'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 20
        [
            [
                {'x': 0, 'y': 0, 'value': 4},
                {'x': 1, 'y': 0, 'value': 8},
                {'x': 0, 'y': 1, 'value': 7},
                {'x': 1, 'y': 1, 'value': 6},
                {'x': 1, 'y': 2, 'value': 1}
            ],
            [
                {'x': 2, 'y': 0, 'value': 3},
                {'x': 2, 'y': 1, 'value': 2},
                {'x': 2, 'y': 2, 'value': 10}
            ],
            True, 15,
            [
                {'count': 3, 'score': 15},
                {'count': 3, 'score': 15},
                {'count': 2, 'score': 11},
                {'count': 3, 'score': 15}
            ],
            True, "OK"
        ],

        # no 21
        [
            [
                {'x': 0, 'y': 0, 'value': 4},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 9},
                {'x': 1, 'y': 2, 'value': 5}
            ],
            [{'x': 2, 'y': 2, 'value': 10}],
            False, 10,
            [{'count': 2, 'score': 15}],
            True, "OK"
        ],

        # no 22
        [
            [
                {'x': 1, 'y': 0, 'value': 3},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 8},
                {'x': 0, 'y': 2, 'value': 4}
            ],
            [{'x': 2, 'y': 1, 'value': 5}],
            True, 5,
            [{'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 23
        [
            [
                {'x': 0, 'y': 0, 'value': 5},
                {'x': 1, 'y': 0, 'value': 9},
                {'x': 1, 'y': 1, 'value': 5},
                {'x': 1, 'y': 2, 'value': 1},
                {'x': 2, 'y': 2, 'value': 4}
            ],
            [{'x': 2, 'y': 1, 'value': 10}],
            False, 10,
            [{'count': 2, 'score': 14}, {'count': 2, 'score': 15}],
            True, "OK"
        ],

        # no 24
        [
            [
                {'x': 0, 'y': 0, 'value': 6},
                {'x': 1, 'y': 0, 'value': 3},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 8},
                {'x': 1, 'y': 2, 'value': 4},
                {'x': 2, 'y': 2, 'value': 7}
            ],
            [{'x': 2, 'y': 1, 'value': 5}],
            True, 5,
            [{'count': 2, 'score': 12}, {'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 25
        [
            [
                {'x': 0, 'y': 0, 'value': 7},
                {'x': 1, 'y': 0, 'value': 4},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 11},
                {'x': 2, 'y': 1, 'value': 2},
                {'x': 2, 'y': 2, 'value': 9}
            ],
            [{'x': 2, 'y': 0, 'value': 4}],
            True, 4,
            [{'count': 3, 'score': 15}, {'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 27
        [
            [
                {'x': 0, 'y': 0, 'value': 2},
                {'x': 1, 'y': 0, 'value': 3},
                {'x': 1, 'y': 1, 'value': 4}
            ],
            [{'x': 2, 'y': 1, 'value': 7}, {'x': 2, 'y': 2, 'value': 3}],
            False, 10,
            [{'count': 2, 'score': 11}, {'count': 2, 'score': 10}],
            True, "OK"
        ],

        # no 28
        [
            [
                {'x': 0, 'y': 0, 'value': 7},
                {'x': 0, 'y': 1, 'value': 5},
                {'x': 1, 'y': 1, 'value': 3},
                {'x': 1, 'y': 2, 'value': 12},
                {'x': 1, 'y': 3, 'value': 0}
            ],
            [{'x': 2, 'y': 2, 'value': 2}, {'x': 3, 'y': 2, 'value': 1}],
            True, 3,
            [{'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 31
        [
            [
                {'x': 1, 'y': 0, 'value': 7},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 8}
            ],
            [{'x': 2, 'y': 1, 'value': 5}, {'x': 2, 'y': 2, 'value': 10}],
            False, 15,
            [{'count': 3, 'score': 15}, {'count': 2, 'score': 15}],
            True, "OK"
        ],

        # no 32
        [
            [
                {'x': 1, 'y': 0, 'value': 8},
                {'x': 1, 'y': 1, 'value': 3},
                {'x': 0, 'y': 2, 'value': 7},
                {'x': 1, 'y': 2, 'value': 6}
            ],
            [{'x': 2, 'y': 1, 'value': 12}, {'x': 2, 'y': 2, 'value': 2}],
            False, 14,
            [
                {'count': 2, 'score': 15},
                {'count': 3, 'score': 15},
                {'count': 2, 'score': 14}
            ],
            True, "OK"
        ],

        # no 33
        [
            [
                {'x': 0, 'y': 0, 'value': 1},
                {'x': 1, 'y': 0, 'value': 8},
                {'x': 1, 'y': 1, 'value': 5},
                {'x': 2, 'y': 1, 'value': 8}
            ],
            [{'x': 2, 'y': 0, 'value': 6}, {'x': 2, 'y': 2, 'value': 1}],
            True, 7,
            [{'count': 3, 'score': 15}, {'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 34
        [
            [
                {'x': 0, 'y': 0, 'value': 8},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 11},
                {'x': 2, 'y': 1, 'value': 2},
                {'x': 0, 'y': 2, 'value': 5},
                {'x': 2, 'y': 2, 'value': 9}
            ],
            [{'x': 1, 'y': 0, 'value': 3}, {'x': 2, 'y': 0, 'value': 4}],
            True, 7,
            [
                {'count': 2, 'score': 14},
                {'count': 3, 'score': 15},
                {'count': 3, 'score': 15}
            ],
            True, "OK"
        ],

        # no 35
        [
            [
                {'x': 1, 'y': 0, 'value': 3},
                {'x': 2, 'y': 0, 'value': 2},
                {'x': 3, 'y': 0, 'value': 10},
                {'x': 0, 'y': 1, 'value': 2},
                {'x': 1, 'y': 1, 'value': 5},
                {'x': 2, 'y': 1, 'value': 8},
                {'x': 0, 'y': 2, 'value': 3},
                {'x': 0, 'y': 3, 'value': 10}
            ],
            [{'x': 1, 'y': 2, 'value': 7}, {'x': 2, 'y': 2, 'value': 5}],
            True, 12,
            [
                {'count': 3, 'score': 15},
                {'count': 3, 'score': 15},
                {'count': 3, 'score': 15}
            ],
            True, "OK"
        ],

        # no 36
        [
            [
                {'x': 0, 'y': 0, 'value': 8},
                {'x': 0, 'y': 1, 'value': 5},
                {'x': 0, 'y': 2, 'value': 2},
                {'x': 1, 'y': 2, 'value': 10}
            ],
            [
                {'x': 1, 'y': 3, 'value': 4},
                {'x': 2, 'y': 3, 'value': 9},
                {'x': 3, 'y': 3, 'value': 2}
            ],
            True, 15,
            [{'count': 2, 'score': 14}, {'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 37
        [
            [
                {'x': 2, 'y': 0, 'value': 3},
                {'x': 3, 'y': 0, 'value': 9},
                {'x': 2, 'y': 1, 'value': 4},
                {'x': 1, 'y': 2, 'value': 6},
                {'x': 2, 'y': 2, 'value': 8}
            ],
            [
                {'x': 0, 'y': 1, 'value': 7},
                {'x': 0, 'y': 2, 'value': 1},
                {'x': 0, 'y': 3, 'value': 7}
            ],
            True, 15,
            [{'count': 3, 'score': 15}, {'count': 3, 'score': 15}],
            True, "OK"
        ],

        # no 38
        [
            [
                {'x': 0, 'y': 0, 'value': 0},
                {'x': 0, 'y': 1, 'value': 11},
                {'x': 1, 'y': 1, 'value': 4},
                {'x': 2, 'y': 1, 'value': 0},
                {'x': 0, 'y': 2, 'value': 4},
                {'x': 1, 'y': 2, 'value': 10},
                {'x': 2, 'y': 2, 'value': 1}
            ],
            [
                {'x': 1, 'y': 3, 'value': 1},
                {'x': 2, 'y': 3, 'value': 14},
                {'x': 3, 'y': 3, 'value': 0}
            ],
            True, 15,
            [
                {'count': 3, 'score': 15},
                {'count': 3, 'score': 15},
                {'count': 3, 'score': 15}
            ],
            True, "OK"
        ],

        # invalid
        # 1 Token first turn not center
        [
            [],
            [{'x': 14, 'y': 11, 'value': 1}],
            None, 0, [], False, rules.INVALID_MUST_TURN_MUST_BE_START
        ],
        # 2 Token first turn not center
        [
            [],
            [{'x': 0, 'y': 0, 'value': 1}, {'x': 0, 'y': 1, 'value': 1}],
            None, 0, [], False, rules.INVALID_MUST_TURN_MUST_BE_START
        ],
        # 3 Token first turn not center
        [
            [],
            [
                {'x': 11, 'y': 2, 'value': 1},
                {'x': 12, 'y': 2, 'value': 1},
                {'x': 10, 'y': 2, 'value': 13}
            ],
            None, 0, [], False, rules.INVALID_MUST_TURN_MUST_BE_START
        ],

        # 4 Tokens aligned
        [
            [{'x': 7, 'y': 2, 'value': 1}],
            [
                {'x': 8, 'y': 2, 'value': 1},
                {'x': 9, 'y': 2, 'value': 1},
                {'x': 10, 'y': 2, 'value': 13}
            ],
            None, 0, [], False, rules.INVALID_PLACEMENT
        ],

        # empty play
        [
            [{'x': 7, 'y': 7, 'value': 1}],
            [],
            None, 0, [], False, rules.INVALID_SIZE_PLAY
        ],
        # too big play
        [
            [{'x': 7, 'y': 7, 'value': 1}],
            [
                {'x': 9, 'y': 6, 'value': 1},
                {'x': 10, 'y': 6, 'value': 1},
                {'x': 7, 'y': 6, 'value': 1},
                {'x': 8, 'y': 6, 'value': 12}
            ],
            None, 0, [], False, rules.INVALID_SIZE_PLAY
        ],

        # not aligned play
        [
            [{'x': 7, 'y': 7, 'value': 1}],
            [
                {'x': 7, 'y': 8, 'value': 1},
                {'x': 8, 'y': 8, 'value': 1},
                {'x': 8, 'y': 9, 'value': 13}
            ],
            None, 0, [], False, rules.INVALID_NOT_ALIGNED_PLAY
        ],

        # Non adjacent tokens 1
        [
            [{'x': 7, 'y': 7, 'value': 5}, {'x': 8, 'y': 7, 'value': 2}],
            [{'x': 5, 'y': 6, 'value': 1}, {'x': 7, 'y': 6, 'value': 1}],
            None, 0, [], False, rules.INVALID_NON_ADJACENT_TOKENS
        ],
        # Non adjacent tokens 2
        [
            [{'x': 7, 'y': 7, 'value': 5}, {'x': 8, 'y': 7, 'value': 2}],
            [{'x': 1, 'y': 1, 'value': 1}, {'x': 2, 'y': 1, 'value': 1}],
            None, 0, [], False, rules.INVALID_ISOLATED_PLAY
        ],

        # 2 tokens too spread apart
        [
            [],
            [{'x': 7, 'y': 7, 'value': 1}, {'x': 10, 'y': 7, 'value': 1}],
            None, 0, [], False, rules.INVALID_TOO_SPREAD_PLAY
        ],
        # 3 tokens too spread apart
        [
            [],
            [
                {'x': 7, 'y': 2, 'value': 1},
                {'x': 9, 'y': 2, 'value': 1},
                {'x': 11, 'y': 2, 'value': 13}
            ],
            None, 0, [], False, rules.INVALID_TOO_SPREAD_PLAY
        ],

        # 2 tokens sum too high
        [
            [],
            [{'x': 7, 'y': 7, 'value': 8}, {'x': 8, 'y': 7, 'value': 9}],
            None, 0, [], False, rules.INVALID_SCORE_PLAY
        ],
        # 3 tokens sum too low
        [
            [],
            [
                {'x': 7, 'y': 7, 'value': 1},
                {'x': 8, 'y': 7, 'value': 1},
                {'x': 9, 'y': 7, 'value': 1}
            ],
            None, 0, [], False, rules.INVALID_SCORE_PLAY
        ],
        # 3 tokens sum too high
        [
            [],
            [
                {'x': 7, 'y': 7, 'value': 6},
                {'x': 8, 'y': 7, 'value': 6},
                {'x': 9, 'y': 7, 'value': 6}
            ],
            None, 0, [], False, rules.INVALID_SCORE_PLAY
        ],
        [
            [
                {'value': 2, 'y': 0, 'x': 5}, {'value': 1, 'y': 1, 'x': 4},
                {'value': 11, 'y': 1, 'x': 5}, {'value': 3, 'y': 1, 'x': 6},
                {'value': 4, 'y': 1, 'x': 8}, {'value': 2, 'y': 1, 'x': 9},
                {'value': 2, 'y': 2, 'x': 5}, {'value': 1, 'y': 2, 'x': 6},
                {'value': 7, 'y': 2, 'x': 8}, {'value': 5, 'y': 3, 'x': 1},
                {'value': 11, 'y': 3, 'x': 6}, {'value': 0, 'y': 3, 'x': 7},
                {'value': 4, 'y': 3, 'x': 8}, {'value': 1, 'y': 4, 'x': 1},
                {'value': 9, 'y': 4, 'x': 3}, {'value': 6, 'y': 4, 'x': 4},
                {'value': 0, 'y': 4, 'x': 5}, {'value': 12, 'y': 4, 'x': 7},
                {'value': 5, 'y': 4, 'x': 10}, {'value': 10, 'y': 4, 'x': 12},
                {'value': 9, 'y': 5, 'x': 1}, {'value': 3, 'y': 5, 'x': 2},
                {'value': 3, 'y': 5, 'x': 3}, {'value': 8, 'y': 5, 'x': 6},
                {'value': 3, 'y': 5, 'x': 7}, {'value': 4, 'y': 5, 'x': 8},
                {'value': 5, 'y': 5, 'x': 10}, {'value': 8, 'y': 5, 'x': 11},
                {'value': 2, 'y': 5, 'x': 12}, {'value': 0, 'y': 6, 'x': 2},
                {'value': 3, 'y': 6, 'x': 4}, {'value': 5, 'y': 6, 'x': 5},
                {'value': 7, 'y': 6, 'x': 6}, {'value': 10, 'y': 6, 'x': 8},
                {'value': 0, 'y': 6, 'x': 9}, {'value': 5, 'y': 6, 'x': 10},
                {'value': 12, 'y': 7, 'x': 2}, {'value': 2, 'y': 7, 'x': 3},
                {'value': 0, 'y': 7, 'x': 6}, {'value': 14, 'y': 7, 'x': 7},
                {'value': 1, 'y': 7, 'x': 8}, {'value': 7, 'y': 8, 'x': 3},
                {'value': 0, 'y': 8, 'x': 7}, {'value': 2, 'y': 9, 'x': 2},
                {'value': 6, 'y': 9, 'x': 3}, {'value': 7, 'y': 9, 'x': 4},
                {'value': 7, 'y': 9, 'x': 6}, {'value': 1, 'y': 9, 'x': 7},
                {'value': 5, 'y': 10, 'x': 4}, {'value': 4, 'y': 10, 'x': 5},
                {'value': 6, 'y': 10, 'x': 6}, {'value': 9, 'y': 11, 'x': 2},
                {'value': 3, 'y': 11, 'x': 3}, {'value': 3, 'y': 11, 'x': 4},
                {'value': 2, 'y': 11, 'x': 6}, {'value': 8, 'y': 11, 'x': 7},
                {'value': 1, 'y': 12, 'x': 0}, {'value': 5, 'y': 12, 'x': 2},
                {'value': 6, 'y': 12, 'x': 3}, {'value': 3, 'y': 12, 'x': 7},
                {'value': 1, 'y': 12, 'x': 8}, {'value': 11, 'y': 12, 'x': 10},
                {'value': 0, 'y': 12, 'x': 11}, {'value': 4, 'y': 12, 'x': 12},
                {'value': 13, 'y': 13, 'x': 0}, {'value': 1, 'y': 13, 'x': 1},
                {'value': 1, 'y': 13, 'x': 2}, {'value': 10, 'y': 13, 'x': 8},
                {'value': 5, 'y': 13, 'x': 9}, {'value': 0, 'y': 13, 'x': 10},
                {'value': 13, 'y': 14, 'x': 1}, {'value': 4, 'y': 14, 'x': 8},
                {'value': 7, 'y': 14, 'x': 9}, {'value': 4, 'y': 14, 'x': 10}
            ],
            [
                {'value': 9, 'y': 1, 'x': 10}, {'value': 0, 'y': 0, 'x': 10}
            ],
            False, 9,
            [{'count': 3, 'score': 15}, {'count': 2, 'score': 9}],
            True, "OK"
        ]
    ],
    # valid
    ids=['1 Token first turn center',
         '2 Tokens first turn center',
         '3 Tokens first turn center',

         'Paper rule no 1',
         'Paper rule no 2',
         'Paper rule no 3',
         'Paper rule no 4',
         'Paper rule no 5',
         'Paper rule no 6',
         'Paper rule no 7',
         'Paper rule no 8',
         'Paper rule no 9',
         'Paper rule no 11',
         'Paper rule no 13',
         'Paper rule no 14',
         'Paper rule no 15',
         'Paper rule no 16',
         'Paper rule no 17',
         'Paper rule no 20',
         'Paper rule no 21',
         'Paper rule no 22',
         'Paper rule no 23',
         'Paper rule no 24',
         'Paper rule no 25',
         'Paper rule no 27',
         'Paper rule no 28',
         'Paper rule no 31',
         'Paper rule no 32',
         'Paper rule no 33',
         'Paper rule no 34',
         'Paper rule no 35',
         'Paper rule no 36',
         'Paper rule no 37',
         'Paper rule no 38',

         # Invalid
         '1 Token first turn not center',
         '2 Token first turn not center',
         '3 Token first turn not center',

         '4 Tokens aligned',

         'empty play',
         'too big play',

         'not aligned play',

         'Non adjacent tokens 1',
         'Non adjacent tokens 2',

         '2 tokens too spread apart',
         '3 tokens too spread apart',

         '2 tokens sum too high',
         '3 tokens sum too low',
         '3 tokens sum too high',
         'bug']
)
def test_analyse_play(
    board_content,
    play,
    complete,
    score_play,
    scores,
    valid,
    valid_reason
):
    boardInstance = board.Board()
    for token in board_content:
        boardInstance.set_placement(token['x'], token['y'], token['value'])

    analyse = rules.analyse_play(boardInstance, play)
    if not analyse['valid']:
        assert analyse['reason'] == valid_reason
    else:
        assert analyse['values'] == scores
        assert analyse['complete'] == complete
        assert analyse['score_play'] == score_play
    assert analyse['valid'] == valid


@pytest.mark.parametrize(
    "board_content,hand,expected_result",
    [
        [
            [], [1, 2, 3], True
        ],
        [
            [{'x': 8, 'y': 4, 'value': 10}],
            [10, 6, 8],
            False
        ],
        [
            [{'x': 8, 'y': 4, 'value': 10}],
            [1, 6, 8],
            True
        ]
    ],
    ids=["Empty Board",
         "No possible play",
         "Possible play"]
)
def test_can_play(board_content, hand, expected_result):
    boardInstance = board.Board()
    for token in board_content:
        boardInstance.set_placement(token['x'], token['y'], token['value'])

    assert rules.can_play(boardInstance, hand) is expected_result
