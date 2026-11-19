# Legacy notebook audit

The repository originally contained three directly executable notebooks. They
are preserved under `notebooks/legacy/` as historical evidence.

## Blackjack

- Hand-value and Blackjack functions depended on a global card-value mapping.
- Game execution happened at cell execution time.
- Replay accepted only the exact string `Yes`, while other prompts normalized
  case.
- Rules, random deck state and terminal interaction were mixed together.

## Guess the Number

- Any difficulty other than `easy` silently became hard.
- Non-integer and out-of-range input were not handled.
- Random generation, terminal interaction and attempt state were inseparable.

## Higher or Lower

- The game required `IPython.display`, so it was not a normal terminal program.
- Data, display and state transitions lived in one notebook cell.
- Several follower values were explicitly hypothetical and therefore could not
  be represented as current measurements.

## Modernization boundary

The modern package preserves the original game concepts while extracting pure,
testable rules. The follower dataset is retained only as a labelled static game
snapshot. No live social-media accuracy is claimed.
