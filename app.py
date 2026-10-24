import time
import streamlit as st

# ---------------- CONFIG ----------------
GRID_TEXT = """
Q Z M R T P L X B N K W J F H
V C Y G D S A Q P L Z R T M X
K H W B N J F V Q I Y L P D S
R P X T M G Z K H L B Q N Y F
D L Q V C R J N X O G T Z K M
Y F B K W H P D S V L X R V C
M Z R N T Y G Q F E B W D P L
C X H J V L M R P Y Q N K T B
W G D P S F X Y N O J L V Q R
B N K Q H T R Z M U F D P Y X
P V C M L X G B Q B T K N J Z
F J Y D W N Z P H A C V Q M K
T Q B R K G X M Y B J Z D L V
N W L F P C Q T B Y M R H K Y
Z R G V J M D Y K N L F W C P
"""

# Correct buttons as (row, column), counting from 1.
# PLACEHOLDER: these are the vowels in the grid. Replace with your own!
CORRECT_CELLS = {
    (3, 10),
    (4, 10),
    (5, 10),
    (6, 10),
    (7, 10),
    (8, 10),
    (9, 10),
    (10, 10),
    (11, 10),
    (12, 10),
    (13, 10),
    (14, 10),
}

WIN_MESSAGE = "You found the word :) Hi Brianna! I love you so so much, more than words can describe. I always imagine our relationship as one that could last forever. I am so happy being with you and there is not a doubt in my mind about you, and I hope that you feel the same way about me. This is both of our longest relationships that we have been in, and I think that shows the level of commitment we have for eachother. I hope that we continue to grow and be the best people we can be. As for right now, I hope you are able to continue doing well in school, making US money through your job, and finishing your voulenteering hours or however you spell it. When I think of a perfect future, I imagine the ability to settle down, own a house, have a stable job that doesn't cause me stress, and a family. I hope that can be us, and in order for it to be us we have to work hard right now. I am sure we can make that happen. Anyway, I love you more than anything and hope you have a good day at work!"
RED_SECONDS = 2
# ----------------------------------------

grid = [line.split() for line in GRID_TEXT.strip().splitlines()]
SIZE = len(grid)
correct = {(r - 1, c - 1) for r, c in CORRECT_CELLS}  # convert to 0-indexed

st.set_page_config(page_title="Find the hidden message", layout="wide")

# ---- session state ----
if "found" not in st.session_state:
    st.session_state.found = set()
if "wrong" not in st.session_state:
    st.session_state.wrong = None  # (r, c, timestamp)

# Clear an expired red button
if st.session_state.wrong:
    _, _, t = st.session_state.wrong
    if time.time() - t >= RED_SECONDS:
        st.session_state.wrong = None


def on_click(r, c):
    if (r, c) in correct:
        st.session_state.found.add((r, c))
    else:
        st.session_state.wrong = (r, c, time.time())


# ---- CSS to color buttons (targets each button by its key) ----
css = ["<style>"]
css.append("div[class*='st-key-cell_'] button {padding: 0.25rem 0; min-height: 2.5rem;}")
for (r, c) in st.session_state.found:
    css.append(
        f".st-key-cell_{r}_{c} button "
        "{background-color:#2ecc71 !important; color:white !important; border-color:#27ae60 !important;}"
    )
if st.session_state.wrong:
    wr, wc, _ = st.session_state.wrong
    css.append(
        f".st-key-cell_{wr}_{wc} button "
        "{background-color:#e74c3c !important; color:white !important; border-color:#c0392b !important;}"
    )
css.append("</style>")
st.markdown("\n".join(css), unsafe_allow_html=True)

# ---- UI ----
st.title("Find the hidden message")

for r in range(SIZE):
    cols = st.columns(SIZE, gap="small")
    for c in range(SIZE):
        cols[c].button(
            grid[r][c],
            key=f"cell_{r}_{c}",
            on_click=on_click,
            args=(r, c),
            use_container_width=True,
        )

if correct and correct <= st.session_state.found:
    st.success(WIN_MESSAGE)
    st.balloons()

# ---- make the red disappear after 2 seconds ----
if st.session_state.wrong:
    _, _, t = st.session_state.wrong
    time.sleep(max(0.0, RED_SECONDS - (time.time() - t)))
    st.session_state.wrong = None
    st.rerun()
