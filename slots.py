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

WIN_IMG = "https://i.imgflip.com/1ur9b0.jpg"  
LOSE_IMG = "https://i.imgflip.com/26am.jpg"   
JACKPOT_IMG = "https://i.imgflip.com/1h7in3.jpg" # Leonardo DiCaprio Toast

# Trash Talk Lines
QUIPS_SPIN = ["Let's gooooo!", "Daddy needs a new pair of shoes!", "Rolling...", "Manifesting a win..."]
QUIPS_LOSE = ["Oof.", "Ripped off.", "My cat plays better.", "Insert coin to cry."]

# --- 3. STATE MANAGEMENT ---
if 'balance' not in st.session_state:
    st.session_state.balance = 200 # Start with more money
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
    .stApp { background-color: #1a1a1a; color: white; }

    /* MACHINE CONTAINER */
    .machine-container {
        background: linear-gradient(145deg, #2b2b2b, #1e1e1e);
        border: 4px solid #d4af37;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    /* REELS */
    .reel-container {
        display: flex; justify-content: space-between; gap: 8px;
        background-color: #000; padding: 10px; border-radius: 10px; border: 2px inset #555;
    }
    .reel-box {
        background-color: #fff; width: 32%; aspect-ratio: 1/1;
        display: flex; align-items: center; justify-content: center;
        font-size: 45px; border-radius: 5px; color: black;
    }

    /* BIG BUTTON */
    div.stButton > button {
        width: 100%; height: 90px; font-size: 28px; font-weight: 900;
        text-transform: uppercase; color: white; border: none; border-radius: 15px;
        background: radial-gradient(circle, #ff4b1f 0%, #ff9068 100%);
        box-shadow: 0px 8px 0px #b83b3e, 0px 10px 20px rgba(0,0,0,0.4);
        transition: all 0.1s;
    }
    div.stButton > button:active {
        transform: translateY(8px); box-shadow: 0px 0px 0px #b83b3e;
    }
    
    /* RESET BUTTON (Blue) */
    .reset-btn > button {
        background: radial-gradient(circle, #3498db 0%, #2980b9 100%);
        box-shadow: 0px 8px 0px #1f618d, 0px 10px 20px rgba(0,0,0,0.4);
    }
    .reset-btn > button:active {
        box-shadow: 0px 0px 0px #1f618d;
    }

    /* INFO TEXT */
    .status-text { font-size: 18px; font-weight: bold; color: #ddd; text-align: center; margin-bottom: 10px; min-height: 24px; }
    
    /* PAYOUT TABLE */
    .payout-box {
        background-color: #333; padding: 10px; border-radius: 10px;
        text-align: center; font-size: 14px; color: #aaa; margin-bottom: 15px;
        border: 1px dashed #555;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---

st.markdown("<h2 style='text-align: center; color: #d4af37;'>🎰 ULTRA SLOTS</h2>", unsafe_allow_html=True)

# Balance & Last Win
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"<div style='background:#333; padding:10px; border-radius:10px; text-align:center; color:#2ecc71; border:1px solid #d4af37;'><b>BANK: ${st.session_state.balance}</b></div>", unsafe_allow_html=True)
with c2:
    if st.session_state.last_win > 0:
        st.markdown(f"<div style='background:#333; padding:10px; border-radius:10px; text-align:center; color:#f1c40f; border:1px solid #d4af37;'><b>WON: +${st.session_state.last_win}</b></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background:#333; padding:10px; border-radius:10px; text-align:center; color:#777; border:1px solid #555;'>WON: $0</div>", unsafe_allow_html=True)

# Bet Selector
st.markdown("<br>", unsafe_allow_html=True)
bet_amount = st.select_slider("Select Bet Amount:", options=[10, 20, 50, 100], value=10)

# REEL DISPLAY
slot_placeholder = st.empty()

def render_machine(r1, r2, r3):
    html_code = f"""
    <div class="machine-container">
        <div class="status-text">{st.session_state.message}</div>
        <div class="reel-container">
            <div class="reel-box">{r1}</div>
            <div class="reel-box">{r2}</div>
            <div class="reel-box">{r3}</div>
        </div>
    </div>
    """
    slot_placeholder.markdown(html_code, unsafe_allow_html=True)

render_machine(*st.session_state.reels)

# --- 6. GAME LOGIC ---

# CHECK FOR BANKRUPTCY
if st.session_state.balance < 10:
    st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
    if st.button("🔄 RESTART GAME (You're Broke!)"):
        st.session_state.balance = 200
        st.session_state.game_state = "READY"
        st.session_state.message = "Welcome back! Good luck."
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # NORMAL SPIN BUTTON
    if st.button(f"🔴 SPIN (${bet_amount})"):
        if st.session_state.balance < bet_amount:
            st.session_state.message = "⚠️ NOT ENOUGH MONEY!"
            render_machine(*st.session_state.reels)
        else:
            # 1. Deduct Cost
            st.session_state.balance -= bet_amount
            st.session_state.message = random.choice(QUIPS_SPIN)
            st.session_state.last_win = 0 # Reset last win display
            
            # 2. SPIN ANIMATION
            for _ in range(12):
                r1 = random.choice(SYMBOLS)
                r2 = random.choice(SYMBOLS)
                r3 = random.choice(SYMBOLS)
                render_machine(r1, r2, r3)
                time.sleep(0.08)

            # 3. RESULT
            final_reels = [random.choice(SYMBOLS) for _ in range(3)]
            st.session_state.reels = final_reels

            # 4. WIN CHECK (Using Payout Table)
            # We check if all 3 match
            if final_reels[0] == final_reels[1] == final_reels[2]:
                symbol = final_reels[0]
                multiplier = PAYOUTS[symbol]
                winnings = bet_amount * multiplier
                
                st.session_state.balance += winnings
                st.session_state.last_win = winnings
                st.session_state.game_state = "WIN"
                
                # Special message for Diamond Jackpot
                if symbol == "💎":
                    st.session_state.game_state = "JACKPOT"
                    st.session_state.message = f"💎 JACKPOT!!! +${winnings}"
                else:
                    st.session_state.message = f"WINNER! ({symbol}) +${winnings}"
            else:
                st.session_state.game_state = "LOSE"
                st.session_state.message = random.choice(QUIPS_LOSE)

            st.rerun()

# --- 7. MEME AREA ---
if st.session_state.game_state == "JACKPOT":
    st.balloons()
    st.image(JACKPOT_IMG, caption="RETIREMENT FUND SECURED!", use_container_width=True)

elif st.session_state.game_state == "WIN":
    st.balloons()
    st.image(WIN_IMG, caption="Not bad...", use_container_width=True)

elif st.session_state.game_state == "LOSE":
    st.image(LOSE_IMG, caption="Emotional Damage", use_container_width=True)

# --- 8. LEGEND ---
with st.expander("ℹ️ View Payout Rules"):
    st.markdown("""
    * 💎 **Diamond:** 50x Bet (Jackpot!)
    * 7️⃣ **Seven:** 20x Bet
    * 🍇 **Grapes/Bell:** 10x Bet
    * 🍒 **Cherry/Lemon:** 5x Bet
    """)
