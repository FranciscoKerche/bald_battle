import streamlit as st
import pandas as pd
import random
from PIL import Image

# Load data
df = pd.read_csv("bald_celebrities.csv")
st.title("🧑‍🦲 Bald Battle!")

# Initialize session state
if "started" not in st.session_state:
    st.session_state.started = False
if "said_no" not in st.session_state:
    st.session_state.said_no = False

# Show intro screen
if not st.session_state.started:
    st.markdown("""
    ### Let's find out who deserves the right not to have a single hair on their head!

    Are you ready to play, **Clara**?
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes"):
            st.session_state.started = True
            st.rerun()

    with col2:
        if not st.session_state.said_no:
            if st.button("No"):
                st.session_state.said_no = True
                st.rerun()
        else:
            if st.button("Oops, sorry, I meant yes... I really wanna play it 😳"):
                st.session_state.started = True
                st.rerun()

    st.stop()





# Setup session state
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "current_pair" not in st.session_state:
    st.session_state.current_pair = random.sample(list(df.index), 2)
if "seen" not in st.session_state:
    st.session_state.seen = set()
if "round_num" not in st.session_state:
    st.session_state.round_num = 1
if "final_winner" not in st.session_state:
    st.session_state.final_winner = None

# Get Pitbull's index
pitbull_idx = df[df["Name"].str.lower() == "pitbull"].index
pitbull_idx = pitbull_idx[0] if not pitbull_idx.empty else None

# Helper to get next contender
def get_next_contender(exclude):
    valid_indexes = set(df.index) - st.session_state.seen - set(exclude)

    # Enforce Pitbull delay
    if st.session_state.round_num < 30 and pitbull_idx in valid_indexes:
        valid_indexes.remove(pitbull_idx)

    return random.choice(list(valid_indexes)) if valid_indexes else None

def declare_winner(name, img_path):
    st.markdown(f"""
                ## Clara, it's settled, your favorite bald person is: **{name}**! 🫢
                And now 30 minutes of your airplane ride are just gone, you can thank me anytime!""")
    st.image(img_path, use_container_width=True)

# Get current pair
a_idx, b_idx = st.session_state.current_pair
a_row = df.loc[a_idx]
b_row = df.loc[b_idx]

col1, col2 = st.columns(2)

# Display one celeb
def display_celeb(col, row, button_key):
    if col.button("👇 Vote", key=button_key):
        winner_idx = row.name
        loser_idx = b_idx if row.name == a_idx else a_idx

        # Update round and scores
        st.session_state.scores[winner_idx] = st.session_state.scores.get(winner_idx, 0) + 1
        st.session_state.seen.add(loser_idx)
        st.session_state.round_num += 1

        new_idx = get_next_contender(exclude=[winner_idx, loser_idx])

        if new_idx is None:
            st.session_state.final_winner = winner_idx
        else:
            st.session_state.current_pair = [winner_idx, new_idx]

        st.rerun()

    col.image(row["Image Path"], caption=row["Name"], use_container_width=True)
    col.markdown(f"""
    - **Height**: {row['Height:']}
    - **DOB**: {row['DOB:']}
    - **Birthplace**: {row['Birth Place:']}
    - **Net Worth**: {row['Net Worth:']}
    - **Zodiac**: {row['Zodiac:']}
    - **Relationship**: {row['Relationship Status:']}
    - **Ethnicity**: {row['Ethnicity:']}
    """)
    col.markdown(f"{row['Description']}")

# Final winner logic
if st.session_state.final_winner is not None:
    winner_row = df.loc[st.session_state.final_winner]
    declare_winner(winner_row["Name"], winner_row["Image Path"])
else:
    display_celeb(col1, a_row, "vote_left")
    display_celeb(col2, b_row, "vote_right")
