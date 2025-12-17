import streamlit as st
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Meme Slots Deluxe",
    page_icon="🎰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. GAME ASSETS & PAYOUTS ---
# Dictionary: Symbol -> Multiplier (How much you win)
PAYOUTS = {
    "🍒": 5,   # Weak win (5x bet)
    "🍋": 5,
    "🍇": 10,  # Medium win (10x bet)
    "🔔": 10,
    "7️⃣": 20,  # Big win (20x bet)
    "💎": 50   # JACKPOT (50x bet)
}
SYMBOLS = list(PAYOUTS.keys())

# Meme URLs (Direct image links)
WIN_IMG = "https://i.imgflip.com/1ur9b0.jpg"   # Success Kid
LOSE_IMG = "https://i.imgflip.com/26am.jpg"    # Crying Jordan or similar
JACKPOT_IMG = "https://i.imgflip.com/1h7in3.jpg" # Leo Toast

# Trash Talk & Hype Lines
QUIPS_SPIN = [
    "Let's gooooo!", 
    "Daddy needs a new pair of GPUs!", 
    "Manifesting a win...", 
    "Spinning for glory!",
    "Do it for the vine!"
]
QUIPS_LOSE = [
    "Oof. That hurt.", 
    "Rigged? Maybe.", 
    "My grandmother spins better.", 
    "Insert coin to cry.",
    "Skill issue.",
    "Emotional Damage."
]

# --- 3. STATE MANAGEMENT ---
# Initialize session state variables if they don't exist
if 'balance' not in st.session_state:
    st.session_state.balance = 200 # Starting Bankroll
if 'reels' not in st.session_state:
    st.session_state.reels = ["7️⃣", "7️⃣", "7️⃣"]
if 'game_state' not in st.session_state:
    st.session_state.game_state = "READY"
if 'message' not in st.session_state:
    st.session_state.message = "Pick your bet and spin!"
if 'last_win' not in st.session_state:
    st.session_state.last_win = 0

