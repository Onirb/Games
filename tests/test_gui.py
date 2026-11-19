from mini_games.blackjack import Card, RoundOutcome
from mini_games.cli import build_parser
from mini_games.gui import COLORS, format_hand, outcome_message


def test_gui_outcome_copy_covers_every_blackjack_outcome():
    for outcome in RoundOutcome:
        message, color = outcome_message(outcome)
        assert message
        assert color.startswith("#")


def test_gui_card_formatting_and_theme_contract():
    hand = [Card("Ace", "Spades"), Card("King", "Hearts")]
    assert format_hand(hand) == "Ace of Spades\nKing of Hearts"
    assert {"background", "surface", "card", "text", "cyan", "green", "red"} <= COLORS.keys()


def test_cli_exposes_graphical_console_command():
    assert build_parser().parse_args(["gui"]).game == "gui"
