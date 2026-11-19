from random import Random

import pytest

from mini_games.blackjack import (
    BlackjackRound,
    Card,
    RoundOutcome,
    hand_value,
    is_blackjack,
    is_soft_hand,
    resolve_outcome,
    standard_deck,
)


def cards(*ranks: str) -> list[Card]:
    return [Card(rank, "Spades") for rank in ranks]


@pytest.mark.parametrize(
    ("ranks", "expected"),
    [
        (("10", "7"), 17),
        (("Ace", "9"), 20),
        (("Ace", "9", "Ace"), 21),
        (("Ace", "Ace", "9", "King"), 21),
    ],
)
def test_hand_value_handles_aces(ranks, expected):
    assert hand_value(cards(*ranks)) == expected


def test_blackjack_requires_exactly_two_cards():
    assert is_blackjack(cards("Ace", "King"))
    assert not is_blackjack(cards("Ace", "5", "5"))


def test_soft_hand_distinguishes_aces_counted_as_eleven_or_one():
    assert is_soft_hand(cards("Ace", "6"))
    assert is_soft_hand(cards("Ace", "Ace", "5"))
    assert not is_soft_hand(cards("Ace", "10", "6"))


def test_dealer_soft_17_rule_is_explicit():
    stand = BlackjackRound(deck=cards("2"), dealer_hand=cards("Ace", "6"))
    stand.dealer_play()
    assert stand.dealer_value == 17 and len(stand.dealer_hand) == 2

    hit = BlackjackRound(deck=cards("2"), dealer_hand=cards("Ace", "6"))
    hit.dealer_play(hit_soft_17=True)
    assert hit.dealer_value == 19 and len(hit.dealer_hand) == 3


def test_outcomes_cover_naturals_busts_and_pushes():
    assert resolve_outcome(cards("Ace", "King"), cards("10", "9")) is RoundOutcome.PLAYER_BLACKJACK
    assert resolve_outcome(cards("10", "8", "5"), cards("10", "9")) is RoundOutcome.PLAYER_BUST
    assert resolve_outcome(cards("10", "9"), cards("10", "8", "5")) is RoundOutcome.DEALER_BUST
    assert resolve_outcome(cards("10", "8"), cards("9", "9")) is RoundOutcome.PUSH


def test_standard_deck_has_52_unique_cards():
    deck = standard_deck()
    assert len(deck) == 52
    assert len(set(deck)) == 52


def test_seeded_deal_is_reproducible():
    first = BlackjackRound.deal(Random(42))
    second = BlackjackRound.deal(Random(42))
    assert first.player_hand == second.player_hand
    assert first.dealer_hand == second.dealer_hand
