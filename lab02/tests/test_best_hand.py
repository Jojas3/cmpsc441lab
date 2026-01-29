"""Tests for poker_hand.py best_hand function."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from itertools import combinations

from poker_hand import best_hand, hand_rank


def test_straight_flush():
    """Test selecting the best straight flush from 7 cards."""
    hand = "6C 7C 8C 9C TC 5C JS".split()
    result = sorted(best_hand(hand))
    assert result == ['6C', '7C', '8C', '9C', 'TC']


def test_full_house_over_two_pair():
    """Test selecting full house when multiple pairs are available."""
    hand = "TD TC TH 7C 7D 8C 8S".split()
    result = sorted(best_hand(hand))
    assert result == ['8C', '8S', 'TC', 'TD', 'TH']


def test_four_of_a_kind():
    """Test selecting four of a kind with best kicker."""
    hand = "JD TC TH 7C 7D 7S 7H".split()
    result = sorted(best_hand(hand))
    assert result == ['7C', '7D', '7H', '7S', 'JD']


def test_returns_five_cards():
    """Test that best_hand always returns exactly 5 cards."""
    hand = "2C 3D 5H 7S 9C JD KH".split()
    result = best_hand(hand)
    assert len(result) == 5


def test_flush_beats_straight():
    """Test that a flush is chosen over a straight."""
    hand = "2H 4H 6H 8H TH 9C JS".split()
    result = sorted(best_hand(hand))
    assert result == ['2H', '4H', '6H', '8H', 'TH']


def test_straight():
    """Test selecting a straight."""
    hand = "5C 6D 7H 8S 9C 2D KH".split()
    result = sorted(best_hand(hand))
    assert result == ['5C', '6D', '7H', '8S', '9C']


def test_three_of_a_kind():
    """Test selecting three of a kind with best kickers."""
    hand = "AC AD AH 2C 5D 8S KH".split()
    result = sorted(best_hand(hand))
    assert 'AC' in result
    assert 'AD' in result
    assert 'AH' in result
    assert 'KH' in result
    assert '8S' in result


def test_two_pair():
    """Test selecting two pair with best kicker."""
    hand = "AC AD KC KD 2C 5D 8S".split()
    result = sorted(best_hand(hand))
    assert 'AC' in result
    assert 'AD' in result
    assert 'KC' in result
    assert 'KD' in result
    assert '8S' in result


def test_one_pair():
    """Test selecting one pair with best kickers."""
    hand = "AC AD 3C 5D 7S 9H JC".split()
    result = sorted(best_hand(hand))
    assert 'AC' in result
    assert 'AD' in result
    assert 'JC' in result
    assert '9H' in result
    assert '7S' in result


def test_high_card():
    """Test selecting highest cards when no hand is made."""
    hand = "2C 4D 6H 8S TC QD AH".split()
    result = sorted(best_hand(hand))
    assert result == ['6H', '8S', 'AH', 'QD', 'TC']


def test_ace_low_straight():
    """Test selecting an ace-low straight (wheel)."""
    hand = "AC 2D 3H 4S 5C 9D KH".split()
    result = sorted(best_hand(hand))
    assert result == ['2D', '3H', '4S', '5C', 'AC']


def test_best_hand_is_valid_subset():
    """Test that the returned hand is a valid subset of input."""
    hand = "6C 7C 8C 9C TC 5C JS".split()
    result = best_hand(hand)
    for card in result:
        assert card in hand


def test_best_hand_rank_is_maximum():
    """Test that the returned hand has the maximum possible rank."""
    hand = "TD TC TH 7C 7D 8C 8S".split()
    result = best_hand(hand)
    result_rank = hand_rank(result)

    for combo in combinations(hand, 5):
        combo_rank = hand_rank(list(combo))
        assert result_rank >= combo_rank
