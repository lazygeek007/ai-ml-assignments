import random

import streamlit as st

from connect_four_core import (
    AI,
    EMPTY,
    HUMAN,
    ai_decide_move,
    board_full,
    board_to_html,
    create_board,
    drop_piece,
    get_next_open_row,
    get_valid_locations,
    is_valid_location,
    winning_move,
)


def init_game() -> None:
    if "board" not in st.session_state:
        st.session_state.board = create_board()
        st.session_state.turn = HUMAN
        st.session_state.game_over = False
        st.session_state.message = (
            "<h3>🎮 Connect Four Game</h3>"
            "<p>👤 Your turn! Click a column to drop your piece.</p>"
        )
        st.session_state.pending_ai = False


def reset_game() -> None:
    st.session_state.board = create_board()
    st.session_state.turn = HUMAN
    st.session_state.game_over = False
    st.session_state.message = (
        "<h3>🎮 New Game Started!</h3>"
        "<p>👤 Your turn! Click a column to drop your piece.</p>"
    )
    st.session_state.pending_ai = False


def render_interface(status_placeholder, board_placeholder) -> None:
    status_placeholder.markdown(st.session_state.message, unsafe_allow_html=True)
    board_placeholder.markdown(board_to_html(st.session_state.board), unsafe_allow_html=True)


def human_move(column: int) -> None:
    if st.session_state.game_over or st.session_state.turn != HUMAN:
        return

    board = st.session_state.board
    if not is_valid_location(board, column):
        st.session_state.message = (
            "<h3>⚠️ Invalid Move!</h3>"
            "<p>Column is full or out of range. Please try another column.</p>"
        )
        return

    row = get_next_open_row(board, column)
    if row is None:
        st.session_state.message = (
            "<h3>⚠️ Column Full!</h3><p>Please choose another column.</p>"
        )
        return

    drop_piece(board, row, column, HUMAN)

    if winning_move(board, HUMAN):
        st.session_state.game_over = True
        st.session_state.message = (
            "<h3>🎉 CONGRATULATIONS! YOU WON! 🎉</h3>"
            "<p>You connected four — fantastic strategy!</p>"
        )
        return

    if board_full(board):
        st.session_state.game_over = True
        st.session_state.message = (
            "<h3>🤝 IT'S A DRAW! 🤝</h3>"
            "<p>The board is full — great game!</p>"
        )
        return

    st.session_state.turn = AI
    st.session_state.pending_ai = True
    st.session_state.message = (
        "<h3>🤖 Computer is thinking…</h3>"
        "<p>The AI is calculating its move.</p>"
    )


def ai_move() -> None:
    if st.session_state.game_over or st.session_state.turn != AI:
        return

    board = st.session_state.board
    column = ai_decide_move(board, depth=3)
    row = get_next_open_row(board, column)
    if row is None:
        valid = get_valid_locations(board)
        if not valid:
            st.session_state.game_over = True
            st.session_state.message = (
                "<h3>🤝 IT'S A DRAW! 🤝</h3>"
                "<p>The board is full — great game!</p>"
            )
            return
        column = random.choice(valid)
        row = get_next_open_row(board, column)

    drop_piece(board, row, column, AI)

    if winning_move(board, AI):
        st.session_state.game_over = True
        st.session_state.message = (
            "<h3>🤖 COMPUTER WINS! 🤖</h3>"
            "<p>Better luck next time — the AI found a winning line.</p>"
        )
        return

    if board_full(board):
        st.session_state.game_over = True
        st.session_state.message = (
            "<h3>🤝 IT'S A DRAW! 🤝</h3>"
            "<p>The board is full — great game!</p>"
        )
        return

    st.session_state.turn = HUMAN
    st.session_state.pending_ai = False
    st.session_state.message = (
        "<h3>👤 Your turn!</h3>"
        "<p>Click a column to drop your piece.</p>"
    )


def main() -> None:
    st.set_page_config(page_title="Connect Four AI", page_icon="🎮", layout="centered")
    st.title("Connect Four: Human vs. Minimax AI")

    init_game()

    status_placeholder = st.empty()
    board_placeholder = st.empty()

    render_interface(status_placeholder, board_placeholder)

    button_row = st.columns(len(st.session_state.board[0]))
    for idx, column in enumerate(button_row):
        disabled = (
            st.session_state.game_over
            or st.session_state.turn != HUMAN
            or not is_valid_location(st.session_state.board, idx)
        )
        if column.button(f"Col {idx}", disabled=disabled):
            human_move(idx)
            render_interface(status_placeholder, board_placeholder)

    if st.session_state.pending_ai and not st.session_state.game_over:
        ai_move()
        st.session_state.pending_ai = False
        render_interface(status_placeholder, board_placeholder)

    st.divider()
    if st.button("🔄 New Game"):
        reset_game()
        render_interface(status_placeholder, board_placeholder)
        st.experimental_rerun()


if __name__ == "__main__":
    main()

