import pytest

from app.game import board
from app.game import score
from app.game import rules


@pytest.mark.parametrize(
    "board_content,play,expected_score",
    [
        # valid
        # 1 Token first turn center
        [[], [{'x': 7, 'y': 7, 'value': 1}], 2],
        # 2 Token first turn center
        [[], [{'x': 7, 'y': 7, 'value': 1}, {'x': 6, 'y': 7, 'value': 1}], 3],
        # 3 Token first turn center
        [
            [],
            [
                {'x': 7, 'y': 6, 'value': 3},
                {'x': 7, 'y': 7, 'value': 4},
                {'x': 7, 'y': 8, 'value': 8}
            ],
            110
        ],

        # valid from paper rules
        # no 1
        [
            [{'x': 0, 'y': 0, 'value': 10}],
            [{'x': 1, 'y': 0, 'value': 3}],
            13
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
            25
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
            30
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
            34
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
            60
        ],

        # no 6
        [
            [{'x': 1, 'y': 0, 'value': 9}, {'x': 2, 'y': 0, 'value': 5}],
            [{'x': 0, 'y': 1, 'value': 7}, {'x': 1, 'y': 1, 'value': 6}],
            28
        ],

        # no 7
        [
            [{'x': 0, 'y': 1, 'value': 10}, {'x': 1, 'y': 1, 'value': 3}],
            [{'x': 0, 'y': 0, 'value': 1}, {'x': 0, 'y': 2, 'value': 4}],
            30
        ],

        # no 8
        [
            [{'x': 0, 'y': 0, 'value': 15}, {'x': 0, 'y': 1, 'value': 0}],
            [{'x': 1, 'y': 0, 'value': 0}, {'x': 2, 'y': 0, 'value': 0}],
            30
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
            32
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
            37
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
            59
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
            60
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
            69
        ],

        # no 16
        [
            [{'x': 0, 'y': 0, 'value': 10}, {'x': 1, 'y': 0, 'value': 3}],
            [
                {'x': 0, 'y': 1, 'value': 4},
                {'x': 1, 'y': 1, 'value': 8},
                {'x': 2, 'y': 1, 'value': 3}
            ],
            105
        ],

        # no 17
        [
            [{'x': 0, 'y': 2, 'value': 11}, {'x': 1, 'y': 2, 'value': 4}],
            [
                {'x': 2, 'y': 0, 'value': 5},
                {'x': 2, 'y': 1, 'value': 10},
                {'x': 2, 'y': 2, 'value': 0}
            ],
            110
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
            151
        ],

        # no 21
        [
            [
                {'x': 2, 'y': 2, 'value': 4},
                {'x': 2, 'y': 3, 'value': 2},
                {'x': 3, 'y': 3, 'value': 9},
                {'x': 3, 'y': 4, 'value': 5}
            ],
            [{'x': 4, 'y': 4, 'value': 10}],
            25
        ],

        # no 22
        [
            [
                {'x': 3, 'y': 3, 'value': 3},
                {'x': 2, 'y': 4, 'value': 2},
                {'x': 3, 'y': 4, 'value': 8},
                {'x': 2, 'y': 5, 'value': 4}
            ],
            [{'x': 4, 'y': 4, 'value': 5}],
            60
        ],

        # no 23
        [
            [
                {'x': 2, 'y': 3, 'value': 5},
                {'x': 3, 'y': 3, 'value': 9},
                {'x': 3, 'y': 4, 'value': 5},
                {'x': 3, 'y': 5, 'value': 1},
                {'x': 4, 'y': 5, 'value': 4}
            ],
            [{'x': 4, 'y': 4, 'value': 10}],
            39
        ],

        # no 24
        [
            [
                {'x': 2, 'y': 3, 'value': 6},
                {'x': 3, 'y': 3, 'value': 3},
                {'x': 2, 'y': 4, 'value': 2},
                {'x': 3, 'y': 4, 'value': 8},
                {'x': 3, 'y': 5, 'value': 4},
                {'x': 4, 'y': 5, 'value': 7}
            ],
            [{'x': 4, 'y': 4, 'value': 5}],
            72
        ],

        # no 25
        [
            [
                {'x': 2, 'y': 4, 'value': 7},
                {'x': 3, 'y': 4, 'value': 4},
                {'x': 2, 'y': 5, 'value': 2},
                {'x': 3, 'y': 5, 'value': 11},
                {'x': 4, 'y': 5, 'value': 2},
                {'x': 4, 'y': 6, 'value': 9}
            ],
            [{'x': 4, 'y': 4, 'value': 4}],
            90
        ],

        # no 27
        [
            [
                {'x': 2, 'y': 3, 'value': 2},
                {'x': 3, 'y': 3, 'value': 3},
                {'x': 3, 'y': 4, 'value': 4}
            ],
            [{'x': 4, 'y': 4, 'value': 7}, {'x': 4, 'y': 5, 'value': 3}],
            28
        ],

        # no 28
        [
            [
                {'x': 1, 'y': 2, 'value': 7},
                {'x': 1, 'y': 3, 'value': 5},
                {'x': 2, 'y': 3, 'value': 3},
                {'x': 2, 'y': 4, 'value': 12},
                {'x': 2, 'y': 5, 'value': 0}
            ],
            [{'x': 3, 'y': 4, 'value': 2}, {'x': 4, 'y': 4, 'value': 1}],
            60
        ],

        # no 31
        [
            [
                {'x': 3, 'y': 3, 'value': 7},
                {'x': 2, 'y': 4, 'value': 2},
                {'x': 3, 'y': 4, 'value': 8}
            ],
            [{'x': 4, 'y': 4, 'value': 5}, {'x': 4, 'y': 5, 'value': 10}],
            75
        ],

        # no 32
        [
            [
                {'x': 3, 'y': 2, 'value': 8},
                {'x': 3, 'y': 3, 'value': 3},
                {'x': 2, 'y': 4, 'value': 7},
                {'x': 3, 'y': 4, 'value': 6}
            ],
            [{'x': 4, 'y': 3, 'value': 12}, {'x': 4, 'y': 4, 'value': 2}],
            89
        ],

        # no 33
        [
            [
                {'x': 2, 'y': 4, 'value': 1},
                {'x': 3, 'y': 4, 'value': 8},
                {'x': 3, 'y': 5, 'value': 5},
                {'x': 4, 'y': 5, 'value': 8}
            ],
            [{'x': 4, 'y': 4, 'value': 6}, {'x': 4, 'y': 6, 'value': 1}],
            90
        ],

        # no 34
        [
            [
                {'x': 2, 'y': 4, 'value': 8},
                {'x': 2, 'y': 5, 'value': 2},
                {'x': 3, 'y': 5, 'value': 11},
                {'x': 4, 'y': 5, 'value': 2},
                {'x': 2, 'y': 6, 'value': 5},
                {'x': 4, 'y': 6, 'value': 9}
            ],
            [{'x': 3, 'y': 4, 'value': 3}, {'x': 4, 'y': 4, 'value': 4}],
            104
        ],

        # no 35
        [
            [
                {'x': 4, 'y': 2, 'value': 3},
                {'x': 5, 'y': 2, 'value': 2},
                {'x': 6, 'y': 2, 'value': 10},
                {'x': 3, 'y': 3, 'value': 2},
                {'x': 4, 'y': 3, 'value': 5},
                {'x': 5, 'y': 3, 'value': 8},
                {'x': 3, 'y': 4, 'value': 3},
                {'x': 3, 'y': 5, 'value': 10}
            ],
            [{'x': 4, 'y': 4, 'value': 7}, {'x': 5, 'y': 4, 'value': 5}],
            120
        ],

        # no 36
        [
            [
                {'x': 3, 'y': 1, 'value': 8},
                {'x': 3, 'y': 2, 'value': 5},
                {'x': 3, 'y': 3, 'value': 2},
                {'x': 4, 'y': 3, 'value': 10}
            ],
            [
                {'x': 4, 'y': 4, 'value': 4},
                {'x': 5, 'y': 4, 'value': 9},
                {'x': 6, 'y': 4, 'value': 2}
            ],
            124
        ],

        # no 37
        [
            [
                {'x': 6, 'y': 2, 'value': 3},
                {'x': 7, 'y': 2, 'value': 9},
                {'x': 6, 'y': 3, 'value': 4},
                {'x': 5, 'y': 4, 'value': 6},
                {'x': 6, 'y': 4, 'value': 8}
            ],
            [
                {'x': 4, 'y': 3, 'value': 7},
                {'x': 4, 'y': 4, 'value': 1},
                {'x': 4, 'y': 5, 'value': 7}
            ],
            140
        ],

        # no 38
        [
            [
                {'x': 1, 'y': 1, 'value': 0},
                {'x': 1, 'y': 2, 'value': 11},
                {'x': 2, 'y': 2, 'value': 4},
                {'x': 3, 'y': 2, 'value': 0},
                {'x': 1, 'y': 3, 'value': 4},
                {'x': 2, 'y': 3, 'value': 10},
                {'x': 3, 'y': 3, 'value': 1}
            ],
            [
                {'x': 2, 'y': 4, 'value': 1},
                {'x': 3, 'y': 4, 'value': 14},
                {'x': 4, 'y': 4, 'value': 0}
            ],
            170
        ],

        # invalid
        # 1 Token first turn not center
        [[], [{'x': 14, 'y': 11, 'value': 1}], 0],
        # 2 Token first turn not center
        [[], [{'x': 0, 'y': 0, 'value': 1}, {'x': 0, 'y': 1, 'value': 1}], 0],
        # 3 Token first turn not center
        [
            [],
            [
                {'x': 11, 'y': 2, 'value': 1},
                {'x': 12, 'y': 2, 'value': 1},
                {'x': 10, 'y': 2, 'value': 13}
            ],
            0
        ],

        # empty play
        [[{'x': 7, 'y': 7, 'value': 1}], [], 0],
        # too big play
        [[{'x': 7, 'y': 7, 'value': 1}], [
            {'x': 9, 'y': 6, 'value': 1},
            {'x': 10, 'y': 6, 'value': 1},
            {'x': 7, 'y': 6, 'value': 1},
            {'x': 8, 'y': 6, 'value': 12}
        ], 0],

        # not aligned play
        [
            [{'x': 7, 'y': 7, 'value': 1}],
            [
                {'x': 7, 'y': 8, 'value': 1},
                {'x': 8, 'y': 8, 'value': 1},
                {'x': 8, 'y': 9, 'value': 13}
            ], 0
        ],

        # Non adjacent tokens 1
        [
            [{'x': 7, 'y': 7, 'value': 5}, {'x': 8, 'y': 7, 'value': 2}],
            [{'x': 5, 'y': 6, 'value': 1}, {'x': 7, 'y': 6, 'value': 1}],
            0
        ],
        # Non adjacent tokens 2
        [
            [{'x': 7, 'y': 7, 'value': 5}, {'x': 8, 'y': 7, 'value': 2}],
            [{'x': 1, 'y': 1, 'value': 1}, {'x': 2, 'y': 1, 'value': 1}],
            0
        ],

        # 2 tokens too spread apart
        [
            [],
            [{'x': 7, 'y': 7, 'value': 1}, {'x': 10, 'y': 7, 'value': 1}],
            0
        ],
        # 3 tokens too spread apart
        [
            [],
            [
                {'x': 7, 'y': 2, 'value': 1},
                {'x': 9, 'y': 2, 'value': 1},
                {'x': 11, 'y': 2, 'value': 13}
            ],
            0
        ],

        # 2 tokens sum too high
        [
            [],
            [{'x': 7, 'y': 7, 'value': 8}, {'x': 8, 'y': 7, 'value': 9}],
            0
        ],
        # 3 tokens sum too low
        [
            [],
            [
                {'x': 7, 'y': 7, 'value': 1},
                {'x': 8, 'y': 7, 'value': 1},
                {'x': 9, 'y': 7, 'value': 1}
            ],
            0
        ],
        # 3 tokens sum too high
        [
            [],
            [
                {'x': 7, 'y': 7, 'value': 6},
                {'x': 8, 'y': 7, 'value': 6},
                {'x': 9, 'y': 7, 'value': 6}
            ],
            0
        ]
    ],
    # valids
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

         'empty play',
         'too big play',

         'not aligned play',

         'Non adjacent tokens 1',
         'Non adjacent tokens 2',

         '2 tokens too spread apart',
         '3 tokens too spread apart',

         '2 tokens sum too high',
         '3 tokens sum too low',
         '3 tokens sum too high']
)
def test_calculate_score(board_content, play, expected_score):
    boardInstance = board.Board()
    for token in board_content:
        boardInstance.set_placement(token['x'], token['y'], token['value'])

    play_analyse = rules.analyse_play(boardInstance, play)
    calculated_score = score.calculate_score(boardInstance, play, play_analyse)
    assert calculated_score == expected_score
