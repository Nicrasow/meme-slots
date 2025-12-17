import streamlit as st
import random
import time
from dataclasses import dataclass

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Text Slots: Toxic Edition",
    page_icon="💬",
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

# WEIGHTED MATH (Total ~100)
SYMBOLS = [
    Symbol("🥔", "Potato",      5,  45), # 45% chance
    Symbol("💩", "Poop",        10, 25), # 25% chance
    Symbol("🍆", "Eggplant",    20, 15), # 15% chance
    Symbol("💀", "Skull",       50, 10), # 10% chance
    Symbol("💎", "Diamond",     100, 4), # 4% chance
    Symbol("🦄", "Unicorn",     500, 1)  # 1% chance
]

# Quick Lookups
POPULATION = [s.emoji for s in SYMBOLS]
WEIGHTS = [s.weight for s in SYMBOLS]
SYMBOL_MAP = {s.emoji: s for s in SYMBOLS}

# --- THE TEXT ENGINE (Expanded Humor) ---

MSG_WELCOME = [
    "Ready to lose some money?",
    "The rent isn't going to pay itself.",
    "I hope you brought your wallet.",
    "Insert coin. Try not to cry.",
]

MSG_ROAST = [
    "Skill issue.",
    "My cat plays better than this.",
    "Have you considered a different hobby?",
    "Oof. That was embarrassing.",
    "The algorithm is laughing at you.",
    "Donate more to the house, please.",
    "Yikes.",
    "Are you even trying?",
    "Emotional Damage.",
    "Maybe try Checkers?",
    "404: Win not found.",
    "Imagine losing to a potato.",
]

MSG_NEAR_MISS = [ 
    # Triggered when 2 symbols match but 3rd misses
    "So close, yet so broke.",
    "Baited.",
    "The machine is teasing you.",
    "Almost rich. (But actually poor).",
    "Psych!",
    "It hurts, doesn't it?"
]

MSG_WIN = [
    "We take those!",
    "Finally, a W.",
    "Don't spend it all in one place.",
    "Pure skill (it was luck).",
    "Stonks 📈",
    "Winner Winner Chicken Dinner.",
    "IRS has entered the chat.",
]

MSG_JACKPOT = [
    "🦄 UNBELIEVABLE SCENES! 🦄",
    "MOM GET THE CAMERA!",
    "RETIREMENT SECURED!",
    "SYSTEM ERROR: YOU WEREN'T SUPPOSED TO WIN THIS!",
    "GOD MODE ACTIVATED."
]

# --- 3. STATE MANAGEMENT ---
if 'balance' not in st.session_state:
    st.session_state.balance = 200
if 'reels' not in st.session_state:
    st.session_state.reels = ["🥔", "🥔", "🥔"]
if 'display_msg' not in st.session_state:
    st.session_state.display_msg = random.choice(MSG_WELCOME)
if 'msg_color' not in st.session_state:
    st.session_state.msg_color = "#ffffff" # Default white

