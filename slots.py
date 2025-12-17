import streamlit as st
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Smooth Slots",
    page_icon="🎰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. GAME SETTINGS ---
SYMBOLS = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍇"]
PAYOUTS = {"🍒": 5, "🍋": 5, "🍇": 10, "🔔": 10, "7️⃣": 20, "💎": 50}

# --- 3. STATE ---
if 'balance' not in st.session_state: st.session_state.balance = 200
if 'reels' not in st.session_state: st.session_state.reels = ["7️⃣", "7️⃣", "7️⃣"]
if 'msg' not in st.session_state: st.session_state.msg = "READY TO PLAY"
if 'msg_color' not in st.session_state: st.session_state.msg_color = "#f1c40f" # Gold

# --- 4. CSS (LOCKED LAYOUT) ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }

    /* --- THE CONTAINER (LOCKED HEIGHT) --- */
    /* This is the key. We force height to 300px so it NEVER grows/shrinks */
    .machine-box {
        background: #222;
        border: 4px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        height: 320px; /* FIXED HEIGHT TO STOP SHAKING */
        display: flex;
        flex-direction: column;
        justify-content: space-between; /* Space out elements evenly */
        align-items: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    /* STATUS TEXT */
    .status-msg {
        font-family: sans-serif;
        font-size: 24px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-top: 10px;
        height: 40px; /* Fixed height for text area */
        width: 100%;
    }

    /* REELS ROW */
    .reel-row {
        display: flex;
        justify-content: center;
        gap: 15px;
        width: 100%;
    }

    /* REEL BOXES */
    .reel {
        background: #fff;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
        border-radius: 10px;
        border: 2px solid #555;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
    }

    /* --- THE BUTTON (FORCED WIDE) --- */
    /* We target every possible button container to force width */
    div.stButton {
        width: 100%;
    }
    div.stButton > button {
        width: 100% !important; /* Force width */
        height: 100px !important; /* Force height */
        font-size: 30px !important;
        font-weight: 900 !important;
        background: linear-gradient(to bottom, #e74c3c, #c0392b) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0px 8px 0px #922b21 !important;
        transition: transform 0.1s;
    }
    div.stButton > button:active {
        transform: translateY(5px);
        box-shadow: 0px 0px 0px #922b21 !important;
    }
    
    /* Balance Badge */
    .balance {
        text-align: center;
        font-family: monospace;
        color: #2ecc71;
        font-size: 20px;
        background: #333;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #555;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI COMPONENTS ---

st.markdown("<h2 style='text-align: center; color: #d4af37; margin-bottom:0;'>🎰 CASINO PRO</h2>", unsafe_allow_html=True)

# Balance
st.markdown(f"<div class='balance'>WALLET: ${st.session_state.balance}</div>", unsafe_allow_html=True)

# Bet Slider
bet = st.select_slider("Wager:", options=[10, 20, 50, 100], value=10)

# SLOT MACHINE DISPLAY
# We use a single placeholder to render the entire machine at once.
machine_placeholder = st.empty()

def render(r1, r2, r3, msg, color):
    # This HTML structure is rigid. It uses flexbox to keep everything perfectly centered.
    html = f"""
    <div class="machine-box">
        <div class="status-msg" style="color: {color};">{msg}</div>
        <div class="reel-row">
            <div class="reel">{r1}</div>
            <div class="reel">{r2}</div>
            <div class="reel">{r3}</div>
        </div>
        <div style="height:10px;"></div> 
    </div>
    """
    machine_placeholder.markdown(html, unsafe_allow_html=True)

# Initial Draw
render(st.session_state.reels[0], st.session_state.reels[1], st.session_state.reels[2], st.session_state.msg, st.session_state.msg_color)

# --- 6. GAME LOGIC ---

# The Button
if st.button(f"SPIN (${bet})"):
    if st.session_state.balance < bet:
        st.session_state.msg = "INSUFFICIENT FUNDS"
        st.session_state.msg_color = "#e74c3c" # Red
        render(*st.session_state.reels, "INSUFFICIENT FUNDS", "#e74c3c")
    else:
        # Deduct
        st.session_state.balance -= bet
        
        # --- SMOOTH ANIMATION ---
        # We DO NOT change the text during spin. This stops the shaking.
        for _ in range(12):
            r1 = random.choice(SYMBOLS)
            r2 = random.choice(SYMBOLS)
            r3 = random.choice(SYMBOLS)
            render(r1, r2, r3, "SPINNING...", "#fff") # Text stays static white
            time.sleep(0.06)

        # --- RESULT ---
        final_reels = [random.choice(SYMBOLS) for _ in range(3)]
        st.session_state.reels = final_reels
        
        # Win Check
        if final_reels[0] == final_reels[1] == final_reels[2]:
            symbol = final_reels[0]
            win = bet * PAYOUTS[symbol]
            st.session_state.balance += win
            st.session_state.msg = f"WIN! +${win}"
            st.session_state.msg_color = "#2ecc71" # Green
            st.balloons()
        else:
            st.session_state.msg = "YOU LOST"
            st.session_state.msg_color = "#e74c3c" # Red

        # Rerun to update balance
        st.rerun()
