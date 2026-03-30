"""
Unit Tests — Slot Machine
Author: Figo Figo

10+ unit tests covering core game logic.
Run with: python -m pytest test_slot_machine.py -v --tb=short
Coverage: python -m pytest --cov=slot_machine --cov-report=term-missing
"""

import pytest
from unittest.mock import patch
from slot_machine import SlotMachine, PAYOUTS, MIN_BET, MAX_BET, STARTING_BALANCE


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def machine():
    """Fresh SlotMachine with default starting balance."""
    return SlotMachine()


@pytest.fixture
def low_balance_machine():
    """SlotMachine with just enough for one minimum bet."""
    return SlotMachine(starting_balance=1)


# ── Initialisation Tests ──────────────────────────────────────────────────────

class TestInit:
    def test_default_balance(self, machine):
        assert machine.balance == STARTING_BALANCE

    def test_custom_balance(self):
        m = SlotMachine(starting_balance=500)
        assert m.balance == 500

    def test_invalid_zero_balance(self):
        with pytest.raises(ValueError):
            SlotMachine(starting_balance=0)

    def test_invalid_negative_balance(self):
        with pytest.raises(ValueError):
            SlotMachine(starting_balance=-50)

    def test_initial_stats_zero(self, machine):
        assert machine.total_spins == 0
        assert machine.total_wagered == 0
        assert machine.total_won == 0


# ── Bet Validation Tests ──────────────────────────────────────────────────────

class TestValidateBet:
    def test_valid_bet(self, machine):
        assert machine.validate_bet(10) is True

    def test_bet_minimum(self, machine):
        assert machine.validate_bet(MIN_BET) is True

    def test_bet_maximum(self, machine):
        assert machine.validate_bet(MAX_BET) is True

    def test_bet_below_minimum(self, machine):
        assert machine.validate_bet(0) is False

    def test_bet_above_maximum(self, machine):
        assert machine.validate_bet(MAX_BET + 1) is False

    def test_bet_exceeds_balance(self, low_balance_machine):
        assert low_balance_machine.validate_bet(2) is False

    def test_non_integer_bet(self, machine):
        assert machine.validate_bet(5.5) is False

    def test_string_bet(self, machine):
        assert machine.validate_bet("ten") is False


# ── Spin Tests ────────────────────────────────────────────────────────────────

class TestSpin:
    def test_spin_returns_three_symbols(self, machine):
        result = machine.spin()
        assert len(result) == 3

    def test_spin_returns_valid_symbols(self, machine):
        valid = set(PAYOUTS.keys())
        result = machine.spin()
        for symbol in result:
            assert symbol in valid

    def test_spin_randomness(self, machine):
        results = [tuple(machine.spin()) for _ in range(50)]
        assert len(set(results)) > 1


# ── Win Detection Tests ───────────────────────────────────────────────────────

class TestCheckWin:
    def test_three_matching_symbols_is_win(self, machine):
        is_win, multiplier, symbol = machine.check_win(["🍒", "🍒", "🍒"])
        assert is_win is True
        assert symbol == "🍒"
        assert multiplier == PAYOUTS["🍒"]

    def test_jackpot_symbol_payout(self, machine):
        is_win, multiplier, symbol = machine.check_win(["7️⃣", "7️⃣", "7️⃣"])
        assert is_win is True
        assert multiplier == PAYOUTS["7️⃣"]

    def test_two_matching_is_not_win(self, machine):
        is_win, multiplier, symbol = machine.check_win(["🍒", "🍒", "🍋"])
        assert is_win is False
        assert multiplier == 0
        assert symbol is None

    def test_all_different_is_not_win(self, machine):
        is_win, _, _ = machine.check_win(["🍒", "🍋", "🔔"])
        assert is_win is False


# ── Payout Calculation Tests ──────────────────────────────────────────────────

class TestCalculatePayout:
    def test_payout_correct(self, machine):
        assert machine.calculate_payout(10, 5) == 50

    def test_payout_zero_multiplier(self, machine):
        assert machine.calculate_payout(10, 0) == 0

    def test_payout_minimum_bet(self, machine):
        assert machine.calculate_payout(1, PAYOUTS["7️⃣"]) == PAYOUTS["7️⃣"]


# ── Play Round Tests ──────────────────────────────────────────────────────────

class TestPlayRound:
    def test_balance_reduced_by_bet_on_loss(self, machine):
        with patch.object(machine, "spin", return_value=["🍒", "🍋", "🔔"]):
            machine.play_round(10)
        assert machine.balance == STARTING_BALANCE - 10

    def test_balance_increased_on_win(self, machine):
        with patch.object(machine, "spin", return_value=["💎", "💎", "💎"]):
            result = machine.play_round(10)
        expected = STARTING_BALANCE - 10 + (10 * PAYOUTS["💎"])
        assert machine.balance == expected
        assert result["is_win"] is True

    def test_invalid_bet_raises(self, machine):
        with pytest.raises(ValueError):
            machine.play_round(0)

    def test_spin_count_increments(self, machine):
        machine.play_round(5)
        machine.play_round(5)
        assert machine.total_spins == 2

    def test_wagered_tracked(self, machine):
        machine.play_round(10)
        machine.play_round(20)
        assert machine.total_wagered == 30

    def test_round_result_keys(self, machine):
        result = machine.play_round(5)
        for key in ["result", "is_win", "symbol", "multiplier", "bet", "payout", "balance"]:
            assert key in result


# ── Stats Tests ───────────────────────────────────────────────────────────────

class TestGetStats:
    def test_stats_after_no_play(self, machine):
        stats = machine.get_stats()
        assert stats["total_spins"] == 0
        assert stats["net"] == 0

    def test_net_negative_after_loss(self, machine):
        with patch.object(machine, "spin", return_value=["🍒", "🍋", "🔔"]):
            machine.play_round(10)
        stats = machine.get_stats()
        assert stats["net"] == -10

    def test_net_positive_after_jackpot(self, machine):
        with patch.object(machine, "spin", return_value=["7️⃣", "7️⃣", "7️⃣"]):
            machine.play_round(10)
        stats = machine.get_stats()
        assert stats["net"] == 10 * PAYOUTS["7️⃣"] - 10
