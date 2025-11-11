# Assignment 01: Connect Four with Fixed-Depth Minimax

## Objective

Build a two-player Connect Four game (7x6 grid) where a human competes against a computer agent powered by a depth-limited Minimax algorithm (depth = 3).

## Deliverables

- `ConnectFourGame _Final.ipynb` – full notebook implementation with interactive console play.
- `streamlit_app.py` – Streamlit web application for live demos.
- `connect_four_core.py` – shared logic module consumed by both notebook and Streamlit interfaces.
- `requirements.txt` – minimal dependencies (`streamlit`) for deploying the app.

## Notebook Walkthrough

- 7x6 grid representation via reusable helpers from `connect_four_core.py`.
- Human vs. computer gameplay loop with validated moves.
- Depth-3 Minimax agent using handcrafted heuristics (win/block/center control).
- Win/draw detection after every turn with clear board visualization.

Run locally:

```
jupyter notebook "ConnectFourGame _Final.ipynb"
```

Execute all cells to initialize helpers and play the prompt-based game in the notebook.

## Streamlit Web Demo

Launch locally:

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Deploy to [Streamlit Community Cloud](https://share.streamlit.io/):

1. Push this assignment directory to GitHub.  
2. On Streamlit Cloud, create a new app pointing to `assignments/01-connect-four/streamlit_app.py`.  
3. Select the repo branch and set the working directory if prompted.  
4. Provide `assignments/01-connect-four/requirements.txt` so dependencies install automatically.  
5. Copy the generated URL and replace the placeholder below:

```
Live Demo: https://<your-app>.streamlit.app
```

## Reflection Questions

- How does the evaluation function influence play style?  
- Which board configurations trick the Minimax agent at depth 3?  
- What improvements would iterative deepening or alpha-beta pruning bring?  
- Could move ordering or transposition tables make depth 4+ feasible in real time?

Document answers (or TODOs) in the notebook markdown cells as you experiment, and update the README with new insights when the demo is live.

