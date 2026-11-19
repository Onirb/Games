# Adding a game

The mini arcade is intended to grow over time. New games should remain isolated
from existing rules and expose a small interface that the terminal or desktop
layers can call.

## Checklist

1. Create a domain module under `src/mini_games/`.
2. Keep game rules independent from `input()`, `print()` and Tkinter widgets.
3. Accept a `random.Random` instance when randomness affects behavior.
4. Add deterministic tests under `tests/` for rules, validation and end states.
5. Add a graphical view to `gui.py` and register its card on `HomeView`.
6. Add a terminal command only when the game works naturally in a console.
7. Document controls and any data-source limitations in `README.md`.
8. Run the complete test suite and inspect the desktop layout before commit.

## Minimum domain contract

A game module should make its state explicit and provide methods that perform
one meaningful transition. The interface layer is responsible only for reading
user actions and rendering the resulting state.

```python
game = NewGame(rng=random.Random(seed))
result = game.perform(action)
```

Avoid module-level execution and mutable global game state. Static data may be
stored in immutable tuples or dedicated data files, with provenance and age
clearly documented when the values represent the outside world.
