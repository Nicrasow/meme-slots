import streamlit as st
import random
import time
from dataclasses import dataclass

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="CYBER SLOTS_v4",
    page_icon="💾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. THE MATH (WEIGHTED) ---
@dataclass
class Symbol:
    emoji: str
    name: str
    payout: int
    weight: int

# Probability: High weight = Common, Low weight = Rare
SYMBOLS = [
    Symbol("🥔", "POTATO",    5,   45), # Trash
    Symbol("💿", "DISK",      10,  25), # Common
    Symbol("💾", "FLOPPY",    20,  15), # Uncommon
    Symbol("🔋", "ENERGY",    50,  10), # Rare
    Symbol("💎", "DIAMOND",   100, 4),  # Very Rare
    Symbol("👽", "ALIEN",     500, 1)   # Jackpot
]

POPULATION = [s.emoji for s in SYMBOLS]
WEIGHTS = [s.weight for s in SYMBOLS]
SYMBOL_MAP = {s.emoji: s for s in SYMBOLS}

# --- 3. THE "TRASH TALK" ENGINE ---
LOG_WELCOME = [
    "SYSTEM READY. INSERT CREDITS.",
    "AWAITING INPUT...",
    "DON'T BLAME THE ALGORITHM.",
    "HIGH RISK // HIGH REWARD"
]
LOG_SPIN = [
    "ACCESSING MAINFRAME...", 
    "RNG CYCLES: OPTIMIZED", 
    "DECRYPTING LUCK...", 
    "OVERCLOCKING..."
]
LOG_LOSE = [
    "ERROR 404: WIN NOT FOUND",
    "SKILL_LEVEL: LOW",
    "WALLET INTEGRITY: CRITICAL",
    "TRY INSTALLING 'WIN.EXE'",
    "MISSION FAILED.",
    "SYSTEM LAUGHING AT USER."
]
LOG_NEAR = [
    "WARNING: NEAR MISS DETECTED",
    "SIGNAL INTERRUPTED...",
    "SO CLOSE IT HURTS.",
    "GLITCH IN THE MATRIX."
]
LOG_WIN = [
    "SUCCESS! FUNDS ACQUIRED.",
    "OPTIMAL OUTCOME.",
    "PROTOCOL: CELEBRATE",
    "PROFIT MARGIN: INCREASED"
]

# --- 4. STATE ---
if 'balance' not in st.session_state: st.session_state.balance = 200
if 'reels' not in st.session_state: st.session_state.reels = ["🥔", "🥔", "🥔"]
if 'log_txt' not in st.session_state: st.session_state.log_txt = random.choice(LOG_WELCOME)
if 'log_color' not in st.session_state: st.session_state.log_color = "#00ff00" # Neon Green

# --- 5. ADVANCED CSS (THE "LOOK") ---
st.markdown("""
    <style>
    /* MAIN THEME: Cyberpunk Terminal */
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }

    /* THE TERMINAL SCREEN (Log Box) */
    .terminal-box {
        border: 2px solid #00ff00;
        background-color: #001100;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        text-align: center;
        margin-bottom: 20px;
        min-height: 60px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        text-shadow: 0 0 5px #00ff00;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* THE REEL CONTAINER */
    .machine-frame {
        background: #111;
        border: 4px solid #333;
        border-radius: 15px;
        padding: 20px;
        box-shadow: inset 0 0 30px #000;
        margin-bottom: 20px;
    }

    .reel-container {
        display: flex; justify-content: space-between; gap: 10px;
    }

    /* INDIVIDUAL REELS */
    .reel {
        width: 32%;
        aspect-ratio: 1/1;
        background-color: #000;
        border: 2px solid #444;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 60px;
        box-shadow: 0 0 10px rgba(0,0,0,0.8);
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }

    /* THE BIG 'EXECUTE' BUTTON */
    div.stButton > button {
        width: 100%;
        height: 100px;
        font-family: 'Courier New', monospace;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 2px;
        background-color: #000;
        color: #00ff00;
        border: 2px solid #00ff00;
        border-radius: 5px;
        box-shadow: 0 0 10px #00ff00;
        transition: all 0.2s ease-in-out;
        text-transform: uppercase;
    }
    
    div.stButton > button:hover {
        background-color: #00ff00;
        color: #000;
        box-shadow: 0 0 30px #00ff00;
        transform: scale(1.02);
    }
    
    div.stButton > button:active {
        transform: scale(0.98);
        box-shadow: 0 0 5px #00ff00;
    }

    /* REMOVE DEFAULT STREAMLIT PADDING */
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }
    </style>
""", unsafe_allow_html=True)

# --- 6. UI CONSTRUCTION ---

st.markdown("<h2 style='text-align:center; color:#00ff00; text-shadow: 0 0 10px #00ff00;'>&gt; CYBER_SLOTS_v4</h2>", unsafe_allow_html=True)

