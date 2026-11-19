"""Dark desktop mini-console for the three games using only Tkinter."""

from __future__ import annotations

import tkinter as tk
from random import Random
from tkinter import messagebox

from .blackjack import BlackjackRound, RoundOutcome
from .guessing import GuessFeedback, NumberGuessingGame
from .higher_lower import HigherLowerGame, STATIC_PROFILES


COLORS = {
    "background": "#070b14",
    "surface": "#101827",
    "card": "#172033",
    "border": "#273449",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "cyan": "#38bdf8",
    "blue": "#2563eb",
    "green": "#22c55e",
    "red": "#ef4444",
    "gold": "#f59e0b",
}

FONT = "Segoe UI"


def flat_button(parent, text: str, command, *, color: str | None = None, width: int = 16):
    background = color or COLORS["blue"]
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=background,
        fg=COLORS["text"],
        activebackground=COLORS["cyan"],
        activeforeground=COLORS["background"],
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        font=(FONT, 11, "bold"),
        padx=16,
        pady=10,
        width=width,
    )


def panel(parent, **grid_options):
    frame = tk.Frame(
        parent,
        bg=COLORS["card"],
        highlightbackground=COLORS["border"],
        highlightthickness=1,
        padx=22,
        pady=20,
    )
    if grid_options:
        frame.grid(**grid_options)
    return frame


def format_hand(hand) -> str:
    return "\n".join(str(card) for card in hand)


def outcome_message(outcome: RoundOutcome) -> tuple[str, str]:
    messages = {
        RoundOutcome.PLAYER_BLACKJACK: ("Blackjack! You win.", COLORS["green"]),
        RoundOutcome.DEALER_BLACKJACK: ("Dealer has Blackjack.", COLORS["red"]),
        RoundOutcome.BOTH_BLACKJACK: ("Both have Blackjack. Push.", COLORS["gold"]),
        RoundOutcome.PLAYER_BUST: ("You went over 21. Dealer wins.", COLORS["red"]),
        RoundOutcome.DEALER_BUST: ("Dealer went over 21. You win.", COLORS["green"]),
        RoundOutcome.PLAYER_WIN: ("You win this round.", COLORS["green"]),
        RoundOutcome.DEALER_WIN: ("Dealer wins this round.", COLORS["red"]),
        RoundOutcome.PUSH: ("Equal hands. Push.", COLORS["gold"]),
    }
    return messages[outcome]


class MiniGamesApp(tk.Tk):
    def __init__(self, seed: int | None = None) -> None:
        super().__init__()
        self.title("Python Mini Games")
        self.geometry("1120x720")
        self.minsize(920, 620)
        self.configure(bg=COLORS["background"])
        self.rng = Random(seed)
        self.content = tk.Frame(self, bg=COLORS["background"])
        self.content.pack(fill="both", expand=True)
        self.show_home()

    def show(self, view_class) -> None:
        for child in self.content.winfo_children():
            child.destroy()
        view_class(self.content, self).pack(fill="both", expand=True)

    def show_home(self) -> None:
        self.show(HomeView)

    def show_blackjack(self) -> None:
        self.show(BlackjackView)

    def show_guessing(self) -> None:
        self.show(GuessingView)

    def show_higher_lower(self) -> None:
        self.show(HigherLowerView)


