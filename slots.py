import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Meme Slots 🎰",
    page_icon="🍒",
    layout="centered"
)

# --- CUSTOM CSS (To make it look like a casino) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .css-10trblm {
        color: #f1c40f;
    }
    .stButton>button {
        color: white;
        background-color: #e74c3c;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE (To remember balance between spins) ---
if 'balance' not in st.session_state:
    st.session_state.balance = 100

# --- GAME ASSETS ---
symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍇"]
# NOTE: To host online easily, we will use URL images instead of local files
# You can replace these URLs with links to your own memes
win_image_url = "https://i.imgflip.com/1ur9b0.jpg"  # Example: Distracted Boyfriend
lose_image_url = "https://i.imgflip.com/26am.jpg"   # Example: This is Fine dog

# --- THE APP UI ---
st.title("💸 MEME CASINO WEB 💸")
st.write("Current Balance")
st.metric(label="", value=f"${st.session_state.balance}")

# --- SPIN LOGIC ---
if st.button("SPIN ($10) 🎰"):
    if st.session_state.balance < 10:
        st.error("You are broke! Refresh the page to reset.")
    else:
        # Deduct money
        st.session_state.balance -= 10
        
        # Spin animation (simulated)
        slots = st.columns(3)
        with st.spinner("Spinning..."):
            time.sleep(1) # Fake delay for suspense
            
        # Generate results
        results = [random.choice(symbols) for _ in range(3)]
        
        # Show results big
        for i, symbol in enumerate(results):
            with slots[i]:
                st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{symbol}</h1>", unsafe_allow_html=True)

        # Win/Loss Check
        if results[0] == results[1] == results[2]:
            winnings = 100
            st.session_state.balance += winnings
            st.success(f"JACKPOT! You won ${winnings}!")
            st.balloons()
            st.image(win_image_url, caption="STONKS 📈")
        else:
            st.warning("You lost...")
            if random.random() < 0.3:
                st.image(lose_image_url, caption="NOT STONKS 📉")
            
            # Force a rerun to update the balance metric at the top immediately
            st.rerun()