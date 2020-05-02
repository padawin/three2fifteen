import random
from collections import Counter
from app.game import rules


class Bag(object):
    def __init__(self, exclude=[]):
        exclude = Counter(exclude)
        full = Counter([
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3, 3, 3, 3,
            4, 4, 4, 4, 4, 4, 4,
            5, 5, 5, 5, 5, 5, 5, 5,
            6, 6, 6, 6, 6, 6,
            7, 7, 7, 7, 7, 7,
            8, 8, 8, 8,
            9, 9, 9, 9,
            10, 10, 10,
            11, 11, 11,
            12, 12,
            13, 13,
            14,
            15
        ])

        diff = full - exclude
        self.tokens = list(diff.elements())

    def remove_same_tokens_as(self, to_exclude):
        self.tokens = [token for token in self.tokens if token != to_exclude]

    def pick_token(self):
        if len(self.tokens) == 0:
            raise Error("The bag is empty")
        token = random.choice(self.tokens)
        self.tokens.remove(token)
        return token

    def fill_hand(self, hand=[]):
        nb_to_pick = min(
            len(self.tokens),
            rules.MAX_SIZE_HAND - len(hand)
        )
        return hand + [self.pick_token() for i in range(nb_to_pick)]

    def is_empty(self):
        return len(self.tokens) == 0


class Error(BaseException):
    pass
