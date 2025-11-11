# Assignment 01: Connect Four with Fixed-Depth Minimax

## Overview

A two-player Connect Four game (7x6 grid) where a human competes against a computer agent powered by a depth-limited Minimax algorithm (depth = 3).

## Live Demo

**Play the game:** [https://connectfourgame.streamlit.app/](https://connectfourgame.streamlit.app/)

## Screenshot

![Connect Four Game](screenshot.png)

## Project Structure

- `ConnectFourGame _Final.ipynb` – Full notebook implementation with interactive console play
- `streamlit_app.py` – Streamlit web application
- `connect_four_core.py` – Shared game logic module used by both notebook and Streamlit app
- `requirements.txt` – Dependencies for the Streamlit app

## Features

- 7x6 grid representation with validated moves
- Human vs. computer gameplay
- Depth-3 Minimax AI agent with strategic heuristics (win detection, blocking, center control)
- Real-time win/draw detection
- Interactive board visualization

## Local Setup

### Notebook

```bash
jupyter notebook "ConnectFourGame _Final.ipynb"
```

### Streamlit App

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Technical Details

The Minimax algorithm evaluates board positions using:
- Win/block detection (highest priority)
- Center column control
- Window-based scoring for potential threats
- Static evaluation function for non-terminal positions
