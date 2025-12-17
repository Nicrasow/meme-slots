import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Meme Slots Ultimate",
    page_icon="🎰",
    layout="centered"
)

# --- CSS STYLING (To make it look like a game) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .reel-box {
        border: 2px solid #f1c40f;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #2c3e50;
        font-size: 60px;
    }
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 24px;
        background-color: #e74c3c;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
    }
    div.stButton > button:hover {
        background-color: #c0392b;
        border: 2px solid white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE BALANCE ---
if 'balance' not in st.session_state:
    st.session_state.balance = 100

# --- ASSETS ---
symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍇"]

# Using public URLs for memes so they work instantly
win_img = "https://i.imgflip.com/1ur9b0.jpg"  # Distracted Boyfriend
lose_img = "https://i.imgflip.com/26am.jpg"   # This is Fine dog

# --- TITLE & BALANCE ---
st.title("💸 MEME CASINO 💸")

col_bal, col_status = st.columns([1, 2])
with col_bal:
    st.metric("Your Money", f"${st.session_state.balance}")

# --- THE SLOT MACHINE DISPLAY ---
# We create empty placeholders first so we can update them during animation
c1, c2, c3 = st.columns(3)
with c1:
    slot1 = st.empty()
with c2:
    slot2 = st.empty()
with c3:
    slot3 = st.empty()

# Function to render a single slot box
def draw_slot(placeholder, symbol):
    placeholder.markdown(f"<div class='reel-box'>{symbol}</div>", unsafe_allow_html=True)

# Draw initial state (Question marks)
draw_slot(slot1, "❓")
draw_slot(slot2, "❓")
draw_slot(slot3, "❓")

# --- MESSAGE AREA ---
result_area = st.empty()

# --- SPIN LOGIC ---
if st.button("SPIN! ($10)"):
    if st.session_state.balance < 10:
        result_area.error("🚫 BROKE! You have no money left. Refresh page to reset.")
    else:
        # 1. Deduct Money
        st.session_state.balance -= 10
        
        # 2. THE ANIMATION LOOP
        # This loop runs 15 times rapidly to simulate spinning
        for i in range(15):
            # Pick random symbols just for the visual effect
            s1 = random.choice(symbols)
            s2 = random.choice(symbols)
            s3 = random.choice(symbols)
            
            draw_slot(slot1, s1)
            draw_slot(slot2, s2)
            draw_slot(slot3, s3)
            
            # Pause briefly to create the "flicker" effect
            time.sleep(0.1)

        # 3. GENERATE FINAL RESULT
        final_1 = random.choice(symbols)
        final_2 = random.choice(symbols)
        final_3 = random.choice(symbols)
        
        # Show final symbols
        draw_slot(slot1, final_1)
        draw_slot(slot2, final_2)
        draw_slot(slot3, final_3)

        # 4. CHECK WIN/LOSS
        if final_1 == final_2 == final_3:
            # WIN
            winnings = 100
            st.session_state.balance += winnings
            result_area.success(f"🎉 JACKPOT! You won ${winnings}!")
            st.balloons()
            st.image(win_img, caption="EZ MONEY!")
        else:
            # LOSS
            result_area.error("📉 YOU LOST!")
            st.image(lose_img, caption="Emotional Damage")
        
        # We perform a tiny sleep so the user sees the image, 
        # then we force a rerun to update the 'Your Money' metric at the top
        time.sleep(1)
        st.rerun()
