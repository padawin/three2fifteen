from api.game import board

MAX_SIZE_HAND = 3


def analyse_placement(board_instance, x, y, token_value):
    """
    Check if 4 directions the number of adjacent token + the sum of their points
    """
    count_score = get_count_score(board_instance, x, y, token_value)
    valid = count_score and (
            count_score['count_vertical'] < MAX_SIZE_HAND and
            count_score['score_vertical'] <= 15
            or
            count_score['count_vertical'] == MAX_SIZE_HAND and
            count_score['score_vertical'] == 15
    ) and (
            count_score['count_horizontal'] < MAX_SIZE_HAND and
            count_score['score_horizontal'] <= 15
            or
            count_score['count_horizontal'] == MAX_SIZE_HAND and
            count_score['score_horizontal'] == 15
    )
    res = {'valid': valid}

    if valid:
        res = {**res, **count_score}

    return res


def get_count_score(board_instance, x, y, token_value):
    if not board_instance.coordinates_in_bound(x, y):
        return False

    token_at = board_instance.get_token_at(x, y)
    if token_at is not None:
        return False

    count_tokens_horizontal = 1
    count_tokens_vertical = 1
    score_horizontal = token_value
    score_vertical = token_value

    def _compute_sums(x, y, coef_x, coef_y, count_tokens, score):
        for i in range(1, 4):
            token_at = board_instance.get_token_at(
                x + (coef_x * i),
                y - (coef_y * i)
            )
            if token_at is None:
                break
            count_tokens += 1
            score += token_at

        return (count_tokens, score)

    # top
    count_tokens_vertical, score_vertical = _compute_sums(x, y, 0, -1, count_tokens_vertical, score_vertical)
    # bottom
    count_tokens_vertical, score_vertical = _compute_sums(x, y, 0, 1, count_tokens_vertical, score_vertical)
    # left
    count_tokens_horizontal, score_horizontal = _compute_sums(x, y, -1, 0, count_tokens_horizontal, score_horizontal)
    # right
    count_tokens_horizontal, score_horizontal = _compute_sums(x, y, 1, 0, count_tokens_horizontal, score_horizontal)

    return {
        'count_horizontal': count_tokens_horizontal,
        'count_vertical': count_tokens_vertical,
        'score_horizontal': score_horizontal,
        'score_vertical': score_vertical
    }

VALID = "OK"
INVALID_SIZE_PLAY = "Invalid play size"
INVALID_SCORE_PLAY = "Invalid play score"
INVALID_NOT_ALIGNED_PLAY = "Play not aligned"
INVALID_TOO_SPREAD_PLAY = "Play too spread"
INVALID_NON_ADJACENT_TOKENS = "Not adjacent tokens"
INVALID_MUST_TURN_MUST_BE_START = "First turn must be played in start"
INVALID_PLACEMENT = "A placement is invalid"
INVALID_ISOLATED_PLAY = "A play must touch the rest of the tokens"


def analyse_play(board_instance, play):
    size_play = len(play)
    score_play = sum(token['value'] for token in play)
    analyse = {
        'valid': True,
        'size_play': size_play,
        'score_play': score_play
    }

    # a play has between 1 and MAX_SIZE_HAND tokens
    if size_play == 0 or size_play > MAX_SIZE_HAND:
        return {'valid': False, 'reason': INVALID_SIZE_PLAY}

    # makes sure the score is valid
    if size_play == MAX_SIZE_HAND and score_play != 15 or score_play > 15:
        return {'valid': False, 'reason': INVALID_SCORE_PLAY}

    if size_play > 1:
        tokens_alignment_analyse, data = _analyse_tokens_alignment(
            board_instance,
            play
        )
        if tokens_alignment_analyse != VALID:
            return {'valid': False, 'reason': tokens_alignment_analyse}

        analyse = {**analyse, **data}

    # for first turn, make sure a token is in the center
    play_position_analyse = _analyse_play_position(board_instance, play)
    if play_position_analyse != VALID:
        return {'valid': False, 'reason': play_position_analyse}

    # check the token can be placed on the board
    score_placements = _try_place_tokens(board_instance, play)
    if not score_placements:
        return {'valid': False, 'reason': INVALID_PLACEMENT}

    # -1 represents the last token placed in the temporary board, which is the
    # global state of the play
    analyse['complete'] = (
        size_play == MAX_SIZE_HAND or
        size_play == 2 and score_placements[-1]['count_{}'.format(analyse['aligned'])] == MAX_SIZE_HAND or
        # 1 token play
        size_play == 1 and (
            score_placements[0]['count_horizontal'] == MAX_SIZE_HAND or
            score_placements[0]['count_vertical'] == MAX_SIZE_HAND
        ))

    analyse['values'] = _compute_score_count(
        score_placements,
        analyse['aligned'] if 'aligned' in analyse else None
    )

    return analyse