# --- 4. CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #111; color: #fff; }
    
    /* CONSOLE BOX */
    .console-box {
        background-color: #000;
        border: 2px solid #333;
        border-radius: 10px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        text-align: center;
        margin-bottom: 20px;
        min-height: 80px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
    }
    
    /* REELS */
    .reel-container {
        display: flex; justify-content: center; gap: 15px; margin-bottom: 30px;
    }
    .reel-box {
        width: 100px; height: 100px;
        background: linear-gradient(145deg, #222, #111);
        border: 2px solid #555;
        border-radius: 15px;
        font-size: 60px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    
    /* BUTTONS */
    div.stButton > button {
        width: 100%; height: 70px; font-size: 24px; font-weight: bold;
        background: #333; color: white; border: 1px solid #555;
        border-radius: 8px; transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #444; border-color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI COMPONENTS ---

st.markdown("<h1 style='text-align: center; font-family: monospace; color: #00ff00;'>&gt; TERMINAL_SLOTS_v3.exe</h1>", unsafe_allow_html=True)

# 1. Stats Bar
c1, c2 = st.columns(2)
with c1:
    st.metric("CREDITS", f"${st.session_state.balance}")
with c2:
    bet = st.select_slider("WAGER", options=[10, 50, 100, 200, "ALL"], value=10)
    if bet == "ALL":
        bet = st.session_state.balance

# 2. The Machine (Reels)
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

# 3. The Commentary Console (Replaces Images)
msg_placeholder = st.empty()

def render_console(text, color):
    html = f"""
    <div class="console-box" style="border-color: {color}; color: {color};">
        &gt; {text}_
    </div>
    """
    msg_placeholder.markdown(html, unsafe_allow_html=True)

render_console(st.session_state.display_msg, st.session_state.msg_color)

# --- 6. GAME LOGIC ---

st.markdown("---")

# BANKRUPTCY CHECK
if st.session_state.balance <= 0:
    render_console("CRITICAL FAILURE: WALLET EMPTY.", "#ff0000")
    if st.button("REBOOT SYSTEM (Beg for $50)"):
        st.session_state.balance = 50
        st.session_state.display_msg = "System Rebooted. Try again."
        st.session_state.msg_color = "#00ff00"
        st.rerun()
else:
    # SPIN BUTTON
    if st.button("EXECUTE SPIN"):
        
        # Validate Bet
        current_bet = bet
        if current_bet > st.session_state.balance:
            st.session_state.display_msg = "ERROR: INSUFFICIENT FUNDS."
            st.session_state.msg_color = "#ff0000"
            st.rerun()

        # Deduct Money
        st.session_state.balance -= current_bet
        
        # Animation
        spin_phrases = ["Accessing Mainframe...", "Crunching Numbers...", "RNG goes brrr...", "Downloading RAM..."]
        chosen_spin_phrase = random.choice(spin_phrases)
        
        for _ in range(8):
            temp = [random.choice(POPULATION) for _ in range(3)]
            render_machine(*temp)
            render_console(chosen_spin_phrase, "#ffff00")
            time.sleep(0.08)

        # Generate Result
        final_reels = random.choices(POPULATION, weights=WEIGHTS, k=3)
        st.session_state.reels = final_reels
        
        # --- WIN/LOSS LOGIC ---
        r1, r2, r3 = final_reels
        
        # 1. JACKPOT (3 Match)
        if r1 == r2 == r3:
            symbol = SYMBOL_MAP[r1]
            win_amount = current_bet * symbol.payout
            st.session_state.balance += win_amount
            
            # Special Jackpot Message
            if symbol.name == "Unicorn" or symbol.name == "Diamond":
                st.session_state.display_msg = random.choice(MSG_JACKPOT) + f" (+${win_amount})"
                st.session_state.msg_color = "#00ffff" # Cyan
                st.balloons()
            else:
                st.session_state.display_msg = f"{random.choice(MSG_WIN)} (Matched {symbol.name}: +${win_amount})"
                st.session_state.msg_color = "#00ff00" # Green
                st.snow()

        # 2. NEAR MISS (2 Match)
        elif r1 == r2 or r2 == r3 or r1 == r3:
            st.session_state.display_msg = random.choice(MSG_NEAR_MISS)
            st.session_state.msg_color = "#ffaa00" # Orange

        # 3. TOTAL LOSS
        else:
            st.session_state.display_msg = random.choice(MSG_ROAST)
            st.session_state.msg_color = "#ff0000" # Red

        st.rerun()

# --- LEGEND ---
with st.expander("VIEW SOURCE_CODE (Payouts)"):
    st.code("""
    if match == 🦄: return 500x  // 1% Chance
    if match == 💎: return 100x  // 4% Chance
    if match == 💀: return 50x   // 10% Chance
    if match == 🍆: return 20x   // 15% Chance
    if match == 💩: return 10x   // 25% Chance
    if match == 🥔: return 5x    // 45% Chance
    else: return EMOTIONAL_DAMAGE
    """, language="python")
