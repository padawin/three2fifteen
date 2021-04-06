import pytest

from api.game import bag


def test_init_is_not_empty():
    b = bag.Bag()
    assert not b.is_empty()


def test_fill_bag_not_empty():
    b = bag.Bag()
    hand = b.fill_hand()
    assert len(hand) == 3
    hand = b.fill_hand([1])
    assert len(hand) == 3
    hand = b.fill_hand([1, 2])
    assert len(hand) == 3
    hand = b.fill_hand([1, 2, 3])
    assert len(hand) == 3
    hand = b.fill_hand([1, 2, 3, 4])
    assert len(hand) == 4


def test_remove_same_tokens_as():
    b = bag.Bag()
    b.remove_same_tokens_as(1)
    assert b.tokens == [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
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
    ]


def test_fill_bag_empty():
    exclude = [
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
        12,12,
        13,13,
        14
    ]
    # contains 15
    b = bag.Bag(exclude)
    hand = b.fill_hand([1])
    assert hand == [1, 15]
    assert b.is_empty()


def test_init_with_data():
    exclude = [
        0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 2, 2,
        3, 3, 3, 3, 3, 3, 3,
        4, 4, 4, 4, 4, 4,
        5, 5, 5, 5, 5, 5, 5,
        6, 6, 6, 6, 6,
        7, 7, 7, 7, 7,
        8, 8, 8,
        9, 9, 9,
        10, 10,
        11, 11,
        12,
        13,
    ]
    b = bag.Bag(exclude)
    assert not b.is_empty()
    in_bag = []
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    in_bag.append(b.pick_token())
    assert not b.is_empty()
    in_bag.append(b.pick_token())
    assert b.is_empty()
    in_bag.sort()
    assert in_bag == [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    with pytest.raises(bag.Error):
        b.pick_token()
