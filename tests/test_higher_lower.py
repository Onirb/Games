from random import Random

import pytest

from mini_games.higher_lower import HigherLowerGame, Profile


PROFILES = (
    Profile("Low", "Test", "A", 10),
    Profile("Middle", "Test", "B", 20),
    Profile("High", "Test", "C", 30),
)


def test_seeded_game_is_reproducible():
    first = HigherLowerGame(PROFILES, Random(4))
    second = HigherLowerGame(PROFILES, Random(4))
    assert (first.left, first.right) == (second.left, second.right)


def test_correct_guess_increments_score_and_keeps_winner():
    game = HigherLowerGame(PROFILES, Random(1))
    winner = game.left if game.left.followers > game.right.followers else game.right
    choice = "a" if winner is game.left else "b"
    result = game.guess(choice)
    assert result.correct and result.score == 1 and not result.game_over
    assert game.left == winner
    assert game.left != game.right


def test_wrong_guess_ends_game():
    game = HigherLowerGame(PROFILES, Random(1))
    correct = "a" if game.left.followers > game.right.followers else "b"
    wrong = "b" if correct == "a" else "a"
    result = game.guess(wrong)
    assert not result.correct and result.game_over and not game.active
    with pytest.raises(RuntimeError):
        game.guess(correct)


def test_choice_and_profiles_are_validated():
    game = HigherLowerGame(PROFILES, Random(1))
    with pytest.raises(ValueError):
        game.guess("c")
    with pytest.raises(ValueError):
        HigherLowerGame((PROFILES[0],), Random(1))
