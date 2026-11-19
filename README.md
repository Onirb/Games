# Python Mini Games

A small desktop mini-console and terminal collection refactored from early
Jupyter notebook exercises into a tested Python package.

The project demonstrates a practical software-engineering progression: preserve
the original work, separate domain rules from input/output, inject randomness
for deterministic tests and expose one consistent command-line interface.

> **Status:** active and continuously evolving. The current three games form
> the first functional release; new games and interface improvements will be
> added incrementally.

## Games

### Blackjack

A single-player round against a dealer with a standard deck, flexible Ace
values, natural Blackjack detection, dealer draw rules and complete outcomes.

### Guess the Number

Guess a number between 1 and 100 with explicit easy and hard attempt limits.
Invalid difficulty, non-integer input and out-of-range guesses are handled
without silently consuming an attempt.

### Higher or Lower

Compare two profiles and choose which has the larger value. The included values
are a **static historical/hypothetical gameplay snapshot** inherited from the
notebook exercise. They are not live follower counts.

## Desktop mini-console

The graphical interface uses Tkinter, included with the standard Windows
Python installation. It provides a dark arcade-style home screen, a card for
each game, in-app navigation and session score feedback.

```powershell
.\.venv\Scripts\python.exe -m mini_games gui
```

After installation, the dedicated launcher is also available:

```powershell
.\.venv\Scripts\mini-games-gui.exe
```

## Run locally

Validated with Python 3.12.

```powershell
git clone https://github.com/Onirb/Games.git
cd Games
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m mini_games gui
```

The terminal interface remains available, and individual games can be opened
directly:

```powershell
.\.venv\Scripts\python.exe -m mini_games blackjack
.\.venv\Scripts\python.exe -m mini_games guess
.\.venv\Scripts\python.exe -m mini_games higher-lower
```

Add `--seed 42` to reproduce the same random sequence during a demonstration.

## Test

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The tests cover Blackjack rules and Aces, deterministic deals, number-guessing
limits, Higher-or-Lower state transitions and terminal choice normalization.

## Structure

```text
src/mini_games/          Domain rules and terminal interface
src/mini_games/gui.py    Desktop mini-console and game screens
tests/                   Fast deterministic tests
notebooks/legacy/        Original notebook exercises, preserved unchanged
legacy/art.py            Original text-art helper
docs/LEGACY_NOTES.md     Audit and modernization boundary
```

## Design choices

- Runtime code has no third-party dependencies.
- Random generators are injected, making behavior reproducible in tests.
- Domain logic does not call `input()` or depend on Jupyter.
- The terminal and desktop interfaces share the same tested game rules.

See the [legacy audit](docs/LEGACY_NOTES.md) for the limitations that motivated
the refactor. Contributors and future maintainers can follow the
[new-game checklist](docs/ADDING_A_GAME.md) to extend the arcade consistently.

## Roadmap

- add new games as independent domain modules;
- expand the home screen without coupling games to each other;
- keep terminal and graphical access when appropriate;
- add tests for every rule before publishing a new game;
- consider persistent scores and optional visual assets in later releases.
