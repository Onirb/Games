"""Reusable Higher-or-Lower engine with a static, explicit data snapshot."""

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class Profile:
    name: str
    description: str
    location: str
    followers: int

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.description.strip():
            raise ValueError("Profile name and description are required.")
        if self.followers < 0:
            raise ValueError("followers cannot be negative.")


@dataclass(frozen=True)
class HigherLowerResult:
    correct: bool
    score: int
    left_value: int
    right_value: int
    game_over: bool


class HigherLowerGame:
    """State machine for repeated comparisons of two distinct profiles."""

    def __init__(self, profiles: tuple[Profile, ...], rng: Random | None = None) -> None:
        if len(profiles) < 2:
            raise ValueError("At least two profiles are required.")
        if len({profile.name for profile in profiles}) != len(profiles):
            raise ValueError("Profile names must be unique.")
        self.profiles = profiles
        self.rng = rng or Random()
        self.score = 0
        self.active = True
        self.left, self.right = self.rng.sample(self.profiles, 2)

    def guess(self, choice: str) -> HigherLowerResult:
        if not self.active:
            raise RuntimeError("The game is already over.")
        normalized = choice.strip().lower()
        if normalized not in {"a", "b"}:
            raise ValueError("Choice must be 'A' or 'B'.")

        if self.left.followers == self.right.followers:
            correct = True
            winner = self.right
        else:
            winning_choice = "a" if self.left.followers > self.right.followers else "b"
            correct = normalized == winning_choice
            winner = self.left if winning_choice == "a" else self.right

        result = HigherLowerResult(
            correct=correct,
            score=self.score + int(correct),
            left_value=self.left.followers,
            right_value=self.right.followers,
            game_over=not correct,
        )
        if not correct:
            self.active = False
            return result

        self.score += 1
        self.left = winner
        candidates = [profile for profile in self.profiles if profile != self.left]
        self.right = self.rng.choice(candidates)
        return result


# Historical/hypothetical values retained for gameplay only. They are not a
# live social-media dataset and must not be presented as current measurements.
STATIC_PROFILES = (
    Profile("Cristiano Ronaldo", "Footballer", "Portugal", 600_000_000),
    Profile("Ariana Grande", "Singer", "United States", 380_000_000),
    Profile("Dwayne Johnson", "Actor", "United States", 390_000_000),
    Profile("Lionel Messi", "Footballer", "Argentina", 482_000_000),
    Profile("Selena Gomez", "Singer and actor", "United States", 429_000_000),
    Profile("National Geographic", "Media organization", "United States", 200_000_000),
    Profile("NASA", "Space agency", "United States", 180_000_000),
    Profile("Taylor Swift", "Singer and songwriter", "United States", 500_000_000),
    Profile("Ed Sheeran", "Singer and songwriter", "United Kingdom", 450_000_000),
    Profile("LeBron James", "Basketball player", "United States", 90_000_000),
)
