"""Number-guessing game state with explicit validation and attempt limits."""

from dataclasses import dataclass, field
from enum import StrEnum
from random import Random


DIFFICULTY_ATTEMPTS = {"easy": 10, "hard": 5}


class GuessFeedback(StrEnum):
    TOO_LOW = "too_low"
    TOO_HIGH = "too_high"
    CORRECT = "correct"


@dataclass
class NumberGuessingGame:
    secret: int
    attempt_limit: int
    lower_bound: int = 1
    upper_bound: int = 100
    guesses: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.lower_bound >= self.upper_bound:
            raise ValueError("lower_bound must be smaller than upper_bound.")
        if not self.lower_bound <= self.secret <= self.upper_bound:
            raise ValueError("secret must be inside the configured range.")
        if self.attempt_limit < 1:
            raise ValueError("attempt_limit must be positive.")

    @classmethod
    def create(
        cls,
        difficulty: str,
        *,
        rng: Random | None = None,
        lower_bound: int = 1,
        upper_bound: int = 100,
    ) -> "NumberGuessingGame":
        normalized = difficulty.strip().lower()
        if normalized not in DIFFICULTY_ATTEMPTS:
            choices = ", ".join(DIFFICULTY_ATTEMPTS)
            raise ValueError(f"Unknown difficulty {difficulty!r}. Choose: {choices}.")
        generator = rng or Random()
        return cls(
            secret=generator.randint(lower_bound, upper_bound),
            attempt_limit=DIFFICULTY_ATTEMPTS[normalized],
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

    def guess(self, value: int) -> GuessFeedback:
        if self.is_over:
            raise RuntimeError("The game is already over.")
        if not self.lower_bound <= value <= self.upper_bound:
            raise ValueError(
                f"Guess must be between {self.lower_bound} and {self.upper_bound}."
            )
        self.guesses.append(value)
        if value < self.secret:
            return GuessFeedback.TOO_LOW
        if value > self.secret:
            return GuessFeedback.TOO_HIGH
        return GuessFeedback.CORRECT

    @property
    def attempts_used(self) -> int:
        return len(self.guesses)

    @property
    def attempts_remaining(self) -> int:
        return max(0, self.attempt_limit - self.attempts_used)

    @property
    def won(self) -> bool:
        return bool(self.guesses) and self.guesses[-1] == self.secret

    @property
    def is_over(self) -> bool:
        return self.won or self.attempts_remaining == 0
