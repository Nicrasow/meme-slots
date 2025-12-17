import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Meme Slots Pro",
    page_icon="🎰",
    layout="centered"
)

# --- 1. SESSION STATE SETUP (The Game's Memory) ---
# This ensures the game remembers the reels and memes even after the page updates
if 'balance' not in st.session_state:
    st.session_state.balance = 100
if 'reels' not in st.session_state:
    st.session_state.reels = ["❓", "❓", "❓"]
if 'game_state' not in st.session_state:
    st.session_state.game_state = "READY" # Options: READY, WIN, LOSE
if 'last_msg' not in st.session_state:
    st.session_state.last_msg = "Press SPIN to start!"

# --- 2. CUSTOM CSS (The "Better Interface") ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* The Slot Machine Display Box */
    .slot-container {
        background-color: #000000;
        border: 4px solid #d4af37; /* Gold Border */
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.5);
    }
    
    /* The Individual Reels */
    .reel-box {
        background-color: #333333;
        border: 2px solid #555;
        border-radius: 10px;
        color: white;
        font-size: 80px;
        text-align: center;
        padding: 10px;
        height: 140px;
        line-height: 120px;
    }
    
    /* Spin Button Styling */
    div.stButton > button {
        width: 100%;
        height: 70px;
        background: linear-gradient(to bottom, #ff4b1f, #ff9068);
        color: white;
        font-size: 28px;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        box-shadow: 0px 5px 0px #b03010;
        transition: all 0.1s;
    }
    div.stButton > button:active {
        box-shadow: 0px 2px 0px #b03010;
        transform: translateY(3px);
    }
    
    /* Balance Display */
    .balance-box {
        font-family: 'Courier New', monospace;
        background-color: #222;
        color: #0f0;
        padding: 10px;
        border: 1px solid #444;
        border-radius: 5px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ASSETS ---
symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍇"]
win_img = "https://i.imgflip.com/1ur9b0.jpg"  # Distracted Boyfriend
lose_img = "https://i.imgflip.com/26am.jpg"   # This is Fine dog

# --- 4. HEADER & BALANCE ---
st.markdown("<h1 style='text-align: center; color: #d4af37;'>🎰 MEME CASINO PRO 🎰</h1>", unsafe_allow_html=True)

# Display Balance
st.markdown(f"<div class='balance-box'>WALLET: ${st.session_state.balance}</div>", unsafe_allow_html=True)

# --- 5. THE SLOT MACHINE UI ---
# We use a container to group the reels visually
with st.container():
    st.markdown("<div class='slot-container'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    # We create placeholders. These are what we update during animation.
    with c1:
        reel1 = st.empty()
    with c2:
        reel2 = st.empty()
    with c3:
        reel3 = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

# Helper function to draw the reels
def update_reels(r1_symbol, r2_symbol, r3_symbol):
    reel1.markdown(f"<div class='reel-box'>{r1_symbol}</div>", unsafe_allow_html=True)
    reel2.markdown(f"<div class='reel-box'>{r2_symbol}</div>", unsafe_allow_html=True)
    reel3.markdown(f"<div class='reel-box'>{r3_symbol}</div>", unsafe_allow_html=True)

# Draw the current state (this keeps the symbols on screen between clicks)
update_reels(st.session_state.reels[0], st.session_state.reels[1], st.session_state.reels[2])

# --- 6. CONTROLS & LOGIC ---
if st.button("SPIN! ($10)"):
    if st.session_state.balance < 10:
        st.error("🚫 You are bankrupt! Refresh the page to reset.")
    else:
        # Clear previous result message/meme immediately
        st.session_state.game_state = "SPINNING"
        
        # ANIMATION LOOP
        # This runs "live" before we calculate the final result
        for i in range(12):
            s1 = random.choice(symbols)
            s2 = random.choice(symbols)
            s3 = random.choice(symbols)
            update_reels(s1, s2, s3)
            time.sleep(0.1) # Speed of spin
        
        # CALCULATE FINAL RESULT
        final_reels = [random.choice(symbols) for _ in range(3)]
        
        # SAVE TO MEMORY (State)
        st.session_state.reels = final_reels
        st.session_state.balance -= 10
        
        # DETERMINE WIN/LOSS
        if final_reels[0] == final_reels[1] == final_reels[2]:
            st.session_state.balance += 100
            st.session_state.game_state = "WIN"
            st.session_state.last_msg = "JACKPOT! +$100"
        else:
            st.session_state.game_state = "LOSE"
            st.session_state.last_msg = "YOU LOST $10"
            
        # RERUN to update the Balance at the top and show the meme below
        st.rerun()

# --- 7. RESULT DISPLAY (Stays until next spin) ---
if st.session_state.game_state == "WIN":
    st.success(st.session_state.last_msg)
    st.balloons()
    st.image(win_img, caption="STONKS 📈", use_container_width=True)

elif st.session_state.game_state == "LOSE":
    st.error(st.session_state.last_msg)
    st.image(lose_img, caption="NOT STONKS 📉", use_container_width=True)

elif st.session_state.game_state == "READY":
    st.info("Good Luck! Spin to win.")