def _try_place_tokens(board_instance, play):
    """
    Test if all the tokens can be placed on the board and if placing them
    together does not invalidates the board
    """
    tmp_board = board.Board(board_instance.get_grid())
    score_placements = []
    for token in play:
        placement_analyse = analyse_placement(
            tmp_board,
            token['x'],
            token['y'],
            token['value']
        )
        if not placement_analyse['valid']:
            return False

        score_placements.append(placement_analyse)
        tmp_board.set_placement(token['x'], token['y'], token['value'])

    return score_placements


def _analyse_tokens_alignment(board_instance, play):
    """
    Tests if the tokens are aligned, not too spread apart and joined with each
    other
    """
    size_play = len(play)
    xs = list({token['x'] for token in play})
    ys = list({token['y'] for token in play})

    # make sure the tokens are aligned
    aligned_y = len(xs) == 1
    aligned_x = len(ys) == 1
    aligned = (aligned_y and len(ys) == size_play or
               aligned_x and len(xs) == size_play)
    # all the tokens of the play must be aligned and different
    if not aligned:
        return INVALID_NOT_ALIGNED_PLAY, None

    # all the tokens of the play must be within MAX_SIZE_HAND spaces
    # (boundaries included)
    delta_x = max(xs) - min(xs)
    delta_y = max(ys) - min(ys)
    if delta_x > 2 or delta_y > 2:
        return INVALID_TOO_SPREAD_PLAY, None

    # make sure they complete a single line or column
    # eg the following must fail (x are existing tokens and y are new ones):
    # [x][y][ ][y][x]
    if (
        size_play == 2 and
        (
            delta_x == 2 and board_instance.get_token_at(min(xs) + 1, ys[0]) is None or
            delta_y == 2 and board_instance.get_token_at(xs[0], min(ys) + 1) is None
        )
    ):
        return INVALID_NON_ADJACENT_TOKENS, None

    return VALID, {
        'aligned': 'vertical' if aligned_y else 'horizontal',
        'perpendicular': 'vertical' if aligned_x else 'horizontal'
    }


def _analyse_play_position(board_instance, play):
    if board_instance.is_empty():
        if not _has_token_in_start(board_instance, play):
            return INVALID_MUST_TURN_MUST_BE_START
    elif _is_island(board_instance, play):
        return INVALID_ISOLATED_PLAY

    return VALID


def _has_token_in_start(board_instance, play):
    """
    Test if a token of the play is in the start of the board
    """
    return 0 < len([
        1 for token in play
        if board_instance.is_start(token['x'], token['y'])])


def _is_island(board_instance, play):
    """
    Test if the play is placed in an isolated place of the board
    """
    # make sure we don't play in an isolated place
    is_island = True
    for token in play:
        count_score = get_count_score(
            board_instance,
            token['x'],
            token['y'],
            token['value']
        )
        is_island = (is_island and
                     count_score['count_vertical'] == 1 and
                     count_score['count_horizontal'] == 1)
    return is_island


def _compute_score_count(score_placements, aligned):
    scores = []
    if aligned is None:
        for way in ['vertical', 'horizontal']:
            if score_placements[0]['count_{}'.format(way)] > 1:
                scores.append(
                    {
                        'count': score_placements[0]['count_{}'.format(way)],
                        'score': score_placements[0]['score_{}'.format(way)]
                    }
                )
    else:
        perpendicular = 'vertical' if aligned == 'horizontal' else 'horizontal'
        count = 'count_{}'.format(aligned)
        score = 'score_{}'.format(aligned)
        count_perp = 'count_{}'.format(perpendicular)
        score_perp = 'score_{}'.format(perpendicular)
        scores = [
            {'count': neighbour[count_perp], 'score': neighbour[score_perp]}
            for neighbour in score_placements
            if neighbour[count_perp] > 1
        ]
        scores.append(
            {
                'count': score_placements[-1][count],
                'score': score_placements[-1][score]
            }
        )

    return scores

def can_play(board_instance, tokens):
    """
    Return True if at least one of the tokens of `play` can be placed in the
    `board_instance`.
    """
    if board_instance.is_empty():
        return True

    for token in tokens:
        for x, y in board_instance.rim:
            play = [{'x': x, 'y': y, 'value': token}]
            if analyse_play(board_instance, play)['valid']:
                return True

    return False
