import streamlit as st
import random

st.set_page_config(page_title="タブで旗揚げゲーム", layout="centered")

st.title("🚩 タブ選択！旗揚げゲーム")
st.write("上の指示を見て、下のタブから**正しい旗の状態**を選んでクリックしてください！")

# --- セッション状態の初期化 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.game_over = False
    # 指示のバリエーション
    st.session_state.options = [
        {"text": "赤上げて、白上げて", "ans": (True, True)},
        {"text": "赤下げて、白下げて", "ans": (False, False)},
        {"text": "赤下げないで、白上げる", "ans": (True, True)}, # ひっかけ：下げない＝上げ
        {"text": "赤上げないで、白下げない", "ans": (False, True)}, # ひっかけ
        {"text": "白下げて、赤上げる", "ans": (True, False)},
    ]
    st.session_state.current_q = random.choice(st.session_state.options)

# --- ゲームオーバー画面 ---
if st.session_state.game_over:
    st.error(f"ざんねん！スコア: {st.session_state.score}")
    if st.button("もう一度挑戦"):
        st.session_state.score = 0
        st.session_state.game_over = False
        st.rerun()
    st.stop()

# --- 指示の表示 ---
st.info(f"指示： **{st.session_state.current_q['text']}**")

# --- タブによる選択肢 ---
# ここでタブを4つ作り、それぞれの状態をシミュレーションします
tab1, tab2, tab3, tab4 = st.tabs([
    "🔴下・⚪️下", "🔴上・⚪️下", "🔴下・⚪️上", "🔴上・⚪️上"
])

# 正解の判定ロジック
def check_answer(user_red, user_white):
    correct_red, correct_white = st.session_state.current_q['ans']
    if user_red == correct_red and user_white == correct_white:
        st.session_state.score += 1
        st.session_state.current_q = random.choice(st.session_state.options)
        st.toast("正解！✨")
        st.rerun()
    else:
        st.session_state.game_over = True
        st.rerun()

# 各タブの中に「この状態にする」というボタンを配置
with tab1:
    st.write("今の状態： 赤は下、白は下")
    st.button("これで決定！", key="t1", on_click=check_answer, args=(False, False))

with tab2:
    st.write("今の状態： 赤は上、白は下")
    st.button("これで決定！", key="t2", on_click=check_answer, args=(True, False))

with tab3:
    st.write("今の状態： 赤は下、白は上")
    st.button("これで決定！", key="t3", on_click=check_answer, args=(False, True))

with tab4:
    st.write("今の状態： 赤は上、白は上")
    st.button("これで決定！", key="t4", on_click=check_answer, args=(True, True))

st.write(f"現在のスコア: {st.session_state.score}")
