"""Streamlit web application for Connect Four game with Minimax AI."""

import random

import streamlit as st

from connect_four_core import (
    AI,
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

# Constants
INITIAL_MESSAGE = (
    "<h3>🎮 Connect Four Game</h3>"
    "<p>👤 Your turn! Click a column to drop your piece.</p>"
)
NEW_GAME_MESSAGE = (
    "<h3>🎮 New Game Started!</h3>"
    "<p>👤 Your turn! Click a column to drop your piece.</p>"
)
INVALID_MOVE_MESSAGE = (
    "<h3>⚠️ Invalid Move!</h3>"
    "<p>Column is full or out of range. Please try another column.</p>"
)
COLUMN_FULL_MESSAGE = (
    "<h3>⚠️ Column Full!</h3><p>Please choose another column.</p>"
)
HUMAN_WIN_MESSAGE = (
    "<h3>🎉 CONGRATULATIONS! YOU WON! 🎉</h3>"
    "<p>You connected four — fantastic strategy!</p>"
)
AI_WIN_MESSAGE = (
    "<h3>🤖 COMPUTER WINS! 🤖</h3>"
    "<p>Better luck next time — the AI found a winning line.</p>"
)
DRAW_MESSAGE = (
    "<h3>🤝 IT'S A DRAW! 🤝</h3>"
    "<p>The board is full — great game!</p>"
)

# CSS Styles
CSS_STYLES = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    max-width: 1200px;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
}
.game-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
    color: white;
}
.game-header h1 { margin: 0; font-size: 2rem; font-weight: bold; }
.game-header p { margin: 0.5rem 0 0 0; font-size: 1rem; color: rgba(255,255,255,0.9); }
.status-box {
    background: #fff;
    padding: 1.25rem 1rem;
    border-radius: 12px;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 6px rgba(102, 126, 234, 0.15);
    margin-bottom: 1rem;
    text-align: left;
}
.board-wrapper {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    padding: 1rem 1.5rem 1.25rem 1.5rem;
    width: 100%;
}
.board-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0.5rem auto 1rem auto;
    width: 100%;
}
.board-container > div {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.board-container table {
    margin: 0 auto !important;
}
.board-table-wrapper {
    width: 350px !important;
}
.board-game-table {
    width: 350px !important;
    box-sizing: border-box !important;
}
.board-labels-table {
    width: 350px !important;
}
.stButton > button {
    width: 100%;
    height: 48px;
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
.stButton > button:disabled { opacity: 0.4; cursor: not-allowed; }
.board-container [data-testid="stHorizontalBlock"] {
    display: flex !important;
    justify-content: center !important;
    gap: 0 !important;
    margin: 0.5rem auto 0 auto !important;
    width: 350px !important;
    max-width: 350px !important;
}
.board-container [data-testid="column"] {
    padding-left: 0 !important;
    padding-right: 0 !important;
    margin: 0 !important;
    width: 50px !important;
    flex: 0 0 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
}
.board-container [data-testid="column"] .stButton {
    width: 100% !important;
}
.board-container [data-testid="column"] .stButton > button {
    width: 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
    padding: 0.4rem 0.2rem;
    font-size: 0.95rem;
    box-sizing: border-box !important;
}
.info-card {
    background: #fff;
    padding: 1.25rem;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    border-top: 4px solid #764ba2;
}
.info-card h4 { margin-top: 0; color: #44337a; }
.info-card ul { padding-left: 1.1rem; }
.info-card li { margin-bottom: 0.4rem; }
.info-card span { color: #4a5568; }
@media (max-width: 768px) {
    .game-header h1 { font-size: 1.5rem; }
}
</style>
"""

INFO_CARD_HTML = """
<div class="info-card">
    <h4>How to Play</h4>
    <ul>
        <li>Drop discs to connect four in a row.</li>
        <li>Use the drop buttons to pick a column.</li>
        <li>Yellow AI responds instantly using depth-3 Minimax.</li>
        <li>The match ends when someone connects four or the grid fills up.</li>
    </ul>
    <span>Tip: claim the center column to create multiple threats.</span>
</div>
"""

GAME_HEADER_HTML = """
<div class="game-header">
    <h1>🎮 Connect Four</h1>
    <p>Challenge the Minimax AI • First to connect 4 wins!</p>
</div>
"""


def init_game_state() -> None:
    """Initialize the game state in Streamlit session state."""
    if "board" not in st.session_state:
        st.session_state.board = create_board()
        st.session_state.turn = HUMAN
        st.session_state.game_over = False
        st.session_state.message = INITIAL_MESSAGE
        st.session_state.last_ai_column = None


def reset_game_state() -> None:
    """Reset the game to initial state."""
    st.session_state.board = create_board()
    st.session_state.turn = HUMAN
    st.session_state.game_over = False
    st.session_state.message = NEW_GAME_MESSAGE
    st.session_state.last_ai_column = None


def set_game_over_message(message: str) -> None:
    """Set game over state and message."""
    st.session_state.game_over = True
    st.session_state.message = message


def human_move(column: int) -> bool:
    """
    Process a human player's move.
    
    Args:
        column: Column index (0-6) where the player wants to drop a piece.
        
    Returns:
        True if the move was successful, False otherwise.
    """
    if st.session_state.game_over or st.session_state.turn != HUMAN:
        return False

    board = st.session_state.board
    st.session_state.last_ai_column = None

    if not is_valid_location(board, column):
        st.session_state.message = INVALID_MOVE_MESSAGE
        return False

    row = get_next_open_row(board, column)
    if row is None:
        st.session_state.message = COLUMN_FULL_MESSAGE
        return False

    drop_piece(board, row, column, HUMAN)

    if winning_move(board, HUMAN):
        set_game_over_message(HUMAN_WIN_MESSAGE)
        return True

    if board_full(board):
        set_game_over_message(DRAW_MESSAGE)
        return True

    st.session_state.turn = AI
    return True


def ai_move() -> None:
    """Process the AI's move using Minimax algorithm."""
    if st.session_state.game_over or st.session_state.turn != AI:
        return

    board = st.session_state.board
    column = ai_decide_move(board, depth=3)
    row = get_next_open_row(board, column)
    
    if row is None:
        valid = get_valid_locations(board)
        if not valid:
            set_game_over_message(DRAW_MESSAGE)
            return
        column = random.choice(valid)
        row = get_next_open_row(board, column)

    drop_piece(board, row, column, AI)
    st.session_state.last_ai_column = column + 1

    if winning_move(board, AI):
        set_game_over_message(AI_WIN_MESSAGE)
        return

    if board_full(board):
        set_game_over_message(DRAW_MESSAGE)
        return

    st.session_state.turn = HUMAN
    st.session_state.message = (
        f"<h3>🤖 Computer played column {st.session_state.last_ai_column}</h3>"
        "<p>👤 Your turn! Pick your next column.</p>"
    )


def render_status(status_placeholder) -> None:
    """Render the game status message."""
    status_placeholder.markdown(
        f'<div class="status-box">{st.session_state.message}</div>',
        unsafe_allow_html=True,
    )


def render_board(board_placeholder) -> None:
    """Render the game board."""
    board_placeholder.markdown(
        f'<div class="board-wrapper"><div class="board-container">{board_to_html(st.session_state.board)}</div></div>',
        unsafe_allow_html=True,
    )


def render_buttons(board_container) -> None:
    """Render the column selection buttons."""
    with board_container:
        cols = len(st.session_state.board[0])
        button_cols = st.columns(cols, gap="small")
        
        for idx, column in enumerate(button_cols):
            disabled = (
                st.session_state.game_over
                or st.session_state.turn != HUMAN
                or not is_valid_location(st.session_state.board, idx)
            )
            button_text = str(idx) if not disabled else "—"
            
            if column.button(button_text, key=f"col_{idx}", disabled=disabled):
                moved = human_move(idx)
                if moved and not st.session_state.game_over:
                    ai_move()
                st.rerun()


def render_game_header() -> None:
    """Render the game header."""
    st.markdown(GAME_HEADER_HTML, unsafe_allow_html=True)


def render_info_card(info_col) -> None:
    """Render the game instructions card."""
    with info_col:
        st.markdown(INFO_CARD_HTML, unsafe_allow_html=True)


def render_new_game_button(status_col) -> None:
    """Render the new game button."""
    with status_col:
        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        if st.button("🔄 New Game", use_container_width=True):
            reset_game_state()
            st.rerun()


def main() -> None:
    """Main application entry point."""
    st.set_page_config(
        page_title="Connect Four AI",
        page_icon="🎮",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    render_game_header()
    init_game_state()

    # Create layout columns
    status_col, board_col, info_col = st.columns([1.15, 2.2, 1.15], gap="large")

    # Create placeholders for dynamic content
    status_placeholder = status_col.empty()
    board_container = board_col.container()
    board_placeholder = board_container.empty()

    # Render UI components
    render_status(status_placeholder)
    render_board(board_placeholder)
    render_new_game_button(status_col)
    render_info_card(info_col)
    render_buttons(board_container)


if __name__ == "__main__":
    main()
