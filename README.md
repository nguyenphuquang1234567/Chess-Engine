# ♟️ Chess Engine GUI using Python, Pygame, and Stockfish
A fully interactive chess application built with Python and Pygame, featuring integration with the powerful Stockfish engine via UCI protocol. The app allows users to play chess with real-time AI evaluation, undo moves, and customize the interface.
# 🎯 Features
1. 🧠 Play against the Stockfish engine (UCI)
2. ♟️ Drag-and-drop piece movement
3. 🔁 Undo last move
4. 🧩 Highlight legal moves
5. 📈 Real-time position evaluation by Stockfish
6. 🕹️ Player vs Player mode
# 🛠️ Tech Stack
1. Python 3
2. Pygame — for graphics and input
3. python-chess — handles board logic and UCI communication
4. Stockfish — used as the backend engine
# 📸 Screenshots
<img width="565" alt="Ảnh màn hình 2025-06-15 lúc 11 20 16" src="https://github.com/user-attachments/assets/d02658b9-66a5-4f9d-843c-01021196fbca" />

# Usage
```bash
pip install pygame
```
```bash
pip install chess
```
--------------------
# 🔧 Project Structure 
```bash
Chess/
├── Chess/
│   ├── main.py              # Main game loop and rendering
│   ├── chess_engine.py      # Handles Stockfish logic + move control
│   └── ...                  # Other modules (UI, events, etc.)
└── stockfish/
    └── stockfish        # Stockfish engine binary
```

# Instructions
1. Download Stockfish from here https://stockfishchess.org/download/
2. Open the StockFish folder, RENAME the stockfish file in the folder to " stockfish ", RENAME the folder to " stockfish "
3. Clone this repository.
4. Put the stockfish folder and my Chess folder in the same folder
5. Run ChessMain.py
6. Select whether you want to play versus computer, against another player locally, or watch the game of engine playing against itself
# Important key pressed
1. Press z to undo a move.
2. Press r to reset the game.