# --- 4. CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    
    /* MACHINE CONTAINER */
    .machine-container {
        background: linear-gradient(145deg, #2b2b2b, #1e1e1e);
        border: 4px solid #d4af37; /* Gold Border */
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
        margin-bottom: 20px;
        text-align: center;
    }

    /* REELS */
    .reel-container {
        display: flex; justify-content: center; gap: 15px;
        background-color: #000; padding: 15px; border-radius: 10px; border: 2px inset #555;
    }
    .reel-box {
        background-color: #fff; 
        width: 80px; height: 80px;
        display: flex; align-items: center; justify-content: center;
        font-size: 50px; border-radius: 8px; color: black;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }

    /* SPIN BUTTON */
    div.stButton > button {
        width: 100%; height: 80px; font-size: 24px; font-weight: 900;
        text-transform: uppercase; color: white; border: none; border-radius: 15px;
        background: radial-gradient(circle, #ff4b1f 0%, #ff9068 100%);
        box-shadow: 0px 6px 0px #b83b3e, 0px 10px 20px rgba(0,0,0,0.4);
        transition: all 0.1s;
    }
    div.stButton > button:active {
        transform: translateY(4px); box-shadow: 0px 2px 0px #b83b3e;
    }
    
    /* RESTART BUTTON (Blue) */
    .reset-btn > button {
        background: radial-gradient(circle, #3498db 0%, #2980b9 100%);
        box-shadow: 0px 6px 0px #1f618d;
    }

    /* INFO TEXT */
    .status-text { font-size: 20px; font-weight: bold; color: #f1c40f; margin-bottom: 10px; min-height: 30px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---

st.markdown("<h1 style='text-align: center; color: #d4af37; text-shadow: 2px 2px #000;'>🎰 MEME SLOTS DELUXE 🎰</h1>", unsafe_allow_html=True)

# Scoreboard
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"<div style='background:#333; padding:10px; border-radius:10px; text-align:center; color:#2ecc71; border:1px solid #d4af37;'><b>🏦 BANK: ${st.session_state.balance}</b></div>", unsafe_allow_html=True)
with c2:
    if st.session_state.last_win > 0:
        st.markdown(f"<div style='background:#333; padding:10px; border-radius:10px; text-align:center; color:#f1c40f; border:1px solid #d4af37;'><b>🏆 WON: +${st.session_state.last_win}</b></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#333; padding:10px; border-radius:10px; text-align:center; color:#777; border:1px solid #555;'>WON: $0</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Bet Selector
bet_amount = st.select_slider("Select Bet Amount:", options=[10, 20, 50, 100], value=10)

# REEL DISPLAY FUNCTION
slot_placeholder = st.empty()

def render_machine(r1, r2, r3, msg):
    html_code = f"""
    <div class="machine-container">
        <div class="status-text">{msg}</div>
        <div class="reel-container">
            <div class="reel-box">{r1}</div>
            <div class="reel-box">{r2}</div>
            <div class="reel-box">{r3}</div>
        </div>
    </div>
    """
    slot_placeholder.markdown(html_code, unsafe_allow_html=True)

# Initial Render
render_machine(st.session_state.reels[0], st.session_state.reels[1], st.session_state.reels[2], st.session_state.message)

# --- 6. GAME LOGIC ---

# Check if player is broke (less than min bet)
if st.session_state.balance < 10:
    st.error("💸 YOU ARE BROKE!")
    st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
    if st.button("🔄 RESTART GAME (Beg for money)"):
        st.session_state.balance = 200
        st.session_state.game_state = "READY"
        st.session_state.message = "Here's $200. Don't lose it all."
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # SPIN BUTTON
    if st.button(f"🔴 SPIN (${bet_amount})"):
        if st.session_state.balance < bet_amount:
            st.session_state.message = "⚠️ You can't afford that bet!"
            render_machine(*st.session_state.reels, st.session_state.message)
        else:
            # 1. Deduct Cost & Reset
            st.session_state.balance -= bet_amount
            st.session_state.last_win = 0
            
            # 2. Animation Effect
            hype_msg = random.choice(QUIPS_SPIN)
            for _ in range(15): # Spin 15 times quickly
                r1 = random.choice(SYMBOLS)
                r2 = random.choice(SYMBOLS)
                r3 = random.choice(SYMBOLS)
                render_machine(r1, r2, r3, hype_msg)
                time.sleep(0.05) # Speed of animation

            # 3. Determine Final Result
            final_reels = [random.choice(SYMBOLS) for _ in range(3)]
            st.session_state.reels = final_reels

            # 4. Check for Win (All 3 must match)
            if final_reels[0] == final_reels[1] == final_reels[2]:
                symbol = final_reels[0]
                multiplier = PAYOUTS[symbol]
                winnings = bet_amount * multiplier
                
                st.session_state.balance += winnings
                st.session_state.last_win = winnings
                
                if symbol == "💎":
                    st.session_state.game_state = "JACKPOT"
                    st.session_state.message = f"💎 JACKPOT!!! +${winnings}"
                else:
                    st.session_state.game_state = "WIN"
                    st.session_state.message = f"WINNER! ({symbol}) +${winnings}"
            else:
                st.session_state.game_state = "LOSE"
                st.session_state.message = random.choice(QUIPS_LOSE)

            st.rerun()

# --- 7. MEME REACTION AREA ---
st.markdown("---")
if st.session_state.game_state == "JACKPOT":
    st.balloons()
    st.image(JACKPOT_IMG, caption="RETIREMENT SECURED!", use_container_width=True)

elif st.session_state.game_state == "WIN":
    st.snow() # Little confetti
    st.image(WIN_IMG, caption="Profit!", use_container_width=True)

elif st.session_state.game_state == "LOSE":
    st.image(LOSE_IMG, caption="Better luck next time...", use_container_width=True)

# --- 8. RULES LEGEND ---
with st.expander("ℹ️ Payout Rules"):
    st.markdown("""
    * 💎 **Diamond:** 50x (Jackpot)
    * 7️⃣ **Seven:** 20x
    * 🍇 **Grapes/Bell:** 10x
    * 🍒 **Cherry/Lemon:** 5x
    """)
