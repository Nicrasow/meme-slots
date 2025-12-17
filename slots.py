import streamlit as st
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Pro Slots",
    page_icon="🎰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. GAME SETTINGS ---
# Symbol Payout Multipliers
PAYOUTS = {
    "🍒": 5, 
    "🍋": 5, 
    "🍇": 10, 
    "🔔": 10, 
    "7️⃣": 20, 
    "💎": 50
}
SYMBOLS = list(PAYOUTS.keys())

# Funny Text Commentary
QUIPS_SPIN = ["Rolling...", "Big Money...", "No Whammies...", "Good Vibes...", "Let's Go!"]
QUIPS_LOSE = ["Oof.", "Try again.", "So close!", "Ripped off.", "House wins."]
QUIPS_WIN = ["NICE!", "Cha-Ching!", "Easy Money!", "Pure Skill!", "JACKPOT?"]

# --- 3. STATE MANAGEMENT ---
if 'balance' not in st.session_state:
    st.session_state.balance = 200
if 'reels' not in st.session_state:
    st.session_state.reels = ["7️⃣", "7️⃣", "7️⃣"]
if 'message' not in st.session_state:
    st.session_state.message = "Place your bet & Spin!"
if 'last_win' not in st.session_state:
    st.session_state.last_win = 0

# --- 4. CSS STYLING (THE SMOOTH LOOK) ---
st.markdown("""
    <style>
    /* Main Dark Background */
    .stApp {
        background-color: #121212;
        color: white;
    }

    /* THE MACHINE FRAME */
    .machine-container {
        background: linear-gradient(180deg, #333, #1a1a1a);
        border: 4px solid #d4af37; /* Gold Border */
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7);
        text-align: center;
        margin-bottom: 25px;
    }

    /* STATUS TEXT AREA (Fixed height to prevent jumping) */
    .status-text {
        font-family: sans-serif;
        font-size: 18px;
        font-weight: bold;
        color: #f1c40f;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
        min-height: 25px; 
    }

    /* REEL CONTAINER */
    .reel-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        background-color: #000;
        padding: 12px;
        border-radius: 10px;
        border: 2px inset #555;
    }

    /* INDIVIDUAL REELS */
    .reel-box {
        background-color: #f0f0f0;
        width: 33%;
        aspect-ratio: 1/1; /* Perfect Square */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        border-radius: 8px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
        color: black;
        cursor: default;
    }

    /* WIDE 3D BUTTON */
    div.stButton > button {
        width: 100% !important;
        height: 85px;
        font-size: 26px;
        font-weight: 800;
        text-transform: uppercase;
        color: white;
        background: linear-gradient(to bottom, #ff512f, #dd2476);
        border: none;
        border-radius: 12px;
        box-shadow: 0px 6px 0px #9e1a4d, 0px 10px 20px rgba(0,0,0,0.3);
        transition: all 0.1s;
    }
    
    /* Button Press Animation */
    div.stButton > button:active {
        transform: translateY(6px);
        box-shadow: 0px 0px 0px #9e1a4d, inset 0px 5px 10px rgba(0,0,0,0.2);
    }
    
    /* BALANCE BADGE */
    .balance-badge {
        font-family: monospace;
        background-color: #222;
        color: #2ecc71;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #444;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---

# Title
st.markdown("<h2 style='text-align: center; color: #d4af37;'>🎰 ROYAL SLOTS</h2>", unsafe_allow_html=True)

# Balance Display
st.markdown(f"<div class='balance-badge'>CREDITS: ${st.session_state.balance}</div>", unsafe_allow_html=True)

# Bet Slider
bet_amount = st.select_slider("Select Bet:", options=[10, 20, 50, 100], value=10)

# SLOT MACHINE PLACEHOLDER
slot_placeholder = st.empty()

def render_machine(r1, r2, r3, msg):
    html = f"""
    <div class="machine-container">
        <div class="status-text">{msg}</div>
        <div class="reel-container">
            <div class="reel-box">{r1}</div>
            <div class="reel-box">{r2}</div>
            <div class="reel-box">{r3}</div>
        </div>
    </div>
    """
    slot_placeholder.markdown(html, unsafe_allow_html=True)

# Initial Render
render_machine(st.session_state.reels[0], st.session_state.reels[1], st.session_state.reels[2], st.session_state.message)

# --- 6. GAME LOGIC ---

if st.button(f"SPIN (${bet_amount})"):
    if st.session_state.balance < bet_amount:
        st.session_state.message = "🚫 INSUFFICIENT FUNDS"
        render_machine(*st.session_state.reels, st.session_state.message)
    else:
        # 1. Deduct Bet
        st.session_state.balance -= bet_amount
        st.session_state.last_win = 0
        
        # 2. Spin Animation (Loop)
        # We render random symbols rapidly to simulate spinning
        for _ in range(12):
            r1 = random.choice(SYMBOLS)
            r2 = random.choice(SYMBOLS)
            r3 = random.choice(SYMBOLS)
            render_machine(r1, r2, r3, random.choice(QUIPS_SPIN))
            time.sleep(0.08) # Speed of spin

        # 3. Calculate Final Result
        final_reels = [random.choice(SYMBOLS) for _ in range(3)]
        st.session_state.reels = final_reels

        # 4. Check Win
        if final_reels[0] == final_reels[1] == final_reels[2]:
            # WIN
            symbol = final_reels[0]
            multiplier = PAYOUTS[symbol]
            winnings = bet_amount * multiplier
            
            st.session_state.balance += winnings
            st.session_state.last_win = winnings
            
            msg = f"🎉 WIN! +${winnings}"
            if symbol == "💎": msg = f"💎 JACKPOT! +${winnings}"
            
            st.session_state.message = msg
            st.balloons() # Native streamlit confetti
        else:
            # LOSE
            st.session_state.message = random.choice(QUIPS_LOSE)

        # 5. Rerun to update balance
        st.rerun()

# --- 7. PAYOUT INFO ---
with st.expander("ℹ️ View Payouts"):
    st.markdown("""
    * 💎 **Diamond:** 50x Bet
    * 7️⃣ **Seven:** 20x Bet
    * 🍇 **Grape/Bell:** 10x Bet
    * 🍒 **Cherry/Lemon:** 5x Bet
    """)
