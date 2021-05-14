from api.game import rules


def calculate_score(board_instance, play, play_analyse):
    if not play_analyse['valid']:
        return 0

    total = 0
    # this is for a single token play isolated (first turn)
    if play_analyse['values'] == []:
        total = play_analyse['score_play']

    for score in play_analyse['values']:
        total += score['score'] * 2 if score['count'] == 3 else score['score']

    multiplier = None
    for token in play:
        multiplier = board_instance.get_multiplier(token['x'], token['y'])
        if multiplier == 1:
            continue
        count_score = rules.get_count_score(
            board_instance,
            token['x'],
            token['y'],
            token['value']
        )
        multiplier -= 1
        # one of the two has 3 tokens, we want to take
        # 30 * (multiplier - 1) extra points
        # multiplier - 1 because a first iteration of the score has already
        # been taken in account when adding play_analyse['values']
        if (
            play_analyse['complete'] or
            count_score['count_horizontal'] == 3 or
            count_score['count_vertical'] == 3
        ):
            total += 30 * multiplier
        else:
            # otherwise, just multiply the current token
            total += token['value'] * multiplier

    if len(play) == 3:
        total += 50

    return total
