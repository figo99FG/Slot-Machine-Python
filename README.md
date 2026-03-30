# Slot Machine — Python

A dynamic command-line slot machine game built with Python. Features betting, randomised weighted spins, win detection, payout calculation, and session statistics. Designed with OOP principles and validated with **10+ unit tests achieving 95%+ code coverage**.

---

## 🎰 Demo

```
╔══════════════════════════════════╗
║       🎰  SLOT MACHINE  🎰        ║
╚══════════════════════════════════╝

Symbols : 🍒 🍋 🔔 ⭐ 💎 7️⃣
Match 3 to win! Higher symbols = bigger multipliers.

Starting balance: £100

Enter bet (£1–£100, max £100) or 'q' to quit: 10

  [ 💎 | 💎 | 💎 ]
  🎉 WIN! Three 💎 — x25 multiplier — Payout: £250
  Balance: £340
```

---

## 🚀 Features

- **Weighted random spins** — rarer symbols have lower probability
- **Dynamic payouts** — multipliers scale with symbol rarity
- **Input validation** — handles invalid bets, strings, and edge cases
- **Session statistics** — tracks spins, total wagered, total won, and net
- **OOP design** — `SlotMachine` class with clean separation of logic
- **Unit tested** — 10+ tests with `pytest`, 95%+ coverage via `pytest-cov`

---

## 🎲 Symbols & Payouts

| Symbol | Rarity | Multiplier |
|--------|--------|-----------|
| 🍒 Cherry | Common | ×2 |
| 🍋 Lemon | Common | ×3 |
| 🔔 Bell | Uncommon | ×5 |
| ⭐ Star | Rare | ×10 |
| 💎 Diamond | Very Rare | ×25 |
| 7️⃣ Seven | Jackpot | ×50 |

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Testing**: `pytest`, `unittest.mock`
- **Coverage**: `pytest-cov`
- **Design**: OOP — `SlotMachine` class

---

## 📁 Project Structure

```
Slot-Machine-Python/
├── slot_machine.py        # Core game logic and CLI
├── test_slot_machine.py   # Unit tests (10+ tests, 95%+ coverage)
└── README.md
```

---

## ⚙️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/figo99FG/Slot-Machine-Python.git
cd Slot-Machine-Python
```

**2. Run the game**
```bash
python3 slot_machine.py
```

**3. Run unit tests**
```bash
pip install pytest pytest-cov
python -m pytest test_slot_machine.py -v
```

**4. Check coverage**
```bash
python -m pytest --cov=slot_machine --cov-report=term-missing
```

---

## 📚 Concepts Demonstrated

- Object-oriented design with encapsulation
- Weighted probability using `random.choices()`
- Input validation and error handling
- Unit testing with `pytest` and `unittest.mock`
- Code coverage analysis
- Session state tracking across multiple rounds

---

## 👤 Author

**Figo Figo** — BSc Networking & Security, Middlesex University London  
🌐 [figo.me.uk](https://figo.me.uk) · 💼 [LinkedIn](https://www.linkedin.com/in/figo-figo-1204642b2)
