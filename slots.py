import streamlit as st
import random
import time
from dataclasses import dataclass

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Pocket Slots",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ASSETS & DATA ---
@dataclass
class Symbol:
    emoji: str
    name: str
    payout: int
    weight: int

# WEIGHTED MATH (Hard Mode)
SYMBOLS = [
    Symbol("🥔", "Potato",      5,  45),
    Symbol("💩", "Poop",        10, 25),
    Symbol("🍆", "Eggplant",    20, 15),
    Symbol("💀", "Skull",       50, 10),
    Symbol("💎", "Diamond",     100, 4),
    Symbol("🦄", "Unicorn",     500, 1)
]

POPULATION = [s.emoji for s in SYMBOLS]
WEIGHTS = [s.weight for s in SYMBOLS]
SYMBOL_MAP = {s.emoji: s for s in SYMBOLS}

# --- TEXT ENGINE ---
MSG_WELCOME = ["TAP TO LOSE MONEY", "MOM'S CREDIT CARD READY?", "LET'S GO GAMBLING!"]
MSG_ROAST = ["Skill issue.", "Get rekt.", "My battery is dying watching this.", "Oof.", "Delete the app.", "Imagine losing."]
MSG_NEAR_MISS = ["SO CLOSE!", "The pixel missed.", "Baited.", "My thumb slipped.", "Almost rich."]
MSG_WIN = ["WE TAKE THOSE!", "Pure Skill.", "Rent is paid!", "Stonks 📈", "Dinner is on you."]
MSG_JACKPOT = ["🦄 UNICORN GOD 🦄", "RETIREMENT FUND!", "JACKPOT!!!"]

# --- 3. STATE ---
if 'balance' not in st.session_state: st.session_state.balance = 200
if 'reels' not in st.session_state: st.session_state.reels = ["🥔", "🥔", "🥔"]
if 'display_msg' not in st.session_state: st.session_state.display_msg = random.choice(MSG_WELCOME)
if 'msg_color' not in st.session_state: st.session_state.msg_color = "#fff"

# --- 4. MOBILE-FIRST CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #fff; }
    
    /* CONSOLE BOX (Top) */
    .console-box {
        background: #111;
        border: 2px dashed #444;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        text-align: center;
        min-height: 70px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    /* RESPONSIVE REELS CONTAINER */
    .reel-container {
        display: flex;
        justify-content: space-between; /* Spreads them out evenly */
        align-items: center;
        gap: 2%; /* Small gap between reels */
        margin-bottom: 25px;
    }
    
    /* THE REEL BOXES */
    .reel-box {
        width: 32%; /* Fits 3 perfectly on mobile */
        aspect-ratio: 1 / 1; /* Forces it to be a square */
        background: linear-gradient(145deg, #222, #0d0d0d);
        border: 2px solid #555;
        border-radius: 15px;
        display: flex; 
        align-items: center; 
        justify-content: center;
        
        /* Responsive Font Size */
        font-size: clamp(40px, 8vw, 80px); 
        box-shadow: inset 0 0 15px #000;
    }
    
    /* GIANT SPIN BUTTON */
    div.stButton > button {
        width: 100%;
        height: 110px; /* BIG TOUCH TARGET */
        font-size: 35px !important;
        font-weight: 900;
        text-transform: uppercase;
        background: radial-gradient(circle, #ff0055 0%, #990033 100%);
        color: white;
        border: 4px solid #ff99bb;
        border-radius: 20px;
        box-shadow: 0 10px 0 #660022; /* 3D effect */
        transition: transform 0.1s, box-shadow 0.1s;
        margin-top: 10px;
    }
    
    div.stButton > button:active {
        transform: translateY(6px);
        box-shadow: 0 4px 0 #660022;
    }
    
    div.stButton > button:hover {
        border-color: #fff;
    }

    /* Hide standard streamlit junk for cleaner mobile look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---

# Top Stats
c1, c2 = st.columns([1, 1])
with c1:
    st.markdown(f"<h3 style='margin:0; color:#0f0;'>💰 ${st.session_state.balance}</h3>", unsafe_allow_html=True)
with c2:
    bet_options = [10, 50, 100, "ALL"]
    bet = st.selectbox("Wager", options=bet_options, label_visibility="collapsed")
    if bet == "ALL": bet = st.session_state.balance

st.write("") # Spacer

# REELS
reel_placeholder = st.empty()

def render_machine(r1, r2, r3):
    html = f"""
    <div class="reel-container">
        <div class="reel-box">{r1}</div>
        <div class="reel-box">{r2}</div>
        <div class="reel-box">{r3}</div>
    </div>
    """
    reel_placeholder.markdown(html, unsafe_allow_html=True)

render_machine(*st.session_state.reels)

# CONSOLE
msg_placeholder = st.empty()

def render_console(text, color):
    html = f"""
    <div class="console-box" style="border-color: {color}; color: {color};">
        {text}
    </div>
    """
    msg_placeholder.markdown(html, unsafe_allow_html=True)

render_console(st.session_state.display_msg, st.session_state.msg_color)

# --- 6. GAME LOGIC ---

if st.session_state.balance <= 0:
    render_console("❌ YOU ARE BROKE ❌", "#ff0000")
    if st.button("RESET GAME (FREE MONEY)"):
        st.session_state.balance = 200
        st.session_state.display_msg = "Don't mess up this time."
        st.session_state.msg_color = "#fff"
        st.rerun()
else:
    # THE BIG BUTTON
    if st.button("SPIN"):
        
        if bet > st.session_state.balance:
            st.session_state.display_msg = "INSUFFICIENT FUNDS"
            st.session_state.msg_color = "red"
            st.rerun()

        st.session_state.balance -= bet
        
        # --- EXTENDED ANIMATION (2.5 Seconds) ---
        phrases = ["ROLLING...", "HOLD ON...", "PRAYING...", "LOADING LUCK..."]
        
        # We loop 25 times now (was 8) for a longer feel
        for i in range(25):
            temp_reels = [random.choice(POPULATION) for _ in range(3)]
            render_machine(*temp_reels)
            
            # Change text every 5 frames
            if i % 5 == 0:
                render_console(random.choice(phrases), "#ffff00")
            
            # Variable speed: Start fast (0.05), end slow (0.15)
            # This makes it feel like the mechanical wheel is stopping
            sleep_time = 0.05 + (i * 0.004) 
            time.sleep(sleep_time)

        # --- RESULT ---
        final_reels = random.choices(POPULATION, weights=WEIGHTS, k=3)
        st.session_state.reels = final_reels
        r1, r2, r3 = final_reels
        
        if r1 == r2 == r3:
            symbol = SYMBOL_MAP[r1]
            win = bet * symbol.payout
            st.session_state.balance += win
            
            if symbol.name in ["Unicorn", "Diamond"]:
                st.session_state.display_msg = random.choice(MSG_JACKPOT) + f" (+${win})"
                st.session_state.msg_color = "#00ffff" # Cyan
                st.balloons()
            else:
                st.session_state.display_msg = random.choice(MSG_WIN) + f" (+${win})"
                st.session_state.msg_color = "#00ff00" # Green
                st.snow()
        
        elif r1 == r2 or r2 == r3 or r1 == r3:
            st.session_state.display_msg = random.choice(MSG_NEAR_MISS)
            st.session_state.msg_color = "#ffaa00" # Orange
            
        else:
            st.session_state.display_msg = random.choice(MSG_ROAST)
            st.session_state.msg_color = "#ff4444" # Red

        st.rerun()
