import streamlit as st
import random

st.set_page_config(page_title="旗揚げゲーム", layout="centered")

# --- 1. データと状態の初期化 ---
if 'master_commands' not in st.session_state:
    st.session_state.master_commands = [
        {"text": "赤上げて、白上げない", "red": True, "white": False},
        {"text": "赤下げて、白上げる", "red": False, "white": True},
        {"text": "赤下げないで、白下げて", "red": True, "white": False},
        {"text": "白上げないで、赤上げる", "red": True, "white": False},
        {"text": "赤も白も、下げない！", "red": True, "white": True},
        {"text": "どっちも上げない", "red": False, "white": False},
    ]

if 'current_cmd' not in st.session_state:
    st.session_state.current_cmd = random.choice(st.session_state.master_commands)
    st.session_state.red_up = False
    st.session_state.white_up = False
    st.session_state.answered = False

# --- 2. 文字サイズと太さの調整（CSS） ---
st.markdown(f"""
<style>
div.stButton > button {{
    font-size: 28px !important;
    font-weight: 900 !important;
    height: 3.5em !important;
    border: 3px solid #333 !important;
    border-radius: 15px !important;
}}
</style>
""", unsafe_allow_html=True)

# --- 3. メイン画面表示 ---
st.title("🚩 旗揚げゲーム")

st.markdown(f"""
<div style="background-color: #ffffff; padding: 15px; border-radius: 10px; border: 3px solid #333333;">
    <p style="font-size: 18px; margin: 0; color: #000000; font-weight: bold;">指示：</p>
    <p style="font-size: 24px; font-weight: 900; margin: 0; color: #000000;">【 {st.session_state.current_cmd['text']} 】</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. 操作エリア ---
col1, col2 = st.columns(2)

with col1:
    label_red = "🚩赤を【下げる】" if st.session_state.red_up else "🔴赤を【上げる】"
    if st.button(label_red, use_container_width=True):
        st.session_state.red_up = not st.session_state.red_up
        st.rerun()

with col2:
    label_white = "🏳️白を【下げる】" if st.session_state.white_up else "⚪白を【上げる】"
    if st.button(label_white, use_container_width=True):
        st.session_state.white_up = not st.session_state.white_up
        st.rerun()

# 現在の状態
r_status = "🚩【上】" if st.session_state.red_up else "　【下】"
w_status = "🏳️【上】" if st.session_state.white_up else "　【下】"
st.markdown(f"""
<div style="text-align: center; font-size: 20px; padding: 15px; color: #000000; font-weight: bold;">
    現在の状態： <span style="color: red;">赤{r_status}</span> ／ <span style="color: #333;">白{w_status}</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 5. 判定と風船の演出 ---
if not st.session_state.answered:
    if st.button("✨ これで決定！", use_container_width=True, type="primary"):
        # 判定
        correct_red = (st.session_state.red_up == st.session_state.current_cmd['red'])
        correct_white = (st.session_state.white_up == st.session_state.current_cmd['white'])
        
        if correct_red and correct_white:
            st.session_state.result_type = "success"
            st.session_state.result_msg = "⭕ 正解！！ お見事！"
            st.balloons() # ここで風船！
        else:
            st.session_state.result_type = "error"
            st.session_state.result_msg = "❌ 不正解... 指示をよく見て！"
        
        st.session_state.answered = True
        st.rerun()

else:
    # 結果表示
    if st.session_state.result_type == "success":
        st.success(st.session_state.result_msg)
    else:
        st.error(st.session_state.result_msg)

    # 「次の問題へ」ボタン
    if st.button("➔ 次の問題へ", use_container_width=True):
        st.session_state.current_cmd = random.choice(st.session_state.master_commands)
        st.session_state.red_up = False
        st.session_state.white_up = False
        st.session_state.answered = False
        st.rerun()