class HomeView(tk.Frame):
    def __init__(self, parent, app: MiniGamesApp) -> None:
        super().__init__(parent, bg=COLORS["background"], padx=54, pady=42)
        tk.Label(
            self,
            text="PYTHON MINI ARCADE",
            bg=COLORS["background"],
            fg=COLORS["cyan"],
            font=(FONT, 13, "bold"),
        ).pack(anchor="w")
        tk.Label(
            self,
            text="Choose your game",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=(FONT, 32, "bold"),
        ).pack(anchor="w", pady=(8, 4))
        tk.Label(
            self,
            text="Three classic exercises rebuilt as a single testable desktop application.",
            bg=COLORS["background"],
            fg=COLORS["muted"],
            font=(FONT, 12),
        ).pack(anchor="w", pady=(0, 28))

        cards = tk.Frame(self, bg=COLORS["background"])
        cards.pack(fill="both", expand=True)
        for column in range(3):
            cards.grid_columnconfigure(column, weight=1, uniform="games")
        cards.grid_rowconfigure(0, weight=1)

        games = (
            ("21", "Blackjack", "Build the strongest hand without going over 21.", app.show_blackjack, COLORS["green"]),
            ("1-100", "Guess the Number", "Use high and low hints before your attempts run out.", app.show_guessing, COLORS["cyan"]),
            ("A / B", "Higher or Lower", "Compare two profiles and build a winning streak.", app.show_higher_lower, COLORS["gold"]),
        )
        for column, (badge, title, description, command, accent) in enumerate(games):
            card = panel(cards, row=0, column=column, sticky="nsew", padx=8, pady=4)
            tk.Label(
                card,
                text=badge,
                bg=COLORS["card"],
                fg=accent,
                font=(FONT, 26, "bold"),
            ).pack(anchor="w", pady=(8, 26))
            tk.Label(
                card,
                text=title,
                bg=COLORS["card"],
                fg=COLORS["text"],
                font=(FONT, 18, "bold"),
            ).pack(anchor="w")
            tk.Label(
                card,
                text=description,
                bg=COLORS["card"],
                fg=COLORS["muted"],
                font=(FONT, 11),
                justify="left",
                wraplength=250,
            ).pack(anchor="w", pady=(10, 24))
            flat_button(card, "PLAY", command, color=accent, width=12).pack(anchor="w", side="bottom")

        tk.Label(
            self,
            text="Local only  |  No account  |  No online services",
            bg=COLORS["background"],
            fg=COLORS["muted"],
            font=(FONT, 9),
        ).pack(anchor="e", pady=(18, 0))


class GameView(tk.Frame):
    title = "Game"
    subtitle = ""

    def __init__(self, parent, app: MiniGamesApp) -> None:
        super().__init__(parent, bg=COLORS["background"], padx=38, pady=28)
        self.app = app
        header = tk.Frame(self, bg=COLORS["background"])
        header.pack(fill="x", pady=(0, 22))
        flat_button(header, "<  ARCADE", app.show_home, color=COLORS["surface"], width=10).pack(side="left")
        title_box = tk.Frame(header, bg=COLORS["background"])
        title_box.pack(side="left", padx=24)
        tk.Label(
            title_box, text=self.title, bg=COLORS["background"], fg=COLORS["text"],
            font=(FONT, 24, "bold"),
        ).pack(anchor="w")
        tk.Label(
            title_box, text=self.subtitle, bg=COLORS["background"], fg=COLORS["muted"],
            font=(FONT, 10),
        ).pack(anchor="w")


