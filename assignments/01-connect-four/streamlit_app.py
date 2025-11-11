import math
import random
from typing import List, Optional, Tuple

import numpy as np
import streamlit as st

ROWS = 6
COLUMNS = 7
CONNECT = 4

EMPTY = 0
PLAYER_HUMAN = 1
PLAYER_AI = 2

SYMBOLS = {EMPTY: "⬜️", PLAYER_HUMAN: "🟡", PLAYER_AI: "🔴"}


def create_board() -> np.ndarray:
    return np.zeros((ROWS, COLUMNS), dtype=int)


def drop_piece(board: np.ndarray, row: int, column: int, piece: int) -> None:
    board[row][column] = piece


def is_valid_location(board: np.ndarray, column: int) -> bool:
    return board[0][column] == EMPTY


def get_next_open_row(board: np.ndarray, column: int) -> Optional[int]:
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            return row
    return None


def get_valid_locations(board: np.ndarray) -> List[int]:
    return [c for c in range(COLUMNS) if is_valid_location(board, c)]


def winning_move(board: np.ndarray, piece: int) -> bool:
    # Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if np.all(board[r, c : c + CONNECT] == piece):
                return True
    # Vertical
    for c in range(COLUMNS):
        column = board[:, c]
        for r in range(ROWS - 3):
            if np.all(column[r : r + CONNECT] == piece):
                return True
    # Positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i, c + i] == piece for i in range(CONNECT)):
                return True
    # Negative diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + 3 - i, c + i] == piece for i in range(CONNECT)):
                return True
    return False


def evaluate_window(window: List[int], piece: int) -> int:
    score = 0
    opp_piece = PLAYER_HUMAN if piece == PLAYER_AI else PLAYER_AI

    count_piece = window.count(piece)
    count_opp = window.count(opp_piece)
    count_empty = window.count(EMPTY)

    if count_piece == 4:
        score += 1000
    elif count_piece == 3 and count_empty == 1:
        score += 100
    elif count_piece == 2 and count_empty == 2:
        score += 10

    if count_opp == 4:
        score -= 1000
    elif count_opp == 3 and count_empty == 1:
        score -= 100
    elif count_opp == 2 and count_empty == 2:
        score -= 10

    return score


def score_position(board: np.ndarray, piece: int) -> int:
    score = 0

    center_array = board[:, COLUMNS // 2]
    score += int(np.count_nonzero(center_array == piece)) * 6
    opp_piece = PLAYER_HUMAN if piece == PLAYER_AI else PLAYER_AI
    score -= int(np.count_nonzero(center_array == opp_piece)) * 6

    # Horizontal
    for r in range(ROWS):
        row_array = board[r, :]
        for c in range(COLUMNS - 3):
            window = row_array[c : c + CONNECT].tolist()
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLUMNS):
        col_array = board[:, c]
        for r in range(ROWS - 3):
            window = col_array[r : r + CONNECT].tolist()
            score += evaluate_window(window, piece)

    # Positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i, c + i] for i in range(CONNECT)]
            score += evaluate_window(window, piece)

    # Negative diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i, c + i] for i in range(CONNECT)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board: np.ndarray) -> bool:
    return (
        winning_move(board, PLAYER_HUMAN)
        or winning_move(board, PLAYER_AI)
        or len(get_valid_locations(board)) == 0
    )


def minimax(
    board: np.ndarray,
    depth: int,
    maximizing_player: bool,
) -> Tuple[Optional[int], int]:
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, PLAYER_AI):
                return None, math.inf
            if winning_move(board, PLAYER_HUMAN):
                return None, -math.inf
            return None, 0
        return None, score_position(board, PLAYER_AI)

    if maximizing_player:
        value = -math.inf
        best_column = random.choice(valid_locations)
        for column in valid_locations:
            row = get_next_open_row(board, column)
            if row is None:
                continue
            temp_board = board.copy()
            drop_piece(temp_board, row, column, PLAYER_AI)
            _, new_score = minimax(temp_board, depth - 1, False)
            if new_score > value:
                value = new_score
                best_column = column
        return best_column, value
    value = math.inf
    best_column = random.choice(valid_locations)
    for column in valid_locations:
        row = get_next_open_row(board, column)
        if row is None:
            continue
        temp_board = board.copy()
        drop_piece(temp_board, row, column, PLAYER_HUMAN)
        _, new_score = minimax(temp_board, depth - 1, True)
        if new_score < value:
            value = new_score
            best_column = column
    return best_column, value


def render_board(board: np.ndarray) -> None:
    st.markdown(
        "  " + " ".join(f"**{i+1}**" for i in range(COLUMNS)),
        unsafe_allow_html=True,
    )
    for row in board:
        st.markdown("  " + " ".join(SYMBOLS[cell] for cell in row))


def reset_game() -> None:
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.message = "Your turn! Choose a column."
    st.session_state.turn = PLAYER_HUMAN


def handle_human_move(column: int) -> None:
    board = st.session_state.board
    if not is_valid_location(board, column):
        st.session_state.message = "Column full. Try another."
        return
    row = get_next_open_row(board, column)
    if row is None:
        st.session_state.message = "Column full. Try another."
        return
    drop_piece(board, row, column, PLAYER_HUMAN)
    if winning_move(board, PLAYER_HUMAN):
        st.session_state.game_over = True
        st.session_state.message = "🎉 You win!"
        return
    if len(get_valid_locations(board)) == 0:
        st.session_state.game_over = True
        st.session_state.message = "🤝 It's a draw!"
        return
    st.session_state.turn = PLAYER_AI
    st.session_state.message = "Computer is thinking..."


def handle_ai_move() -> None:
    board = st.session_state.board
    column, _ = minimax(board, depth=3, maximizing_player=True)
    if column is None:
        column = random.choice(get_valid_locations(board))
    row = get_next_open_row(board, column)
    if row is None:
        column = random.choice(get_valid_locations(board))
        row = get_next_open_row(board, column)
    drop_piece(board, row, column, PLAYER_AI)
    if winning_move(board, PLAYER_AI):
        st.session_state.game_over = True
        st.session_state.message = "🤖 Computer wins!"
        return
    if len(get_valid_locations(board)) == 0:
        st.session_state.game_over = True
        st.session_state.message = "🤝 It's a draw!"
        return
    st.session_state.turn = PLAYER_HUMAN
    st.session_state.message = "Your turn! Choose a column."


def main() -> None:
    st.set_page_config(page_title="Connect Four AI", page_icon="🎮", layout="centered")
    st.title("Connect Four: Human vs. Minimax AI")

    if "board" not in st.session_state:
        reset_game()

    st.write(st.session_state.message)
    render_board(st.session_state.board)

    col_buttons = st.columns(COLUMNS)
    for idx, col in enumerate(col_buttons):
        if st.session_state.game_over:
            disabled = True
        else:
            disabled = st.session_state.turn != PLAYER_HUMAN or not is_valid_location(
                st.session_state.board, idx
            )
        if col.button(f"Drop {idx + 1}", disabled=disabled):
            handle_human_move(idx)

    if st.session_state.turn == PLAYER_AI and not st.session_state.game_over:
        handle_ai_move()
        render_board(st.session_state.board)

    st.divider()
    if st.button("🔄 Restart Game"):
        reset_game()
        st.experimental_rerun()


if __name__ == "__main__":
    main()