# 1. STATUS BAR
c1, c2 = st.columns([1, 1])
with c1:
    st.markdown(f"<div style='border:1px solid #444; padding:10px; text-align:center; color:#00ff00;'>CREDITS: {st.session_state.balance}</div>", unsafe_allow_html=True)
with c2:
    # Custom stylized selector
    bet = st.select_slider("WAGER_AMOUNT", options=[10, 50, 100, "ALL"], value=10, label_visibility="collapsed")
    if bet == "ALL": bet = st.session_state.balance

st.write("") # Spacer

# 2. THE SCREEN (Reels)
screen_placeholder = st.empty()

def render_screen(r1, r2, r3):
    html = f"""
    <div class="machine-frame">
        <div class="reel-container">
            <div class="reel">{r1}</div>
            <div class="reel">{r2}</div>
            <div class="reel">{r3}</div>
        </div>
    </div>
    """
    screen_placeholder.markdown(html, unsafe_allow_html=True)

render_screen(*st.session_state.reels)

# 3. THE TERMINAL LOG (Feedback)
log_placeholder = st.empty()

def render_log(text, color):
    html = f"""
    <div class="terminal-box" style="border-color: {color}; color: {color}; text-shadow: 0 0 5px {color};">
        &gt; {text}_
    </div>
    """
    log_placeholder.markdown(html, unsafe_allow_html=True)

render_log(st.session_state.log_txt, st.session_state.log_color)

# --- 7. GAME LOOP ---

if st.session_state.balance <= 0:
    render_log("CRITICAL ERROR: INSUFFICIENT FUNDS.", "#ff0000")
    if st.button(">> REBOOT_SYSTEM (BEG FOR $50) <<"):
        st.session_state.balance = 50
        st.session_state.log_txt = "SYSTEM REBOOT SUCCESSFUL."
        st.session_state.log_color = "#00ff00"
        st.rerun()
else:
    # THE BIG BUTTON
    if st.button(">> EXECUTE_SPIN <<"):
        
        # Check Funds
        if bet > st.session_state.balance:
            st.session_state.log_txt = "ERROR: FUNDS LOW. LOWER BET."
            st.session_state.log_color = "#ff0000"
            st.rerun()

        # Deduct
        st.session_state.balance -= bet
        
        # --- THE PHYSICS ANIMATION ---
        # 20 Frames. Starts fast (0.05s) -> Slows to (0.2s)
        spin_msg = random.choice(LOG_SPIN)
        
        for i in range(20):
            # 1. Randomize Reels
            temp = [random.choice(POPULATION) for _ in range(3)]
            render_screen(*temp)
            render_log(spin_msg, "#ffff00") # Yellow during spin
            
            # 2. Calculate Decay (Braking effect)
            # Logic: sleep time increases as 'i' gets bigger
            decay = 0.05 + (i * 0.008) 
            time.sleep(decay)

        # --- FINAL CALCULATION ---
        final = random.choices(POPULATION, weights=WEIGHTS, k=3)
        st.session_state.reels = final
        r1, r2, r3 = final
        
        # WIN CHECK
        if r1 == r2 == r3:
            s = SYMBOL_MAP[r1]
            win = bet * s.payout
            st.session_state.balance += win
            
            # Color logic
            if s.name == "ALIEN":
                msg = f"👽 ALIEN CONTACT CONFIRMED (+{win})"
                color = "#00ffff" # Cyan
                st.balloons()
            elif s.name == "DIAMOND":
                msg = f"💎 MAX VALUE EXTRACTED (+{win})"
                color = "#00ffff"
                st.balloons()
            else:
                msg = f"{random.choice(LOG_WIN)} (+{win})"
                color = "#00ff00" # Green
                st.snow()
                
        elif r1 == r2 or r2 == r3 or r1 == r3:
            msg = random.choice(LOG_NEAR)
            color = "#ffa500" # Orange
            
        else:
            msg = random.choice(LOG_LOSE)
            color = "#ff0000" # Red
            
        # Update State & UI
        st.session_state.log_txt = msg
        st.session_state.log_color = color
        st.rerun()

# --- 8. FOOTER / PAYOUTS ---
with st.expander(">> ACCESS_DATABASE (PAYOUTS)"):
    st.markdown("""
    | SYMBOL | CODE | PAYOUT | ODDS |
    | :---: | :--- | :--- | :--- |
    | 👽 | ALIEN | 500x | 1% |
    | 💎 | DIAMOND | 100x | 4% |
    | 🔋 | ENERGY | 50x | 10% |
    | 💾 | FLOPPY | 20x | 15% |
    | 💿 | DISK | 10x | 25% |
    | 🥔 | POTATO | 5x | 45% |
    """)
