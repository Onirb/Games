from random import Random

import pytest

from mini_games.guessing import GuessFeedback, NumberGuessingGame


def test_feedback_and_win_state():
    game = NumberGuessingGame(secret=50, attempt_limit=3)
    assert game.guess(25) is GuessFeedback.TOO_LOW
    assert game.guess(75) is GuessFeedback.TOO_HIGH
    assert game.guess(50) is GuessFeedback.CORRECT
    assert game.won and game.is_over and game.attempts_remaining == 0


def test_attempt_limit_ends_game():
    game = NumberGuessingGame(secret=10, attempt_limit=2)
    game.guess(1)
    game.guess(2)
    assert game.is_over and not game.won
    with pytest.raises(RuntimeError):
        game.guess(10)


def test_out_of_range_guess_does_not_consume_attempt():
    game = NumberGuessingGame(secret=10, attempt_limit=2)
    with pytest.raises(ValueError):
        game.guess(101)
    assert game.attempts_remaining == 2


def test_difficulty_is_validated_and_seed_is_reproducible():
    first = NumberGuessingGame.create("easy", rng=Random(7))
    second = NumberGuessingGame.create("easy", rng=Random(7))
    assert first.secret == second.secret
    assert first.attempt_limit == 10
    with pytest.raises(ValueError):
        NumberGuessingGame.create("unknown")
