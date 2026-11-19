"""Terminal interface for the mini-games collection."""

import argparse
from collections.abc import Callable
from random import Random

from .blackjack import BlackjackRound, RoundOutcome
from .guessing import GuessFeedback, NumberGuessingGame
from .higher_lower import HigherLowerGame, STATIC_PROFILES


Input = Callable[[str], str]
Output = Callable[[str], None]


OUTCOME_MESSAGES = {
    RoundOutcome.PLAYER_BLACKJACK: "Blackjack! You win.",
    RoundOutcome.DEALER_BLACKJACK: "Dealer has Blackjack.",
    RoundOutcome.BOTH_BLACKJACK: "Both have Blackjack: push.",
    RoundOutcome.PLAYER_BUST: "You went over 21. Dealer wins.",
    RoundOutcome.DEALER_BUST: "Dealer went over 21. You win.",
    RoundOutcome.PLAYER_WIN: "You win.",
    RoundOutcome.DEALER_WIN: "Dealer wins.",
    RoundOutcome.PUSH: "Push.",
}


def ask_choice(prompt: str, choices: set[str], input_fn: Input) -> str:
    while True:
        answer = input_fn(prompt).strip().lower()
        if answer in choices:
            return answer


def play_blackjack(rng: Random, input_fn: Input = input, output: Output = print) -> None:
    game = BlackjackRound.deal(rng)
    output(f"Dealer shows: {game.dealer_hand[0]}")
    output(f"Your hand: {', '.join(map(str, game.player_hand))} ({game.player_value})")
    if not game.has_natural:
        while game.player_value < 21:
            choice = ask_choice("Hit or stand? [h/s]: ", {"h", "s"}, input_fn)
            if choice == "s":
                break
            card = game.player_hit()
            output(f"You drew {card}. Total: {game.player_value}")
        if game.player_value <= 21:
            game.dealer_play()
    output(f"Dealer hand: {', '.join(map(str, game.dealer_hand))} ({game.dealer_value})")
    output(OUTCOME_MESSAGES[game.outcome()])


def play_guessing(rng: Random, input_fn: Input = input, output: Output = print) -> None:
    difficulty = ask_choice("Difficulty [easy/hard]: ", {"easy", "hard"}, input_fn)
    game = NumberGuessingGame.create(difficulty, rng=rng)
    output("I chose a number between 1 and 100.")
    while not game.is_over:
        raw = input_fn(f"Guess ({game.attempts_remaining} attempts left): ").strip()
        try:
            value = int(raw)
            feedback = game.guess(value)
        except ValueError as error:
            output(str(error))
            continue
        if feedback is GuessFeedback.CORRECT:
            output(f"Correct! The number was {game.secret}.")
        elif feedback is GuessFeedback.TOO_LOW:
            output("Too low.")
        else:
            output("Too high.")
    if not game.won:
        output(f"No attempts left. The number was {game.secret}.")


def play_higher_lower(rng: Random, input_fn: Input = input, output: Output = print) -> None:
    game = HigherLowerGame(STATIC_PROFILES, rng)
    output("Values are a static gameplay snapshot, not live follower counts.")
    while game.active:
        output(f"A: {game.left.name} - {game.left.description}, {game.left.location}")
        output(f"B: {game.right.name} - {game.right.description}, {game.right.location}")
        choice = ask_choice("Who has the higher value? [A/B]: ", {"a", "b"}, input_fn)
        result = game.guess(choice)
        output(f"Values: A={result.left_value:,}; B={result.right_value:,}")
        if result.correct:
            output(f"Correct. Score: {result.score}")
        else:
            output(f"Wrong. Final score: {result.score}")


def menu(rng: Random, input_fn: Input = input, output: Output = print) -> None:
    games = {
        "1": ("Blackjack", play_blackjack),
        "2": ("Guess the Number", play_guessing),
        "3": ("Higher or Lower", play_higher_lower),
    }
    while True:
        output("\nMini Games")
        for key, (name, _) in games.items():
            output(f"{key}. {name}")
        output("q. Quit")
        choice = ask_choice("Choose: ", {*games, "q"}, input_fn)
        if choice == "q":
            return
        games[choice][1](rng, input_fn, output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "game",
        nargs="?",
        default="menu",
        choices=("menu", "blackjack", "guess", "higher-lower", "gui"),
    )
    parser.add_argument("--seed", type=int, help="Optional deterministic random seed.")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.game == "gui":
        from .gui import main as gui_main

        gui_main()
        return
    rng = Random(args.seed)
    commands = {
        "menu": menu,
        "blackjack": play_blackjack,
        "guess": play_guessing,
        "higher-lower": play_higher_lower,
    }
    commands[args.game](rng)
