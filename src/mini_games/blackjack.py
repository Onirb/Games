"""Blackjack rules and round state, independent from terminal input/output."""

from dataclasses import dataclass, field
from enum import StrEnum
from random import Random


RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace")
SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
RANK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11,
}


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self) -> None:
        if self.rank not in RANK_VALUES:
            raise ValueError(f"Unknown rank: {self.rank!r}")
        if self.suit not in SUITS:
            raise ValueError(f"Unknown suit: {self.suit!r}")

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"


class RoundOutcome(StrEnum):
    PLAYER_BLACKJACK = "player_blackjack"
    DEALER_BLACKJACK = "dealer_blackjack"
    BOTH_BLACKJACK = "both_blackjack"
    PLAYER_BUST = "player_bust"
    DEALER_BUST = "dealer_bust"
    PLAYER_WIN = "player_win"
    DEALER_WIN = "dealer_win"
    PUSH = "push"


def standard_deck() -> list[Card]:
    return [Card(rank, suit) for suit in SUITS for rank in RANKS]


def shuffled_deck(rng: Random | None = None) -> list[Card]:
    deck = standard_deck()
    (rng or Random()).shuffle(deck)
    return deck


def hand_value(hand: list[Card]) -> int:
    """Return the best Blackjack value without exceeding 21 when possible."""

    value = sum(RANK_VALUES[card.rank] for card in hand)
    aces = sum(card.rank == "Ace" for card in hand)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def is_soft_hand(hand: list[Card]) -> bool:
    """Return whether at least one Ace is still being counted as eleven."""

    aces = sum(card.rank == "Ace" for card in hand)
    if not aces:
        return False
    raw_value = sum(RANK_VALUES[card.rank] for card in hand)
    return hand_value(hand) == raw_value - 10 * (aces - 1)


def is_blackjack(hand: list[Card]) -> bool:
    return len(hand) == 2 and hand_value(hand) == 21


def resolve_outcome(player: list[Card], dealer: list[Card]) -> RoundOutcome:
    player_blackjack = is_blackjack(player)
    dealer_blackjack = is_blackjack(dealer)
    if player_blackjack and dealer_blackjack:
        return RoundOutcome.BOTH_BLACKJACK
    if player_blackjack:
        return RoundOutcome.PLAYER_BLACKJACK
    if dealer_blackjack:
        return RoundOutcome.DEALER_BLACKJACK

    player_total = hand_value(player)
    dealer_total = hand_value(dealer)
    if player_total > 21:
        return RoundOutcome.PLAYER_BUST
    if dealer_total > 21:
        return RoundOutcome.DEALER_BUST
    if player_total > dealer_total:
        return RoundOutcome.PLAYER_WIN
    if dealer_total > player_total:
        return RoundOutcome.DEALER_WIN
    return RoundOutcome.PUSH


@dataclass
class BlackjackRound:
    deck: list[Card]
    player_hand: list[Card] = field(default_factory=list)
    dealer_hand: list[Card] = field(default_factory=list)

    @classmethod
    def deal(cls, rng: Random | None = None) -> "BlackjackRound":
        round_state = cls(shuffled_deck(rng))
        for _ in range(2):
            round_state.player_hit()
            round_state.dealer_hand.append(round_state._draw())
        return round_state

    def _draw(self) -> Card:
        if not self.deck:
            raise RuntimeError("The deck is empty.")
        return self.deck.pop()

    def player_hit(self) -> Card:
        card = self._draw()
        self.player_hand.append(card)
        return card

    def dealer_play(self, *, hit_soft_17: bool = False) -> None:
        while True:
            value = hand_value(self.dealer_hand)
            if value < 17 or (hit_soft_17 and value == 17 and is_soft_hand(self.dealer_hand)):
                self.dealer_hand.append(self._draw())
            else:
                return

    @property
    def player_value(self) -> int:
        return hand_value(self.player_hand)

    @property
    def dealer_value(self) -> int:
        return hand_value(self.dealer_hand)

    @property
    def has_natural(self) -> bool:
        return is_blackjack(self.player_hand) or is_blackjack(self.dealer_hand)

    def outcome(self) -> RoundOutcome:
        return resolve_outcome(self.player_hand, self.dealer_hand)
