"""
Core game logic for Connect Four (7x6) used by both the Jupyter notebook
and the Streamlit web demo. Centralising these utilities keeps behaviour
identical across interfaces and avoids code duplication.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence, Tuple

# Board configuration
ROWS: int = 6
COLS: int = 7
CONNECT: int = 4

# Players
EMPTY: int = 0
HUMAN: int = 1
AI: int = 2

# Display tokens (matches the notebook UI)
TOKEN_MAP = {
    EMPTY: "⚪",
    HUMAN: "🔴",  # Human (red)
    AI: "🟡",  # Computer (yellow)
}


# --------------------------------------------------------------------------- #
# Board helpers
# --------------------------------------------------------------------------- #
def create_board() -> List[List[int]]:
    """Return a fresh 7x6 board initialised with zeros."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def copy_board(board: Sequence[Sequence[int]]) -> List[List[int]]:
    """Deep copy a board (list-of-lists)."""
    return [list(row) for row in board]


def is_valid_location(board: Sequence[Sequence[int]], col: int) -> bool:
    """A column is valid if it is in range and the top cell is empty."""
    return 0 <= col < COLS and board[0][col] == EMPTY


def get_next_open_row(board: Sequence[Sequence[int]], col: int) -> Optional[int]:
    """Return the lowest empty row index for a column, or None if full."""
    if not 0 <= col < COLS:
        return None
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None


def drop_piece(board: List[List[int]], row: int, col: int, piece: int) -> None:
    """Mutate the board by placing a piece at the specified row/column."""
    board[row][col] = piece


def board_full(board: Sequence[Sequence[int]]) -> bool:
    """True when every column is filled to the top."""
    return all(board[0][col] != EMPTY for col in range(COLS))


def get_valid_locations(board: Sequence[Sequence[int]]) -> List[int]:
    """Return all columns that can accept a move."""
    return [col for col in range(COLS) if is_valid_location(board, col)]


# --------------------------------------------------------------------------- #
# Win detection
# --------------------------------------------------------------------------- #
def winning_move(board: Sequence[Sequence[int]], piece: int) -> bool:
    """Check horizontal, vertical, and diagonal connect-four conditions."""
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + offset] == piece for offset in range(CONNECT)):
                return True

    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + offset][col] == piece for offset in range(CONNECT)):
                return True

    # Positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + offset][col + offset] == piece for offset in range(CONNECT)):
                return True

    # Negative diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - offset][col + offset] == piece for offset in range(CONNECT)):
                return True

    return False


# --------------------------------------------------------------------------- #
# Evaluation heuristic
# --------------------------------------------------------------------------- #
def evaluate_window(window: Sequence[int], piece: int) -> int:
    """Assign a score to a window of four cells."""
    opp_piece = HUMAN if piece == AI else AI
    count_self = window.count(piece)
    count_opp = window.count(opp_piece)
    count_empty = window.count(EMPTY)

    score = 0
    if count_self == 4:
        score += 100_000
    elif count_self == 3 and count_empty == 1:
        score += 100
    elif count_self == 2 and count_empty == 2:
        score += 10

    if count_opp == 4:
        score -= 100_000
    elif count_opp == 3 and count_empty == 1:
        score -= 120
    elif count_opp == 2 and count_empty == 2:
        score -= 12

    return score


def score_position(board: Sequence[Sequence[int]], piece: int = AI) -> int:
    """Evaluate the board from the perspective of `piece`."""
    score = 0

    center_column = COLS // 2
    score += sum(1 for row in range(ROWS) if board[row][center_column] == piece) * 6

    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [board[row][col + offset] for offset in range(CONNECT)]
            score += evaluate_window(window, piece)

    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [board[row + offset][col] for offset in range(CONNECT)]
            score += evaluate_window(window, piece)

    # Positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + offset][col + offset] for offset in range(CONNECT)]
            score += evaluate_window(window, piece)

    # Negative diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - offset][col + offset] for offset in range(CONNECT)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board: Sequence[Sequence[int]]) -> bool:
    """Terminal when someone wins or the board fills up."""
    return winning_move(board, HUMAN) or winning_move(board, AI) or board_full(board)


# --------------------------------------------------------------------------- #
# Minimax search
# --------------------------------------------------------------------------- #
def minimax(board: Sequence[Sequence[int]], depth: int, maximizing_player: bool) -> Tuple[int, Optional[int]]:
    """Depth-limited minimax returning (score, column)."""
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)

    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI):
                return (math.inf, None)
            if winning_move(board, HUMAN):
                return (-math.inf, None)
            return (0, None)
        return (score_position(board, AI), None)

    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            board_copy = copy_board(board)
            drop_piece(board_copy, row, col, AI)
            new_score, _ = minimax(board_copy, depth - 1, False)
            if new_score > value:
                value = new_score
                best_col = col
        return value, best_col

    value = math.inf
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        if row is None:
            continue
        board_copy = copy_board(board)
        drop_piece(board_copy, row, col, HUMAN)
        new_score, _ = minimax(board_copy, depth - 1, True)
        if new_score < value:
            value = new_score
            best_col = col
    return value, best_col


def ai_decide_move(board: Sequence[Sequence[int]], depth: int = 3) -> int:
    """Return the column chosen by the AI (falls back to random if needed)."""
    _, candidate = minimax(board, depth=depth, maximizing_player=True)
    if candidate is None:
        valid = get_valid_locations(board)
        return random.choice(valid) if valid else 0
    return candidate


# --------------------------------------------------------------------------- #
# Rendering helpers
# --------------------------------------------------------------------------- #
def board_to_html(board: Sequence[Sequence[int]]) -> str:
    """Render the board as HTML table (mirrors notebook styling)."""
    html = []
    # Column labels at the top
    html.append("<div style='text-align: center; margin-bottom: 8px;'>")
    for col in range(COLS):
        html.append(
            "<span style='display: inline-block; width: 50px; text-align: center; "
            "font-weight: bold; font-size: 1.1rem; color: #4455aa;'>"
            f"{col}</span>"
        )
    html.append("</div>")
    
    html.append("<table style='border-collapse: collapse; margin: 20px auto;'>")
    for row in range(ROWS):
        html.append("<tr>")
        for col in range(COLS):
            token = TOKEN_MAP[board[row][col]]
            html.append(
                "<td style='border: 2px solid #333; width: 50px; height: 50px; "
                "text-align: center; font-size: 24px;'>"
                f"{token}</td>"
            )
        html.append("</tr>")
    html.append("</table>")

    return "".join(html)

