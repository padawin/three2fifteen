from unittest.mock import patch

from app.service import turn
from app.model.turn import TurnModel


@patch.object(TurnModel, 'fetchAllRows')
def test_get_game_content(mock_fetchAllRows):
    mock_fetchAllRows.return_value = [
        {
            'x': [7, 8],
            'y': [7, 7],
            'value': [10, 4],
            'id_user': 1,
            'id_player': 1,
            'score': 14
        },
        {
            'x': [8, 8],
            'y': [8, 9],
            'value': [6, 5],
            'id_user': 2,
            'id_player': 2,
            'score': 11
        },
        {
            'x': [7, 6],
            'y': [8, 8],
            'value': [7, 2],
            'id_user': 1,
            'id_player': 1,
            'score': 9
        }
    ]
    tokens = TurnModel.get_game_content(11)
    assert tokens == [
        {'x': 7, 'y': 7, 'value': 10},
        {'x': 8, 'y': 7, 'value': 4},
        {'x': 8, 'y': 8, 'value': 6},
        {'x': 8, 'y': 9, 'value': 5},
        {'x': 7, 'y': 8, 'value': 7},
        {'x': 6, 'y': 8, 'value': 2}
    ]
