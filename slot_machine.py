"""
Slot Machine Game — Python
Author: Figo Figo
BSc Networking & Security, Middlesex University London

A dynamic command-line slot machine with betting, randomised spins,
win detection, and payout calculation. Built with OOP principles
and validated with 10+ unit tests (95%+ coverage).
"""

import random


# --- Configuration ---

SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "💎", "7️⃣"]

SYMBOL_WEIGHTS = {
    "🍒": 35,
    "🍋": 25,
    "🔔": 20,
    "⭐": 12,
    "💎": 6,
    "7️⃣": 2,
}

PAYOUTS = {
    "🍒": 2,
    "🍋": 3,
    "🔔": 5,
    "⭐": 10,
    "💎": 25,
    "7️⃣": 50,
}

MIN_BET = 1
MAX_BET = 100
STARTING_BALANCE = 100
REELS = 3


class SlotMachine:
    def __init__(self, starting_balance: int = STARTING_BALANCE):
        if starting_balance <= 0:
            raise ValueError("Starting balance must be greater than zero.")
        self.balance = starting_balance
        self.total_spins = 0
        self.total_won = 0
        self.total_wagered = 0

    def validate_bet(self, bet: int) -> bool:
        """Return True if bet is valid given current balance and limits."""
        if not isinstance(bet, int):
            return False
        if bet < MIN_BET or bet > MAX_BET:
            return False
        if bet > self.balance:
            return False
        return True

    def spin(self) -> list:
        """Spin the reels and return a list of REELS symbols."""
        population = list(SYMBOL_WEIGHTS.keys())
        weights = list(SYMBOL_WEIGHTS.values())
        return random.choices(population, weights=weights, k=REELS)

    def check_win(self, result: list) -> tuple:
        """
        Check if the spin result is a win.
        Returns (is_win: bool, payout_multiplier: int, symbol: str)
        """
        if len(set(result)) == 1:
            symbol = result[0]
            return True, PAYOUTS[symbol], symbol
        return False, 0, None

    def calculate_payout(self, bet: int, multiplier: int) -> int:
        """Calculate the payout amount from bet and multiplier."""
        return bet * multiplier

    def play_round(self, bet: int) -> dict:
        """
        Play one round of the slot machine.
        Returns a dict with round results.
        Raises ValueError if bet is invalid.
        """
        if not self.validate_bet(bet):
            raise ValueError(
                f"Invalid bet: {bet}. Bet must be between {MIN_BET} and "
                f"{MAX_BET} and not exceed your balance of {self.balance}."
            )

        self.balance -= bet
        self.total_wagered += bet
        self.total_spins += 1

        result = self.spin()
        is_win, multiplier, symbol = self.check_win(result)
        payout = 0

        if is_win:
            payout = self.calculate_payout(bet, multiplier)
            self.balance += payout
            self.total_won += payout

        return {
            "result": result,
            "is_win": is_win,
            "symbol": symbol,
            "multiplier": multiplier,
            "bet": bet,
            "payout": payout,
            "balance": self.balance,
        }

    def get_stats(self) -> dict:
        """Return session statistics."""
        net = self.total_won - self.total_wagered
        return {
            "total_spins": self.total_spins,
            "total_wagered": self.total_wagered,
            "total_won": self.total_won,
            "net": net,
            "balance": self.balance,
        }


# --- Display Helpers ---

def display_result(round_data: dict):
    """Print the result of a round to the terminal."""
    reels = " | ".join(round_data["result"])
    print(f"\n  [ {reels} ]")
    if round_data["is_win"]:
        print(
            f"  🎉 WIN! Three {round_data['symbol']} — "
            f"x{round_data['multiplier']} multiplier — "
            f"Payout: £{round_data['payout']}"
        )
    else:
        print("  No win. Try again!")
    print(f"  Balance: £{round_data['balance']}")


def display_stats(stats: dict):
    """Print session statistics."""
    print("\n── Session Stats ──────────────────")
    print(f"  Spins       : {stats['total_spins']}")
    print(f"  Total Bet   : £{stats['total_wagered']}")
    print(f"  Total Won   : £{stats['total_won']}")
    net = stats['net']
    sign = "+" if net >= 0 else ""
    print(f"  Net         : {sign}£{net}")
    print(f"  Balance     : £{stats['balance']}")
    print("───────────────────────────────────")


def get_bet(balance: int) -> int | None:
    """Prompt the user for a bet. Returns None if they want to quit."""
    while True:
        raw = input(f"\nEnter bet (£{MIN_BET}–£{MAX_BET}, max £{balance}) or 'q' to quit: ").strip()
        if raw.lower() == "q":
            return None
        try:
            bet = int(raw)
            if bet < MIN_BET or bet > MAX_BET:
                print(f"  Bet must be between £{MIN_BET} and £{MAX_BET}.")
            elif bet > balance:
                print(f"  You only have £{balance}.")
            else:
                return bet
        except ValueError:
            print("  Please enter a whole number.")


# --- Main Game Loop ---

def main():
    print("╔══════════════════════════════════╗")
    print("║       🎰  SLOT MACHINE  🎰        ║")
    print("╚══════════════════════════════════╝")
    print(f"\nSymbols : {' '.join(SYMBOLS)}")
    print("Match 3 to win! Higher symbols = bigger multipliers.\n")

    machine = SlotMachine()
    print(f"Starting balance: £{machine.balance}")

    while machine.balance >= MIN_BET:
        bet = get_bet(machine.balance)
        if bet is None:
            print("\nThanks for playing!")
            break

        round_data = machine.play_round(bet)
        display_result(round_data)

        if machine.balance < MIN_BET:
            print("\n  You've run out of funds. Game over!")
            break
    else:
        print("\n  Insufficient balance to continue. Game over!")

    display_stats(machine.get_stats())


if __name__ == "__main__":
    main()
