import streamlit as st
import random
import time
from dataclasses import dataclass

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Meme Slots: HARD MODE",
    page_icon="🤡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ASSETS & DATA ---

@dataclass
class Symbol:
    emoji: str
    name: str
    payout: int
    weight: int  # Higher = Common, Lower = Rare

# THE MATH (Weighted Probabilities)
# Total weight = 100 approx
SYMBOLS = [
    Symbol("🥔", "Potato",      5,  45), # Very Common (45% chance per reel)
    Symbol("💩", "Poop Emoji",  10, 25), # Common
    Symbol("🍆", "Eggplant",    20, 15), # Uncommon
    Symbol("🚀", "Moon",        50, 10), # Rare
    Symbol("💎", "Diamond",     100, 4), # Very Rare
    Symbol("🦄", "Unicorn",     500, 1)  # 1% chance (Jackpot)
]

# Quick lookups
SYMBOL_MAP = {s.emoji: s for s in SYMBOLS}
POPULATION = [s.emoji for s in SYMBOLS]
WEIGHTS = [s.weight for s in SYMBOLS]

# MEMES
IMG_WIN = "https://i.imgflip.com/1ur9b0.jpg"       # Success Kid
IMG_JACKPOT = "https://i.imgflip.com/1h7in3.jpg"   # Leo Toast
IMG_LOSE = [
    "https://i.imgflip.com/26am.jpg",              # Crying Jordan
    "https://i.imgflip.com/39t54l.jpg",            # Harold Hide Pain
    "https://i.imgflip.com/2GNK.jpg"               # Grumpy Cat
]
IMG_BROKE = "https://i.kym-cdn.com/entries/icons/original/000/032/632/No_No_No_Not_Today_Dikembe_Mutombo_Meme_Banner.jpg" # Not today

# TRASH TALK
ROASTS = [
    "My grandma spins better than you.",
    "Is this your first time using a computer?",
    "Don't quit your day job.",
    "Oof. Even the algorithm feels bad for you.",
    "Skill issue.",
    "Have you tried winning instead?",
    "Your wallet is crying.",
    "Maybe try Checkers?"
]

# --- 3. STATE ---
if 'balance' not in st.session_state:
    st.session_state.balance = 200
if 'reels' not in st.session_state:
    st.session_state.reels = ["🥔", "🥔", "🥔"]
if 'game_state' not in st.session_state:
    st.session_state.game_state = "READY" # READY, WIN, LOSE, BROKE
if 'message' not in st.session_state:
    st.session_state.message = "Feeling lucky, punk?"
if 'current_meme' not in st.session_state:
    st.session_state.current_meme = None

