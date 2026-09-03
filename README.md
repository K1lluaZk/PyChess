# PyChess ♟️🎮

**PyChess** is a modular chess game built in Python and Pygame featuring full chess mechanics, an AI opponent, a progression and points system, guest and registered account support with SQLite persistence, multiple board visual themes, and a responsive modern user interface.

---

## 🌟 Key Features

- **Full Chess Engine & Mechanics**:
  - Valid move generation for all piece types (Pawns, Knights, Bishops, Rooks, Queens, Kings).
  - Proper check, checkmate, and stalemate detection.
  - Automatic pawn promotion to Queen on back rank.
  - Turn system with responsive AI opponent for Black.
  - Visual valid-move indicators and check warnings.
- **Account & Guest System**:
  - **Guest Mode**: Play instantly without registration. Session points are tracked during current gameplay.
  - **Registered Accounts**: Create or log into user accounts. Points are permanently saved in a local SQLite database (`pychess.db`).
- **Points & Rewards Engine**:
  - Configurable points rewards for piece captures, promotions, delivering check, checkmate, and winning matches.
  - Real-time match score calculation and breakdown summary on game conclusion.
- **Modern User Interface**:
  - Interactive **Main Menu** with hover animations and player profile status.
  - In-game **Side Panel** displaying current turn, match score, captured pieces list, and controls.
  - **Points & Leaderboard Screen** with scoring guide and top players ranking.
  - **Game Settings Screen** with customizable board themes (*Classic Slate*, *Emerald Forest*, *Ocean Breeze*, *Warm Wood*) and audio/visual toggles.
  - **Result Screen** detailing match outcome and points breakdown.
- **Modular & Maintainable Architecture**:
  - Clean separation of concerns across `config/`, `database/`, `player/`, `game/`, and `ui/`.

---

## 📂 Project Structure

```text
PyChess/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── pychess.db                  # SQLite database (auto-generated)
│
├── config/                     # Settings and point values
│   ├── settings.py             # Display, board themes, UI palette
│   └── points_config.py        # Centralized point values & reward rules
│
├── database/                   # SQLite data persistence layer
│   ├── db.py                   # DB connection & schema initialization
│   ├── models.py               # User and score models
│   └── repository.py           # UserRepository CRUD operations & leaderboards
│
├── player/                     # Player state & session handling
│   └── session.py              # Guest vs Authenticated user session manager
│
├── game/                       # Core chess game logic
│   ├── constants.py            # Piece identifiers, colors, board layout
│   ├── board.py                # Board 8x8 matrix representation & state
│   ├── moves.py                # Move generation for all 6 piece types
│   ├── rules.py                # Check, checkmate, and stalemate validation
│   ├── ai.py                   # AI move selection for Black
│   ├── points_engine.py        # Match events & score calculation
│   └── game_state.py           # Turn coordinator & match state manager
│
├── ui/                         # Pygame graphical user interface
│   ├── screen_manager.py       # Screen transition & state manager
│   ├── components/             # Reusable UI widgets (Buttons, Inputs, Cards, Theme)
│   └── screens/                # UI Screens (Home, Account, Game, Points, Settings, Result)
│
├── assets/                     # Game assets
│   └── images/
│       └── pieces/             # Chess piece PNG graphics
│
└── tests/                      # Automated test suite
    ├── test_chess_logic.py     # Move generation, check, checkmate, points tests
    ├── test_database.py        # SQLite persistence & session tests
    └── test_ui_smoke.py        # Screen lifecycle & navigation smoke tests
```

---

## 📦 Requirements & Installation

1. **Python 3.8+** installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/K1lluaZk/pychess.git
   cd pychess
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🕹️ How to Play

Run the application:
```bash
python main.py
```

### Gameplay Controls:
1. **Home Screen**: Start game, manage accounts, view points & rules, or adjust settings.
2. **Move Pieces**: Click on any of your white pieces to see highlighted valid moves, then click a valid destination square.
3. **Capture & Score**: Earn points by capturing enemy pieces, delivering checks, and winning by checkmate.
4. **End Game**: When the game concludes, review your earned points and return to the main menu or play again.

---

## 🏆 Points System Reference

| Event | Reward |
| :--- | :--- |
| **Capture Pawn** | `+10 pts` |
| **Capture Knight** | `+30 pts` |
| **Capture Bishop** | `+30 pts` |
| **Capture Rook** | `+50 pts` |
| **Capture Queen** | `+90 pts` |
| **Pawn Promotion** | `+40 pts` |
| **Deliver Check** | `+20 pts` |
| **Deliver Checkmate** | `+100 pts` |
| **Victory Bonus** | `+200 pts` |

---

## 🧪 Running Tests

To run the automated unit test suite:
```bash
python -m unittest discover -s tests
```

---

## 📄 License

This project is licensed under the MIT License.
