import streamlit as st
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Meme Slots Mobile",
    page_icon="🎰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. GAME ASSETS ---
# We use emoji symbols for the reels
SYMBOLS = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍇"]
WIN_IMG = "https://i.imgflip.com/1ur9b0.jpg"  # Distracted Boyfriend
LOSE_IMG = "https://i.imgflip.com/26am.jpg"   # This is Fine dog

# Trash Talk Lines
QUIPS_SPIN = ["Let's gooooo!", "Big money, no whammies!", "Rolling...", "Manifesting a win..."]
QUIPS_WIN = ["EZ MONEY!", "Dinner is on you!", "Pure skill!", "Hacker!"]
QUIPS_LOSE = ["Oof.", "Ripped off.", "My cat plays better.", "Insert coin to cry."]

# --- 3. STATE MANAGEMENT ---
if 'balance' not in st.session_state:
    st.session_state.balance = 100
if 'reels' not in st.session_state:
    st.session_state.reels = ["7️⃣", "7️⃣", "7️⃣"]
if 'game_state' not in st.session_state:
    st.session_state.game_state = "READY"
if 'message' not in st.session_state:
    st.session_state.message = "Press the big red button!"

# --- 4. ADVANCED CSS (THE VISUALS) ---
st.markdown("""
    <style>
    /* Dark Casino Background */
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }

    /* THE SLOT MACHINE FRAME */
    .machine-container {
        background: linear-gradient(145deg, #2b2b2b, #1e1e1e);
        border: 4px solid #d4af37; /* Gold Trim */
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
        text-align: center;
    }

    /* REEL STYLING */
    .reel-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        background-color: #000;
        padding: 15px;
        border-radius: 10px;
        border: 2px inset #555;
    }
    
    .reel-box {
        background-color: #fff;
        width: 30%;
        aspect-ratio: 1/1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
        border-radius: 5px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
        color: black;
    }

    /* BLUR EFFECT FOR SPINNING */
    .blur-spin {
        filter: blur(4px);
        transform: scale(0.9);
        transition: all 0.1s;
    }

    /* 3D ARCADE BUTTON */
    div.stButton > button {
        width: 100%;
        height: 80px;
        font-size: 24px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        background: radial-gradient(circle, #ff5e62 0%, #ff9966 100%);
        border: none;
        border-radius: 50px; /* Pill shape */
        box-shadow: 0px 10px 0px #b83b3e, 0px 10px 20px rgba(0,0,0,0.4); /* 3D Depth */
        transition: all 0.1s;
        margin-top: 20px;
    }

    /* BUTTON PRESS EFFECT */
    div.stButton > button:active {
        transform: translateY(10px); /* Moves down */
        box-shadow: 0px 0px 0px #b83b3e, inset 0px 5px 10px rgba(0,0,0,0.2); /* Shadow disappears */
    }

    /* MEME IMAGE SIZING */
    .meme-img {
        max-height: 150px; /* Small fixed height */
        width: auto;
        border-radius: 10px;
        border: 3px solid #fff;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    
    .status-text {
        font-size: 18px; 
        font-weight: bold; 
        color: #ddd; 
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. INTERFACE LAYOUT ---

# Header
st.markdown("<h2 style='text-align: center; color: #d4af37; text-shadow: 2px 2px #000;'>🎰 POCKET SLOTS</h2>", unsafe_allow_html=True)

# Balance Badge
st.markdown(
    f"<div style='text-align: center; margin-bottom: 10px;'>"
    f"<span style='background: #333; padding: 8px 15px; border-radius: 15px; border: 1px solid #d4af37; color: #2ecc71; font-weight: bold; font-family: monospace; font-size: 1.2rem;'>"
    f"BANK: ${st.session_state.balance}"
    f"</span></div>", 
    unsafe_allow_html=True
)

# THE SLOT MACHINE (Container)
slot_placeholder = st.empty()

# Helper to render the machine HTML
def render_machine(r1, r2, r3, is_spinning=False):
    # If spinning, we add a CSS class to blur the text
    blur_class = "blur-spin" if is_spinning else ""
    
    html_code = f"""
    <div class="machine-container">
        <div class="status-text">{st.session_state.message}</div>
        <div class="reel-container">
            <div class="reel-box {blur_class}">{r1}</div>
            <div class="reel-box {blur_class}">{r2}</div>
            <div class="reel-box {blur_class}">{r3}</div>
        </div>
    </div>
    """
    slot_placeholder.markdown(html_code, unsafe_allow_html=True)

# Initial Render
render_machine(st.session_state.reels[0], st.session_state.reels[1], st.session_state.reels[2])

# THE MEME AREA (Keeps space even if empty so layout doesn't jump)
meme_placeholder = st.empty()

# --- 6. GAME LOGIC ---
if st.button("🔴 SPIN ($10)"):
    if st.session_state.balance < 10:
        st.session_state.message = "🚫 YOU ARE BROKE!"
        render_machine(*st.session_state.reels)
    else:
        # 1. Deduct Cost
        st.session_state.balance -= 10
        st.session_state.message = random.choice(QUIPS_SPIN)
        
        # 2. SPIN ANIMATION (With Blur)
        # We loop 12 times. On each loop, we update the HTML with the "blur-spin" class
        for _ in range(12):
            r1 = random.choice(SYMBOLS)
            r2 = random.choice(SYMBOLS)
            r3 = random.choice(SYMBOLS)
            render_machine(r1, r2, r3, is_spinning=True)
            time.sleep(0.08) # Fast speed

        # 3. CALCULATE RESULT
        final_reels = [random.choice(SYMBOLS) for _ in range(3)]
        st.session_state.reels = final_reels

        # 4. WIN CHECK
        if final_reels[0] == final_reels[1] == final_reels[2]:
            st.session_state.balance += 100
            st.session_state.game_state = "WIN"
            st.session_state.message = random.choice(QUIPS_WIN)
        else:
            st.session_state.game_state = "LOSE"
            st.session_state.message = random.choice(QUIPS_LOSE)

        # 5. RERUN TO UPDATE UI PERMANENTLY
        st.rerun()

# --- 7. RENDER PERSISTENT MEME ---
# This runs after the rerun to ensure the meme stays on screen
if st.session_state.game_state == "WIN":
    st.balloons()
    meme_placeholder.markdown(f"<img src='{WIN_IMG}' class='meme-img'>", unsafe_allow_html=True)
elif st.session_state.game_state == "LOSE":
    meme_placeholder.markdown(f"<img src='{LOSE_IMG}' class='meme-img'>", unsafe_allow_html=True)
