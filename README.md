# Flappy Bird NEAT AI

An AI that learns to play Flappy Bird using NeuroEvolution of Augmenting Topologies (NEAT) in Python with Pygame.

## 🧠 Neural Network (NEAT)

- **Inputs:**
  - Bird's current Y position
  - Distance between the bird and the top pipe
  - Distance between the bird and the bottom pipe

- **Output:**
  - A single value (between 0 and 1)
    - If output > 0.5 → the bird jumps
    - Otherwise → the bird does nothing

- **Activation Function:**
  - Default: `sigmoid` (set in `config_feedforward.txt`)

- **Fitness Function:**
  - +0.2 for each frame the bird survives
  - +5 for passing through a pipe
  - -1 if the bird hits a pipe

## 🎮 How to Run

1. Make sure you have Python 3 installed.
2. Install the required packages:
   ```bash
   pip install pygame neat-python
   ```
3. Ensure the `assets` folder exists and contains:
   - `bird1.png`, `bird2.png`, `bird3.png`
   - `pipe.png`, `base.png`, `bg.png`
4. Run the game:
   ```bash
   python flappy_game.py
   ```

## 📁 Files

- `flappy_game.py`: Main script containing the game and AI logic.
- `config_feedforward.txt`: NEAT configuration settings.
- `assets/`: Folder containing game image assets.

## 🖥️ Display

- Real-time visual simulation of birds learning to play.
- Displays current **score** and **generation** in the window.