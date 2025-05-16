# Yinsh AI Game

This project is an implementation of the board game **Yinsh**, featuring multiple game modes and AI strategies.

## 🎮 Game Modes

- **Player vs Player**
- **Player vs AI**
- **AI vs AI**

## 🧠 AI Algorithms

The AI players in this project use two different strategies:

- **Minimax with Alpha-Beta Pruning**: A depth-limited search algorithm that prunes unneeded branches for performance.
- **Monte Carlo Tree Search (MCTS)**: A probabilistic approach that simulates many possible future game states to choose the best move.

## 🖥️ How to Run

Make sure you have Python installed. Then simply run:

```bash
python3 main.py
```

The GUI will launch, allowing you to choose the desired game mode.

## 📂 Project Structure:

- main.py: Entry point and game launcher

- GUI.py: Graphical user interface for interaction

- YinshGame.py: Core game logic and rules

- IA_player.py: AI player logic (Minimax and MCTS)

- Human_player.py: Handles human player input

- Random_player.py: Optional simple random-move player

- macros.py: Constants and utility functions

- boardState.py: Representation of the game board

- Menu.py: Game mode and player selection menu

## 📖 About Yinsh:

[Yinsh](https://en.wikipedia.org/wiki/YINSH) is a two-player abstract strategy board game and part of the GIPF project series. The goal is to remove three of your own rings by forming lines of five markers.

<hr>

> Project developed for Artificial Inteligence course @FEUP.
