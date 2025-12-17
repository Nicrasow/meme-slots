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

# --- 2. ASSETS ---
PAYOUTS = {"🍒": 5, "🍋": 5, "🍇": 10, "🔔": 10, "7️⃣": 20, "💎": 50}
SYMBOLS = list(PAYOUTS.keys())

# Images
WIN_IMG = "https://i.imgflip.com/1ur9b0.jpg"  
LOSE_IMG = "https://i.imgflip.com/26am.jpg"   
JACKPOT_IMG = "https://i.imgflip.com/1h7in3.jpg"

QUIPS_SPIN = ["Let's gooooo!", "Rolling...", "Manifesting a win...", "Please work..."]
QUIPS_LOSE = ["Oof.", "Ripped off.", "Scammed.", "Insert coin to cry."]

# --- 3. STATE MANAGEMENT ---
if 'balance' not in st.session_state:
    st.session_state.balance = 200
if 'reels' not in st.session_state:
    st.session_state.reels = ["7️⃣", "7️⃣", "7️⃣"]
if 'game_state' not in st.session_state:
    st.session_state.game_state = "READY"
if 'message' not in st.session_state:
    st.session_state.message = "Pick your bet and spin!"
if 'current_img' not in st.session_state:
    st.session_state.current_img = None # Stores the meme URL to show inside frame

# --- 4. CSS ---
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
        text-align: center;
        min-height: 280px; /* Force height so it doesn't jump too much */
    }

    /* REELS */
    .reel-container {
        display: flex; justify-content: space-between; gap: 8px;
        background-color: #000; padding: 10px; border-radius: 10px; border: 2px inset #555;
        margin-bottom: 10px;
    }
    .reel-box {
        background-color: #fff; width: 32%; aspect-ratio: 1/1;
        display: flex; align-items: center; justify-content: center;
        font-size: 40px; border-radius: 5px; color: black;
    }

    /* MEME INSIDE FRAME */
    .mini-meme {
        height: 80px; /* Small height */
        border-radius: 5px;
        border: 2px solid #fff;
        margin-top: 5px;
        animation: popIn 0.3s ease;
    }
    @keyframes popIn {
        0% { transform: scale(0); }
        100% { transform: scale(1); }
    }

    /* WIDE BUTTON */
    div.stButton > button {
        width: 100% !important; /* Force Wide */
        height: 80px; 
        font-size: 24px; 
        font-weight: 900;
        text-transform: uppercase; 
        color: white; border: none; border-radius: 12px;
        background: radial-gradient(circle, #ff4b1f 0%, #ff9068 100%);
        box-shadow: 0px 8px 0px #b83b3e, 0px 10px 20px rgba(0,0,0,0.4);
        transition: all 0.1s;
    }
    div.stButton > button:active {
        transform: translateY(8px); box-shadow: 0px 0px 0px #b83b3e;
    }

    .status-text { font-size: 16px; font-weight: bold; color: #ddd; margin-bottom: 8px; min-height: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- 5. RENDER FUNCTION ---
st.markdown("<h2 style='text-align: center; color: #d4af37;'>🎰 ULTRA SLOTS</h2>", unsafe_allow_html=True)

# Balance
st.markdown(f"<div style='text-align:center; margin-bottom:15px;'><span style='background:#333; padding:8px 15px; border-radius:15px; border:1px solid #d4af37; color:#2ecc71; font-weight:bold;'>BANK: ${st.session_state.balance}</span></div>", unsafe_allow_html=True)

# Bet Slider
bet_amount = st.select_slider("Bet:", options=[10, 20, 50, 100], value=10)

slot_placeholder = st.empty()

def render_machine(r1, r2, r3, message, img_url=None):
    # If there is an image URL, we add the HTML for the image
    img_html = ""
    if img_url:
        img_html = f"<br><img src='{img_url}' class='mini-meme'>"

    html_code = f"""
    <div class="machine-container">
        <div class="status-text">{message}</div>
        <div class="reel-container">
            <div class="reel-box">{r1}</div>
            <div class="reel-box">{r2}</div>
            <div class="reel-box">{r3}</div>
        </div>
        {img_html}
    </div>
    """
    slot_placeholder.markdown(html_code, unsafe_allow_html=True)

# Initial Draw
render_machine(st.session_state.reels[0], st.session_state.reels[1], st.session_state.reels[2], st.session_state.message, st.session_state.current_img)

# --- 6. GAME LOGIC ---
if st.button(f"SPIN (${bet_amount})"):
    if st.session_state.balance < bet_amount:
        st.session_state.message = "⚠️ BROKE!"
        st.session_state.current_img = None
        render_machine(*st.session_state.reels, "⚠️ BROKE!", None)
    else:
        # Deduct
        st.session_state.balance -= bet_amount
        st.session_state.current_img = None # Clear old meme
        
        # ANIMATION
        for _ in range(12):
            r1 = random.choice(SYMBOLS)
            r2 = random.choice(SYMBOLS)
            r3 = random.choice(SYMBOLS)
            # Render spinning state (No image)
            render_machine(r1, r2, r3, random.choice(QUIPS_SPIN), None)
            time.sleep(0.08)

        # RESULTS
        final_reels = [random.choice(SYMBOLS) for _ in range(3)]
        st.session_state.reels = final_reels

        # WIN CHECK
        if final_reels[0] == final_reels[1] == final_reels[2]:
            symbol = final_reels[0]
            winnings = bet_amount * PAYOUTS[symbol]
            st.session_state.balance += winnings
            
            # Select Image
            img = JACKPOT_IMG if symbol == "💎" else WIN_IMG
            msg = f"WIN! +${winnings}"
            st.session_state.game_state = "WIN"
        else:
            img = LOSE_IMG
            msg = random.choice(QUIPS_LOSE)
            st.session_state.game_state = "LOSE"

        # Save state
        st.session_state.message = msg
        st.session_state.current_img = img
        
        # Rerun to update everything
        st.rerun()
