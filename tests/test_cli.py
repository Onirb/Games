from mini_games.cli import ask_choice


def test_ask_choice_retries_until_input_is_valid():
    answers = iter(["invalid", " YES "])
    assert ask_choice("", {"yes", "no"}, lambda _: next(answers)) == "yes"
