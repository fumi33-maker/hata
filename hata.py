import streamlit as st
import random

st.set_page_config(page_title="旗揚げゲーム Pro", layout="centered")

# --- ゲームのデータ準備 ---
if 'game_status' not in st.session_state:
    st.session_state.command = "赤あげて、白あげない"
    st.session_state.red_up = False
    st.session_state.white_up = False
    st.session_state.result = None

# 指示と正解のパターンの定義
commands = {
    "赤あげて、白あげない": {"red": True, "white": False},
    "赤下げないで、白上げる": {"red": True, "white": True},
    "白下げて、赤あげない": {"red": False, "white": False},
    "両方あげて！": {"red": True, "white": True},
    "赤あげて、白下げる": {"red": True, "white": False},
}

def next_game():
    st.session_state.command = random.choice(list(commands.keys()))
    st.session_state.result = None

# --- UI部分 ---
st.title("🚩 旗揚げオンライン")
st.subheader(f"指示：【 {st.session_state.command} 】")

st.divider()

# 旗の状態を選択（トグルやボタンで表現）
col1, col2 = st.columns(2)

with col1:
    st.write("🔴 赤の旗")
    red_status = st.radio("状態", ["下げている", "上げている"], 
                          index=1 if st.session_state.red_up else 0, key="red_radio")
    st.session_state.red_up = (red_status == "上げている")

with col2:
    st.write("⚪ 白の旗")
    white_status = st.radio("状態", ["下げている", "上げている"], 
                            index=1 if st.session_state.white_up else 0, key="white_radio")
    st.session_state.white_up = (white_status == "上げている")

st.divider()

# --- 判定ボタン ---
if st.button("これで決定！", use_container_width=True, type="primary"):
    correct_state = commands[st.session_state.command]
    
    # 判定ロジック
    is_red_correct = st.session_state.red_up == correct_state["red"]
    is_white_correct = st.session_state.white_up == correct_state["white"]
    
    if is_red_correct and is_white_correct:
        st.session_state.result = "⭕ 正解！！"
    else:
        st.session_state.result = "❌ 残念、不正解..."

# 結果表示
if st.session_state.result:
    if "⭕" in st.session_state.result:
        st.success(st.session_state.result)
    else:
        st.error(st.session_state.result)
    
    if st.button("次の問題へ"):
        next_game()
        st.rerun()
