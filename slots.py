import streamlit as st
import random
import time
from dataclasses import dataclass

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Pocket Slots Deluxe",
    page_icon="🤡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DATA & ASSETS ---
@dataclass
class Symbol:
    emoji: str
    name: str
    payout: int
    weight: int

# The Funny/Rude Symbols
SYMBOLS = [
    Symbol("🥔", "Potato",      5,   45),
    Symbol("💩", "Poop",        10,  25),
    Symbol("🍆", "Eggplant",    20,  15),
    Symbol("🤡", "Clown",       50,  10),
    Symbol("💎", "Diamond",     100, 4),
    Symbol("🦄", "Unicorn",     500, 1)
]

POPULATION = [s.emoji for s in SYMBOLS]
WEIGHTS = [s.weight for s in SYMBOLS]
SYMBOL_MAP = {s.emoji: s for s in SYMBOLS}

# The Roasts
LOG_WELCOME = ["READY TO LOSE?", "INSERT HOPES & DREAMS", "DO NOT ADDICT.", "MOM'S CREDIT CARD READY?"]
LOG_SPIN = ["RNG GOING BRRR...", "DRAINING WALLET...", "CALCULATING REGRET...", "LOADING DISAPPOINTMENT..."]
LOG_LOSE = ["Skill issue.", "Get wrecked.", "Imagine losing.", "My grandma spins better.", "Delete the app.", "Oof."]
LOG_NEAR = ["SO CLOSE!", "Baited.", "The pixel missed.", "Almost rich (still poor)."]
LOG_WIN = ["WE TAKE THOSE!", "Pure Skill.", "Rent is paid!", "Stonks 📈", "Finally a W."]
LOG_JACKPOT = ["🦄 UNICORN GOD 🦄", "I AM SCREAMING", "JACKPOT!!!", "QUIT YOUR JOB!"]

# --- 3. STATE ---
if 'balance' not in st.session_state: st.session_state.balance = 200
if 'reels' not in st.session_state: st.session_state.reels = ["🥔", "🥔", "🥔"]
if 'msg' not in st.session_state: st.session_state.msg = random.choice(LOG_WELCOME)
if 'msg_color' not in st.session_state: st.session_state.msg_color = "#00ff00"

# --- 4. CSS MAGIC (STICKY BUTTON) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: sans-serif; }

    /* REEL CONTAINER */
    .reel-container {
        display: flex; justify-content: center; gap: 10px; margin-top: 20px;
    }
    .reel {
        width: 30%; aspect-ratio: 1/1;
        background: #111; border: 2px solid #333; border-radius: 15px;
        font-size: 60px; display: flex; align-items: center; justify-content: center;
        box-shadow: inset 0 0 20px #000;
    }
    
    /* FEEDBACK LOG */
    .log-box {
        text-align: center; font-family: 'Courier New', monospace; font-weight: bold;
        padding: 15px; margin: 20px 0; border-radius: 8px; border: 1px dashed #444;
        font-size: 18px;
    }

    /* --- THE STICKY BUTTON HACK --- */
    /* This targets the container of the button and pins it to the bottom */
    div.stButton {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #000; /* Black background behind button to hide content */
        padding: 15px;
        z-index: 999;
        text-align: center;
        border-top: 1px solid #333;
    }

    /* STYLE THE BUTTON ITSELF */
    div.stButton > button {
        width: 100%;
        height: 80px;
        font-size: 28px !important;
        font-weight: 900;
        text-transform: uppercase;
        background: linear-gradient(45deg, #ff0055, #ff00aa);
        color: white;
        border: none;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(255, 0, 100, 0.5);
        transition: transform 0.1s;
    }
    
    div.stButton > button:active {
        transform: scale(0.95);
    }
    
    /* Add padding to bottom of page so content doesn't get hidden behind button */
    .block-container {
        padding-bottom: 150px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---

# Header
st.markdown("<h2 style='text-align:center; color:#ff00aa;'>🎰 POCKET SLOTS</h2>", unsafe_allow_html=True)

# Stats
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"<h3 style='text-align:center; color:#0f0;'>💰 ${st.session_state.balance}</h3>", unsafe_allow_html=True)
with c2:
    bet = st.select_slider("BET", options=[10, 50, 100, "ALL"], value=10, label_visibility="collapsed")
    if bet == "ALL": bet = st.session_state.balance

# Reels
reel_placeholder = st.empty()
def render_reels(r1, r2, r3):
    html = f"""
    <div class="reel-container">
        <div class="reel">{r1}</div>
        <div class="reel">{r2}</div>
        <div class="reel">{r3}</div>
    </div>
    """
    reel_placeholder.markdown(html, unsafe_allow_html=True)

render_reels(*st.session_state.reels)

# Message Log
msg_placeholder = st.empty()
def render_msg(text, color):
    html = f"<div class='log-box' style='color:{color}; border-color:{color};'>{text}</div>"
    msg_placeholder.markdown(html, unsafe_allow_html=True)

render_msg(st.session_state.msg, st.session_state.msg_color)

# Payout Table (Scrollable content)
with st.expander("Show Rules (Math)"):
    st.write("🦄 Unicorn (1%) = 500x")
    st.write("💎 Diamond (4%) = 100x")
    st.write("🤡 Clown (10%) = 50x")
    st.write("🍆 Eggplant (15%) = 20x")
    st.write("💩 Poop (25%) = 10x")
    st.write("🥔 Potato (45%) = 5x")

# --- 6. GAME LOGIC (CONNECTED TO STICKY BUTTON) ---

# Decide what the button does based on Balance
if st.session_state.balance <= 0:
    # BANKRUPT STATE
    if st.button("💸 BEG FOR MONEY 💸"):
        st.session_state.balance = 200
        st.session_state.msg = "Here's $200. Don't be stupid."
        st.session_state.msg_color = "#fff"
        st.rerun()
else:
    # PLAYING STATE
    if st.button("🔥 SPIN 🔥"):
        if bet > st.session_state.balance:
            st.session_state.msg = "YOU ARE BROKE. LOWER BET."
            st.session_state.msg_color = "red"
            st.rerun()

        # Deduct
        st.session_state.balance -= bet
        
        # Anim
        spin_txt = random.choice(LOG_SPIN)
        for i in range(20):
            render_reels(random.choice(POPULATION), random.choice(POPULATION), random.choice(POPULATION))
            render_msg(spin_txt, "#ffff00")
            time.sleep(0.05 + (i * 0.005)) # Slow down effect

        # Result
        final = random.choices(POPULATION, weights=WEIGHTS, k=3)
        st.session_state.reels = final
        r1, r2, r3 = final
        
        if r1 == r2 == r3:
            s = SYMBOL_MAP[r1]
            win = bet * s.payout
            st.session_state.balance += win
            
            if s.name in ["Unicorn", "Diamond"]:
                st.session_state.msg = random.choice(LOG_JACKPOT) + f" (+${win})"
                st.session_state.msg_color = "#00ffff"
                st.balloons()
            else:
                st.session_state.msg = random.choice(LOG_WIN) + f" (+${win})"
                st.session_state.msg_color = "#00ff00"
                st.snow()
        elif r1 == r2 or r2 == r3 or r1 == r3:
            st.session_state.msg = random.choice(LOG_NEAR)
            st.session_state.msg_color = "#ffa500"
        else:
            st.session_state.msg = random.choice(LOG_LOSE)
            st.session_state.msg_color = "#ff4444"

        st.rerun()
