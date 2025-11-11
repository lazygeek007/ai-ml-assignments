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
        st.session_state.last_ai_column = None


def reset_game() -> None:
    st.session_state.board = create_board()
    st.session_state.turn = HUMAN
    st.session_state.game_over = False
    st.session_state.message = (
        "<h3>🎮 New Game Started!</h3>"
        "<p>👤 Your turn! Click a column to drop your piece.</p>"
    )
    st.session_state.pending_ai = False
    st.session_state.last_ai_column = None


def human_move(column: int) -> None:
    if st.session_state.game_over or st.session_state.turn != HUMAN:
        return

    board = st.session_state.board
    st.session_state.last_ai_column = None
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
    st.session_state.last_ai_column = column + 1

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
        f"<h3>🤖 Computer played column {st.session_state.last_ai_column}</h3>"
        "<p>👤 Your turn! Pick your next column.</p>"
    )


def refresh_ui(status_placeholder, board_placeholder) -> None:
    status_placeholder.markdown(
        f'<div class="status-box">{st.session_state.message}</div>',
        unsafe_allow_html=True,
    )
    board_placeholder.markdown(
        f'<div class="board-container">{board_to_html(st.session_state.board)}</div>',
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Connect Four AI",
        page_icon="🎮",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS for game styling
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header styling */
    .game-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        color: white;
    }
    
    .game-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .game-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    /* Status message styling */
    .status-box {
        background: #fff;
        padding: 1.25rem 1rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 6px rgba(102, 126, 234, 0.15);
        margin-bottom: 1rem;
        text-align: left;
    }
    
    /* Board container */
    .board-container {
        display: flex;
        justify-content: center;
        margin: 1rem auto;
        padding: 1rem 1.5rem;
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        max-width: 520px;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 50px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: 2px solid #667eea;
    }
    
    .stButton > button:hover:not(:disabled) {
        background-color: #667eea;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }
    
    /* New Game button */
    .new-game-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        margin-top: 1rem;
    }
    
    /* Column number labels */
    .column-label {
        text-align: center;
        font-weight: 600;
        color: #4455aa;
        margin: 0.25rem 0 0.5rem 0;
    }
    
    .info-card {
        background: #fff;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        border-top: 4px solid #764ba2;
    }
    .info-card h4 {
        margin-top: 0;
        color: #44337a;
    }
    .info-card ul {
        padding-left: 1.1rem;
    }
    .info-card li {
        margin-bottom: 0.4rem;
    }
    .info-card span {
        color: #4a5568;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .game-header h1 {
            font-size: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Game Header
    st.markdown("""
    <div class="game-header">
        <h1>🎮 Connect Four</h1>
        <p>Challenge the Minimax AI • First to connect 4 wins!</p>
    </div>
    """, unsafe_allow_html=True)

    init_game()

    if st.session_state.pending_ai and not st.session_state.game_over:
        ai_move()
        st.session_state.pending_ai = False

    left_col, middle_col, right_col = st.columns([1.2, 2.4, 1.2])

    status_placeholder = left_col.empty()
    info_placeholder = right_col.empty()
    board_placeholder = middle_col.empty()

    refresh_ui(status_placeholder, board_placeholder)

    info_placeholder.markdown(
        """
        <div class="info-card">
            <h4>How to Play</h4>
            <ul>
                <li>Drop discs to connect four in a row.</li>
                <li>Use the drop buttons to pick a column.</li>
                <li>Yellow AI responds instantly using depth-3 Minimax.</li>
                <li>Game ends when someone connects four or the grid fills up.</li>
            </ul>
            <span>Tip: control the center to create multiple threats.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = len(st.session_state.board[0])
    label_cols = middle_col.columns(cols)
    for idx, col in enumerate(label_cols):
        col.markdown(
            f'<div class="column-label">{idx + 1}</div>',
            unsafe_allow_html=True,
        )

    button_row = middle_col.columns(cols)
    for idx, column in enumerate(button_row):
        disabled = (
            st.session_state.game_over
            or st.session_state.turn != HUMAN
            or not is_valid_location(st.session_state.board, idx)
        )
        button_text = "⬇ Drop" if not disabled else "—"
        if column.button(button_text, key=f"col_{idx}", disabled=disabled):
            human_move(idx)
            refresh_ui(status_placeholder, board_placeholder)

    spacer = middle_col.empty()
    spacer.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

    new_game_container = middle_col.container()
    if new_game_container.button("🔄 New Game", use_container_width=True):
        reset_game()
        refresh_ui(status_placeholder, board_placeholder)
        st.session_state.last_ai_column = None
        st.rerun()


if __name__ == "__main__":
    main()