class BlackjackView(GameView):
    title = "Blackjack"
    subtitle = "Dealer stands on 17. Aces adjust automatically."

    def __init__(self, parent, app: MiniGamesApp) -> None:
        super().__init__(parent, app)
        self.wins = self.losses = self.pushes = 0
        self.finished = False

        body = tk.Frame(self, bg=COLORS["background"])
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure((0, 1), weight=1, uniform="hands")
        body.grid_rowconfigure(0, weight=1)
        self.dealer_panel = panel(body, row=0, column=0, sticky="nsew", padx=(0, 8))
        self.player_panel = panel(body, row=0, column=1, sticky="nsew", padx=(8, 0))
        self.dealer_cards = self._hand_panel(self.dealer_panel, "DEALER")
        self.player_cards = self._hand_panel(self.player_panel, "YOUR HAND")

        controls = tk.Frame(self, bg=COLORS["background"])
        controls.pack(fill="x", pady=(18, 0))
        self.status = tk.Label(
            controls, text="", bg=COLORS["background"], fg=COLORS["cyan"],
            font=(FONT, 13, "bold"),
        )
        self.status.pack(side="left")
        self.scoreboard = tk.Label(
            controls, text="", bg=COLORS["background"], fg=COLORS["muted"],
            font=(FONT, 10),
        )
        self.scoreboard.pack(side="left", padx=18)
        self.new_button = flat_button(controls, "NEW ROUND", self.new_round, color=COLORS["surface"], width=12)
        self.new_button.pack(side="right", padx=(8, 0))
        self.stand_button = flat_button(controls, "STAND", self.stand, color=COLORS["gold"], width=9)
        self.stand_button.pack(side="right", padx=(8, 0))
        self.hit_button = flat_button(controls, "HIT", self.hit, color=COLORS["green"], width=9)
        self.hit_button.pack(side="right")
        self.new_round()

    def _hand_panel(self, parent, heading: str):
        tk.Label(parent, text=heading, bg=COLORS["card"], fg=COLORS["muted"], font=(FONT, 10, "bold")).pack(anchor="w")
        label = tk.Label(
            parent, text="", bg=COLORS["card"], fg=COLORS["text"],
            font=(FONT, 16, "bold"), justify="left", anchor="nw",
        )
        label.pack(fill="both", expand=True, pady=(18, 0))
        return label

    def new_round(self) -> None:
        self.game = BlackjackRound.deal(self.app.rng)
        self.finished = False
        self.status.configure(text="Choose hit or stand.", fg=COLORS["cyan"])
        self._set_actions(True)
        if self.game.has_natural:
            self.finish()
        else:
            self.refresh()

    def refresh(self) -> None:
        if self.finished:
            dealer_text = f"{format_hand(self.game.dealer_hand)}\n\nTotal: {self.game.dealer_value}"
        else:
            dealer_text = f"{self.game.dealer_hand[0]}\n[ hidden card ]"
        self.dealer_cards.configure(text=dealer_text)
        self.player_cards.configure(text=f"{format_hand(self.game.player_hand)}\n\nTotal: {self.game.player_value}")
        self.scoreboard.configure(text=f"W {self.wins}   L {self.losses}   Push {self.pushes}")

    def _set_actions(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.hit_button.configure(state=state)
        self.stand_button.configure(state=state)

    def hit(self) -> None:
        if self.finished:
            return
        self.game.player_hit()
        if self.game.player_value > 21:
            self.finish()
        elif self.game.player_value == 21:
            self.game.dealer_play()
            self.finish()
        else:
            self.refresh()

    def stand(self) -> None:
        if self.finished:
            return
        self.game.dealer_play()
        self.finish()

    def finish(self) -> None:
        self.finished = True
        outcome = self.game.outcome()
        message, color = outcome_message(outcome)
        if outcome in {RoundOutcome.PLAYER_BLACKJACK, RoundOutcome.DEALER_BUST, RoundOutcome.PLAYER_WIN}:
            self.wins += 1
        elif outcome in {RoundOutcome.BOTH_BLACKJACK, RoundOutcome.PUSH}:
            self.pushes += 1
        else:
            self.losses += 1
        self.status.configure(text=message, fg=color)
        self._set_actions(False)
        self.refresh()


class GuessingView(GameView):
    title = "Guess the Number"
    subtitle = "Find a number from 1 to 100 before your attempts run out."

    def __init__(self, parent, app: MiniGamesApp) -> None:
        super().__init__(parent, app)
        self.difficulty = tk.StringVar(value="easy")
        card = panel(self)
        card.pack(fill="both", expand=True)

        selector = tk.Frame(card, bg=COLORS["card"])
        selector.pack(anchor="w")
        tk.Label(selector, text="DIFFICULTY", bg=COLORS["card"], fg=COLORS["muted"], font=(FONT, 10, "bold")).pack(side="left", padx=(0, 16))
        for value, label in (("easy", "EASY - 10"), ("hard", "HARD - 5")):
            tk.Radiobutton(
                selector, text=label, variable=self.difficulty, value=value,
                command=self.new_game, indicatoron=False, selectcolor=COLORS["blue"],
                bg=COLORS["surface"], fg=COLORS["text"], activebackground=COLORS["cyan"],
                activeforeground=COLORS["background"], font=(FONT, 10, "bold"),
                relief="flat", padx=14, pady=8,
            ).pack(side="left", padx=4)

        self.hint = tk.Label(
            card, text="", bg=COLORS["card"], fg=COLORS["cyan"],
            font=(FONT, 28, "bold"),
        )
        self.hint.pack(pady=(70, 12))
        self.attempts = tk.Label(card, text="", bg=COLORS["card"], fg=COLORS["muted"], font=(FONT, 11))
        self.attempts.pack()
        self.entry = tk.Entry(
            card, bg=COLORS["surface"], fg=COLORS["text"], insertbackground=COLORS["text"],
            relief="flat", justify="center", font=(FONT, 24, "bold"), width=8,
        )
        self.entry.pack(pady=22, ipady=8)
        self.entry.bind("<Return>", lambda _: self.submit())
        self.guess_button = flat_button(card, "GUESS", self.submit, color=COLORS["cyan"], width=12)
        self.guess_button.pack()
        self.history = tk.Label(
            card, text="", bg=COLORS["card"], fg=COLORS["muted"],
            font=(FONT, 10), wraplength=760,
        )
        self.history.pack(pady=(28, 0))
        self.new_game()

    def new_game(self) -> None:
        self.game = NumberGuessingGame.create(self.difficulty.get(), rng=self.app.rng)
        self.hint.configure(text="Make your first guess", fg=COLORS["cyan"])
        self.history.configure(text="Previous guesses: -")
        self.entry.configure(state="normal")
        self.guess_button.configure(state="normal", text="GUESS", command=self.submit)
        self.entry.delete(0, "end")
        self.attempts.configure(text=f"{self.game.attempts_remaining} attempts remaining")
        self.entry.focus_set()

    def submit(self) -> None:
        if self.game.is_over:
            self.new_game()
            return
        try:
            value = int(self.entry.get().strip())
            feedback = self.game.guess(value)
        except ValueError as error:
            messagebox.showinfo("Invalid guess", str(error), parent=self)
            return
        self.entry.delete(0, "end")
        self.history.configure(text="Previous guesses: " + ", ".join(map(str, self.game.guesses)))
        self.attempts.configure(text=f"{self.game.attempts_remaining} attempts remaining")
        if feedback is GuessFeedback.CORRECT:
            self.hint.configure(text=f"Correct - the number was {self.game.secret}", fg=COLORS["green"])
            self._finish("PLAY AGAIN")
        elif self.game.is_over:
            self.hint.configure(text=f"No attempts left - it was {self.game.secret}", fg=COLORS["red"])
            self._finish("TRY AGAIN")
        elif feedback is GuessFeedback.TOO_LOW:
            self.hint.configure(text="Too low", fg=COLORS["gold"])
        else:
            self.hint.configure(text="Too high", fg=COLORS["gold"])

    def _finish(self, button_text: str) -> None:
        self.entry.configure(state="disabled")
        self.guess_button.configure(text=button_text, command=self.new_game)


class HigherLowerView(GameView):
    title = "Higher or Lower"
    subtitle = "Static gameplay values - not live social-media measurements."

    def __init__(self, parent, app: MiniGamesApp) -> None:
        super().__init__(parent, app)
        self.body = tk.Frame(self, bg=COLORS["background"])
        self.body.pack(fill="both", expand=True)
        self.body.grid_columnconfigure((0, 1), weight=1, uniform="profiles")
        self.body.grid_rowconfigure(0, weight=1)
        self.left_panel = panel(self.body, row=0, column=0, sticky="nsew", padx=(0, 8))
        self.right_panel = panel(self.body, row=0, column=1, sticky="nsew", padx=(8, 0))
        self.left_name, self.left_detail, self.left_value = self._profile_panel(self.left_panel, "A")
        self.right_name, self.right_detail, self.right_value = self._profile_panel(self.right_panel, "B")

        controls = tk.Frame(self, bg=COLORS["background"])
        controls.pack(fill="x", pady=(18, 0))
        self.status = tk.Label(
            controls, text="", bg=COLORS["background"], fg=COLORS["cyan"],
            font=(FONT, 13, "bold"),
        )
        self.status.pack(side="left")
        self.score_label = tk.Label(
            controls, text="", bg=COLORS["background"], fg=COLORS["muted"], font=(FONT, 11),
        )
        self.score_label.pack(side="left", padx=20)
        self.next_button = flat_button(controls, "NEW GAME", self.new_game, color=COLORS["surface"], width=12)
        self.next_button.pack(side="right", padx=(8, 0))
        self.b_button = flat_button(controls, "CHOOSE B", lambda: self.choose("b"), color=COLORS["gold"], width=11)
        self.b_button.pack(side="right", padx=(8, 0))
        self.a_button = flat_button(controls, "CHOOSE A", lambda: self.choose("a"), color=COLORS["cyan"], width=11)
        self.a_button.pack(side="right")
        self.new_game()

    def _profile_panel(self, parent, badge: str):
        tk.Label(parent, text=badge, bg=COLORS["card"], fg=COLORS["cyan"], font=(FONT, 24, "bold")).pack(anchor="w")
        name = tk.Label(parent, text="", bg=COLORS["card"], fg=COLORS["text"], font=(FONT, 20, "bold"), wraplength=390, justify="left")
        name.pack(anchor="w", pady=(32, 10))
        detail = tk.Label(parent, text="", bg=COLORS["card"], fg=COLORS["muted"], font=(FONT, 11), wraplength=390, justify="left")
        detail.pack(anchor="w")
        value = tk.Label(parent, text="Hidden value", bg=COLORS["card"], fg=COLORS["gold"], font=(FONT, 15, "bold"))
        value.pack(anchor="w", side="bottom", pady=(20, 0))
        return name, detail, value

    def new_game(self) -> None:
        self.game = HigherLowerGame(STATIC_PROFILES, self.app.rng)
        self.status.configure(text="Which value is higher?", fg=COLORS["cyan"])
        self.next_button.configure(text="NEW GAME", command=self.new_game)
        self._show_profiles()
        self._set_choices(True)

    def _show_profiles(self) -> None:
        self.left_name.configure(text=self.game.left.name)
        self.left_detail.configure(text=f"{self.game.left.description}\n{self.game.left.location}")
        self.right_name.configure(text=self.game.right.name)
        self.right_detail.configure(text=f"{self.game.right.description}\n{self.game.right.location}")
        self.left_value.configure(text="Hidden value")
        self.right_value.configure(text="Hidden value")
        self.score_label.configure(text=f"Score: {self.game.score}")

    def _set_choices(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.a_button.configure(state=state)
        self.b_button.configure(state=state)

    def choose(self, choice: str) -> None:
        result = self.game.guess(choice)
        self.left_value.configure(text=f"{result.left_value:,}")
        self.right_value.configure(text=f"{result.right_value:,}")
        self.score_label.configure(text=f"Score: {result.score}")
        self._set_choices(False)
        if result.correct:
            self.status.configure(text="Correct! Continue your streak.", fg=COLORS["green"])
            self.next_button.configure(text="NEXT ROUND", command=self.next_round)
        else:
            self.status.configure(text="Wrong choice. Start a new streak.", fg=COLORS["red"])
            self.next_button.configure(text="PLAY AGAIN", command=self.new_game)

    def next_round(self) -> None:
        self._show_profiles()
        self.status.configure(text="Which value is higher?", fg=COLORS["cyan"])
        self._set_choices(True)


def main() -> None:
    app = MiniGamesApp()
    app.mainloop()


if __name__ == "__main__":
    main()
