import streamlit as st
import random
import time
from dataclasses import dataclass

# --- 1. ARCHITECTURE & CONFIGURATION ---
st.set_page_config(
    page_title="Vegas Pro Slots",
    page_icon="🎰",
    layout="wide",  # distinct wide layout for a "cabinet" feel
    initial_sidebar_state="expanded"
)

# Define a Data Class for our Symbols (Best Practice for structured data)
@dataclass
class Symbol:
    emoji: str
    name: str
    payout: int
    weight: int  # Higher number = more likely to appear

# CONFIGURATION: The "Math" behind the machine
# Weights total to 100 for easy probability calculation
SYMBOLS = [
    Symbol("🍒", "Cherry",  3,  40), # 40% chance
    Symbol("🍋", "Lemon",   5,  30), # 30% chance
    Symbol("🍇", "Grape",   10, 15), # 15% chance
    Symbol("🔔", "Bell",    20, 10), # 10% chance
    Symbol("💎", "Diamond", 50, 4),  # 4% chance
    Symbol("🃏", "Joker",   100, 1)  # 1% chance (ULTRA RARE)
]

# Separate lists for logic processing
SYMBOL_OBJECTS = {s.emoji: s for s in SYMBOLS}
POPULATION = [s.emoji for s in SYMBOLS]
WEIGHTS = [s.weight for s in SYMBOLS]

# --- 2. STATE MANAGEMENT ---
def init_state():
    """Initialize all session state variables in one place."""
    if 'balance' not in st.session_state:
        st.session_state.balance = 500
    if 'reels' not in st.session_state:
        st.session_state.reels = ["🍒", "🍒", "🍒"]
    if 'history' not in st.session_state:
        st.session_state.history = [] # List to store string logs
    if 'msg_type' not in st.session_state:
        st.session_state.msg_type = "info" # info, success, error, warning
    if 'message' not in st.session_state:
        st.session_state.message = "Welcome to Vegas Pro! Good Luck."

init_state()

# --- 3. HELPER FUNCTIONS ---
def spin_logic():
    """
    Selects 3 symbols based on their probability weights.
    Returns: List of 3 emojis
    """
    return random.choices(POPULATION, weights=WEIGHTS, k=3)

def check_win(reels, bet):
    """
    Analyzes the reels and calculates payout.
    Returns: (winnings, message, type)
    """
    # 1. Jackpot: All 3 match
    if reels[0] == reels[1] == reels[2]:
        symbol_data = SYMBOL_OBJECTS[reels[0]]
        win = bet * symbol_data.payout
        
        if symbol_data.name == "Joker":
            return win, f"🃏 ULTIMATE JACKPOT! {symbol_data.payout}x!", "balloons"
        elif symbol_data.name == "Diamond":
            return win, f"💎 MEGA WIN! {symbol_data.payout}x!", "balloons"
        else:
            return win, f"✨ NICE! Triple {symbol_data.name}! (+${win})", "success"
    
    # 2. Mini Win: 2 match (Optional rule to make it friendlier)
    # Checks: A==B or B==C or A==C
    elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
        # Find the matching symbol
        if reels[0] == reels[1]: match = reels[0]
        elif reels[1] == reels[2]: match = reels[1]
        else: match = reels[0]
        
        symbol_data = SYMBOL_OBJECTS[match]
        # Half payout for 2 matches
        mini_win = int(bet * (symbol_data.payout / 2)) 
        if mini_win < 1: mini_win = 1 # Minimum win 1
        return mini_win, f"🤏 Mini Win: Double {symbol_data.name} (+${mini_win})", "success"

    # 3. Loss
    else:
        loss_msgs = ["Whiff.", "The machine is cold.", "Ouch.", "Spin again!", "So close..."]
        return 0, random.choice(loss_msgs), "error"