# --- 4. CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    
    /* The Slot Machine Box */
    .slot-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #333 100%);
        border: 4px solid #ff00ff; /* Neon Pink */
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 0 20px #ff00ff;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Reels */
    .reel-row {
        display: flex; justify-content: center; gap: 10px; margin: 20px 0;
    }
    .reel {
        font-size: 60px;
        background: #fff;
        width: 80px; height: 80px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        border: 3px solid #000;
        box-shadow: inset 0 0 10px #000;
        text-shadow: none;
    }

    /* Message Area */
    .msg-box {
        font-size: 20px; font-weight: bold; color: #00ff00; 
        font-family: 'Courier New', monospace;
        min-height: 50px;
        display: flex; align-items: center; justify-content: center;
    }
    
    /* Custom Buttons */
    .stButton>button {
        width: 100%; font-weight: bold; font-size: 20px;
        border-radius: 10px; height: 60px;
        background: linear-gradient(90deg, #ff8a00, #e52e71);
        color: white; border: none;
    }
    .stButton>button:active { transform: scale(0.98); }
    </style>
""", unsafe_allow_html=True)

# --- 5. UI LAYOUT ---

st.markdown("<h1 style='text-align: center; color: #ff00ff;'>🎰 MEME SLOTS: HARD MODE</h1>", unsafe_allow_html=True)

# Top Bar: Money
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"<h3 style='color: #00ff00; border: 1px solid #00ff00; padding: 5px; text-align: center;'>💰 ${st.session_state.balance}</h3>", unsafe_allow_html=True)
with c2:
    # Bet Selection
    bet = st.select_slider("RISK IT ALL:", options=[10, 50, 100, "ALL IN"], value=10)
    if bet == "ALL IN":
        bet = st.session_state.balance

# THE MACHINE
slot_placeholder = st.empty()

def render_slot(r1, r2, r3, msg):
    html = f"""
    <div class="slot-box">
        <div class="reel-row">
            <div class="reel">{r1}</div>
            <div class="reel">{r2}</div>
            <div class="reel">{r3}</div>
        </div>
        <div class="msg-box">{msg}</div>
    </div>
    """
    slot_placeholder.markdown(html, unsafe_allow_html=True)

# Initial Render
render_slot(*st.session_state.reels, st.session_state.message)

# --- 6. GAME LOGIC ---

# Check Bankruptcy
if st.session_state.balance <= 0:
    st.error("📉 YOU ARE BROKE. GAME OVER.")
    st.image(IMG_BROKE, caption="Access Denied", width=300)
    
    if st.button("🥺 Beg the Developer for $50"):
        st.session_state.balance = 50
        st.session_state.game_state = "READY"
        st.session_state.message = "Don't blow it this time."
        st.rerun()

else:
    # Spin Button
    if st.button("🔥 SPIN THAT THING 🔥"):
        
        # 1. Validation
        if bet > st.session_state.balance:
            st.session_state.message = "You don't have that kind of money, chief."
            st.rerun()
            
        # 2. Pay up
        st.session_state.balance -= bet
        
        # 3. Animation
        roast = random.choice(["Spinning...", "No whammies...", "Pls win...", "Come on..."])
        for _ in range(10):
            temp = [random.choice(POPULATION) for _ in range(3)]
            render_slot(*temp, roast)
            time.sleep(0.08)

        # 4. Result (Weighted)
        # Using random.choices logic
        final_reels = random.choices(POPULATION, weights=WEIGHTS, k=3)
        st.session_state.reels = final_reels
        
        # 5. Win Check (STRICT 3-MATCH ONLY)
        # Since we use weights, getting 3 of a kind is actually hard now.
        if final_reels[0] == final_reels[1] == final_reels[2]:
            symbol = SYMBOL_MAP[final_reels[0]]
            win_amount = bet * symbol.payout
            
            st.session_state.balance += win_amount
            st.session_state.message = f"OH BABY! TRIPLE {symbol.name}! (+${win_amount})"
            
            if symbol.name == "Unicorn":
                st.session_state.game_state = "JACKPOT"
                st.session_state.current_meme = IMG_JACKPOT
            else:
                st.session_state.game_state = "WIN"
                st.session_state.current_meme = IMG_WIN
                
        else:
            # LOSS
            st.session_state.game_state = "LOSE"
            st.session_state.message = random.choice(ROASTS)
            st.session_state.current_meme = random.choice(IMG_LOSE)

        st.rerun()

# --- 7. MEME ZONE ---
if st.session_state.game_state == "WIN":
    st.balloons()
    st.success("WE TAKE THOSE!")
    if st.session_state.current_meme:
        st.image(st.session_state.current_meme, width=400)

elif st.session_state.game_state == "JACKPOT":
    st.balloons()
    st.snow()
    st.markdown("### 🦄 UNICORN STATUS ACHIEVED 🦄")
    st.image(st.session_state.current_meme)

elif st.session_state.game_state == "LOSE":
    st.error("L + Ratio")
    if st.session_state.current_meme:
        st.image(st.session_state.current_meme, width=300)

# --- 8. PAYOUT TABLE (Expandable) ---
with st.expander("📊 View Probability & Payouts"):
    st.markdown("""
    **Rules:** Match 3 symbols exactly. No participation trophies.
    
    | Symbol | Name | Payout | Difficulty |
    | :---: | :--- | :--- | :--- |
    | 🦄 | Unicorn | **500x** | IMPOSSIBLE (1%) |
    | 💎 | Diamond | **100x** | Hard (4%) |
    | 🚀 | Moon | **50x** | Rare (10%) |
    | 🍆 | Eggplant | **20x** | Uncommon (15%) |
    | 💩 | Poop | **10x** | Common (25%) |
    | 🥔 | Potato | **5x** | Everywhere (45%) |
    """)
