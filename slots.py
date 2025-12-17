import streamlit as st
import random
import time

# --- 1. MOBILE CONFIGURATION ---
st.set_page_config(
    page_title="Meme Slots Mobile",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. TRASH TALK ENGINE (Funny Comments) ---
SPIN_QUIPS = [
    "🤞 Praying to the RNG gods...",
    "🧠 Calculating success (0%)...",
    "💸 Goodbye, $10...",
    "👀 Mom! Get the camera!",
    "🎢 Here we go again...",
    "🔨 Smashing that spin button..."
]

WIN_QUIPS = [
    "🚀 TO THE MOON!",
    "🤯 HAX! I'm calling the police.",
    "🍟 Dinner is on you tonight!",
    "🕶️ Pure skill. Definitely not luck.",
    "🏦 The IRS would like to know your location."
]

LOSE_QUIPS = [
    "📉 Emotional Damage.",
    "🤡 You played yourself.",
    "🚮 Have you tried winning instead?",
    "💀 My grandma spins better than this.",
    "📉 Stonks only go down apparently."
]

# --- 3. SESSION STATE SETUP ---
if 'balance' not in st.session_state:
    st.session_state.balance = 100
if 'reels' not in st.session_state:
    st.session_state.reels = ["❓", "❓", "❓"]
if 'game_state' not in st.session_state:
    st.session_state.game_state = "READY" 
if 'commentary' not in st.session_state:
    st.session_state.commentary = "Welcome to the Mobile Casino! 👇"

# --- 4. RESPONSIVE MOBILE CSS ---
st.markdown("""
    <style>
    /* Dark Mode Background */
    .stApp {
        background-color: #121212;
        color: white;
    }
    
    /* The Slot Display - Flexbox for Mobile scaling */
    .slot-row {
        display: flex;
        justify_content: space-between;
        margin-bottom: 15px;
    }
    
    /* Individual Reel Card */
    .reel-card {
        background-color: #2c2c2c;
        border: 2px solid #f1c40f;
        border-radius: 10px;
        width: 30%; /* Fits 3 in a row comfortably on phone */
        aspect-ratio: 1/1; /* Keeps it square */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem; /* Responsive font size */
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Big Tappable Spin Button for Thumbs */
    div.stButton > button {
        width: 100%;
        padding-top: 20px;
        padding-bottom: 20px;
        font-size: 24px;
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        box-shadow: 0px 5px 15px rgba(221, 36, 118, 0.4);
        transition: transform 0.1s;
    }
    div.stButton > button:active {
        transform: scale(0.95);
    }

    /* Commentary Box */
    .comment-box {
        text-align: center;
        font-style: italic;
        color: #aaa;
        margin-bottom: 10px;
        min-height: 1.5em;
    }

    /* Balance Badge */
    .balance-badge {
        background-color: #333;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        color: #2ecc71;
        text-align: center;
        border: 1px solid #444;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. GAME LOGIC ---
symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍇"]
win_img = "https://i.imgflip.com/1ur9b0.jpg"
lose_img = "https://i.imgflip.com/26am.jpg"

# Header
st.markdown("<h2 style='text-align: center;'>🎰 POCKET SLOTS</h2>", unsafe_allow_html=True)

# Balance
st.markdown(f"<div class='balance-badge'>CREDITS: ${st.session_state.balance}</div>", unsafe_allow_html=True)

# Commentary
st.markdown(f"<div class='comment-box'>\"{st.session_state.commentary}\"</div>", unsafe_allow_html=True)

# REELS DISPLAY (Using HTML for perfect mobile layout)
# We use st.empty() to allow animation updates
reels_placeholder = st.empty()

def render_reels(r1, r2, r3):
    html = f"""
    <div class="slot-row">
        <div class="reel-card">{r1}</div>
        <div class="reel-card">{r2}</div>
        <div class="reel-card">{r3}</div>
    </div>
    """
    reels_placeholder.markdown(html, unsafe_allow_html=True)

# Render current state
render_reels(st.session_state.reels[0], st.session_state.reels[1], st.session_state.reels[2])

# SPIN BUTTON
if st.button("SPIN ($10)"):
    if st.session_state.balance < 10:
        st.error("🚫 BROKE ALERT! Refresh to reset.")
    else:
        # 1. Start Spin: Deduct money & update comment
        st.session_state.balance -= 10
        st.session_state.game_state = "SPINNING"
        
        # Show a random "Spinning" quip immediately
        rand_quip = random.choice(SPIN_QUIPS)
        st.markdown(f"<div class='comment-box'>\"{rand_quip}\"</div>", unsafe_allow_html=True)
        
        # 2. Animation Loop (Flicker effect)
        for _ in range(10):
            r1 = random.choice(symbols)
            r2 = random.choice(symbols)
            r3 = random.choice(symbols)
            render_reels(r1, r2, r3)
            time.sleep(0.1)

        # 3. Final Result
        final_reels = [random.choice(symbols) for _ in range(3)]
        st.session_state.reels = final_reels

        # 4. Win/Lose Logic
        if final_reels[0] == final_reels[1] == final_reels[2]:
            st.session_state.balance += 100
            st.session_state.game_state = "WIN"
            st.session_state.commentary = random.choice(WIN_QUIPS)
        else:
            st.session_state.game_state = "LOSE"
            st.session_state.commentary = random.choice(LOSE_QUIPS)
        
        # 5. Rerun to update the Balance badge and show the meme
        st.rerun()

# --- 6. RESULTS & MEMES (Persistent) ---
# This code runs after the rerun, keeping the meme on screen
if st.session_state.game_state == "WIN":
    st.success("JACKPOT! +$100")
    st.balloons()
    st.image(win_img, use_container_width=True) # use_container_width is best for mobile
    
elif st.session_state.game_state == "LOSE":
    st.error("You lost $10")
    st.image(lose_img, use_container_width=True)