# --- 4. ADVANCED CSS STYLING ---
st.markdown("""
    <style>
    /* Dark Casino Theme */
    .stApp { background-color: #0e0e0e; }
    
    /* The Cabinet Frame */
    .cabinet {
        background: linear-gradient(180deg, #444, #222);
        border: 8px solid #c0a062;
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 0 50px rgba(0,0,0,0.9), inset 0 0 20px #000;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* The Screen inside the Cabinet */
    .screen {
        background-color: #000;
        border: 4px solid #111;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: inset 0 0 20px #000;
    }

    /* Reel Styling */
    .reel {
        font-size: 80px;
        background: linear-gradient(0deg, #f0f0f0 0%, #fff 50%, #d9d9d9 100%);
        width: 100%;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #555;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
        text-shadow: 2px 2px 0px rgba(0,0,0,0.2);
    }

    /* Stats Box */
    .stat-box {
        background: #222;
        border: 1px solid #444;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        color: #fff;
        font-family: monospace;
    }
    .stat-value { font-size: 24px; color: #c0a062; font-weight: bold; }
    
    /* Custom Button */
    div.stButton > button {
        background: linear-gradient(180deg, #ff0000, #cc0000);
        color: white; border: none; padding: 15px 30px;
        font-size: 24px; font-weight: bold; text-transform: uppercase;
        width: 100%; border-radius: 10px;
        box-shadow: 0 5px 0 #990000;
    }
    div.stButton > button:active {
        transform: translateY(4px); box-shadow: 0 1px 0 #990000;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---

# Sidebar: History & Rules
with st.sidebar:
    st.markdown("## 📜 Spin History")
    # Show last 10 spins, reversed
    for entry in reversed(st.session_state.history[-10:]):
        st.text(entry)
    
    st.markdown("---")
    st.markdown("## ℹ️ Pay Table")
    for s in SYMBOLS:
        st.markdown(f"**{s.emoji} {s.name}**: {s.payout}x")
    st.markdown("*Double Match = Half Payout*")

# Main Area
st.markdown("<div class='cabinet'>", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center; color:#c0a062; margin-top:0;'>🎰 VEGAS PRO 🎰</h1>", unsafe_allow_html=True)

# Stats Row
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='stat-box'>BALANCE<div class='stat-value'>${st.session_state.balance}</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='stat-box'>LAST BET<div class='stat-value'>${st.session_state.history[-1].split('|')[1].strip() if st.session_state.history else 0}</div></div>", unsafe_allow_html=True)
with c3:
    # Bet Selection
    bet = st.select_slider("WAGER", options=[10, 20, 50, 100, 200, 500], value=20, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# THE REELS (Using Streamlit Columns for responsive layout)
# We use a container to hold the reels
reel_placeholder = st.empty()

# Function to draw the reels
def draw_reels(r1, r2, r3, msg_text, msg_color="#fff"):
    with reel_placeholder.container():
        st.markdown("<div class='screen'>", unsafe_allow_html=True)
        # Message Bar
        st.markdown(f"<h3 style='text-align:center; color:{msg_color}; margin:0 0 20px 0;'>{msg_text}</h3>", unsafe_allow_html=True)
        
        # Reels
        rc1, rc2, rc3 = st.columns(3)
        with rc1: st.markdown(f"<div class='reel'>{r1}</div>", unsafe_allow_html=True)
        with rc2: st.markdown(f"<div class='reel'>{r2}</div>", unsafe_allow_html=True)
        with rc3: st.markdown(f"<div class='reel'>{r3}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Draw initial state
draw_reels(*st.session_state.reels, st.session_state.message)

st.markdown("</div>", unsafe_allow_html=True) # End Cabinet

# --- 6. GAME CONTROL ---
st.markdown("<br>", unsafe_allow_html=True)

# Centered Button
_, col_btn, _ = st.columns([1, 2, 1])

with col_btn:
    # Check bankruptcy
    if st.session_state.balance < 10:
        st.error("📉 YOU ARE BANKRUPT!")
        if st.button("🔄 REFILL WALLET"):
            st.session_state.balance = 500
            st.session_state.history.append("🔄 Refilled Wallet")
            st.rerun()
    else:
        spin_btn = st.button("SPIN REELS 🎲")

        if spin_btn:
            if st.session_state.balance >= bet:
                # 1. Pay Logic
                st.session_state.balance -= bet
                
                # 2. Animation Loop (Visual Only)
                for _ in range(10):
                    temp_reels = [random.choice(POPULATION) for _ in range(3)]
                    draw_reels(*temp_reels, "Spinning...", "#aaa")
                    time.sleep(0.05)
                
                # 3. Determine Result (Weighted)
                result_reels = spin_logic()
                st.session_state.reels = result_reels
                
                # 4. Calculate Winnings
                winnings, msg, effect = check_win(result_reels, bet)
                
                # 5. Update State
                st.session_state.balance += winnings
                st.session_state.message = msg
                
                # 6. Update History
                hist_symbol = "✅" if winnings > 0 else "❌"
                st.session_state.history.append(f"{hist_symbol} | {bet} | {' '.join(result_reels)} | {winnings:+}")
                
                # 7. Final Render & Effects
                color = "#4caf50" if winnings > 0 else "#f44336"
                draw_reels(*result_reels, msg, color)
                
                if effect == "balloons":
                    st.balloons()
                elif effect == "success":
                    st.snow()
                
                st.rerun() # Force update to refresh balance immediately
            else:
                st.warning("Not enough funds!")
