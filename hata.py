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
    st.session_state.is_correct = False

# --- 2. 文字サイズと太さの調整（CSS） ---
st.markdown(f"""
<style>
/* 共通設定：太字、枠線、角丸 */
div.stButton > button {{
    font-weight: 900 !important;
    border: 3px solid #333 !important;
    border-radius: 15px !important;
}}

/* 【赤ボタン専用の設定】 */
div.stButton > button[key="red_btn"] {{
    font-size: 39px !important;  /* ←ここを調整！数字を大きくするとデカくなります */
    height: 4.0em !important;
}}

/* 【白ボタン専用の設定】 */
div.stButton > button[key="white_btn"] {{
    font-size: 35px !important;  /* ←ここを調整！ */
    height: 3.5em !important;
}}

/* 【決定ボタン専用の設定】 */
div.stButton > button[key="decision_btn"] {{
    font-size: 49px !important;  /* 決定ボタンはさらにデカく！ */
    height: 4.0em !important;
}}

/* 【次の問題へボタン専用の設定】 */
div.stButton > button[key="next_btn"] {{
    font-size: 30px !important;
    height: 3.0em !important;
}}
</style>
""", unsafe_allow_html=True)

# --- 3. メイン画面表示 ---
st.title("🚩 旗揚げゲーム")

# 指示：文字色を黒に固定
st.markdown(f"""
<div style="background-color: #ffffff; padding: 15px; border-radius: 10px; border: 3px solid #333333;">
    <p style="font-size: 18px; margin: 0; color: #000000; font-weight: bold;">指示：</p>
    <p style="font-size: 24px; font-weight: 900; margin: 0; color: #000000;">【 {st.session_state.current_cmd['text']} 】</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. 操作エリア（旗を上げる・下げる） ---
col1, col2 = st.columns(2)

with col1:
    label_red = "🚩赤を【下げる】" if st.session_state.red_up else "🔴赤を【上げる】"
    if st.button(label_red, use_container_width=True, key="red_btn"):
        st.session_state.red_up = not st.session_state.red_up
        st.rerun()

with col2:
    label_white = "🏳️白を【下げる】" if st.session_state.white_up else "⚪白を【上げる】"
    if st.button(label_white, use_container_width=True, key="white_btn"):
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

# --- 5. 判定と「次へ」の切り替え ---
if not st.session_state.answered:
    # 決定ボタンを表示（key="decision_btn"）
    if st.button("✨ これで決定！", use_container_width=True, type="primary", key="decision_btn"):
        correct_red = (st.session_state.red_up == st.session_state.current_cmd['red'])
        correct_white = (st.session_state.white_up == st.session_state.current_cmd['white'])
        
        st.session_state.answered = True
        st.session_state.is_correct = (correct_red and correct_white)
        st.rerun()

else:
    # 判定後の演出
    if st.session_state.is_correct:
        st.balloons()
        st.success("⭕ 正解！！ やった～！")
    else:
        st.error("❌ 残念... ")

    # 「次の問題へ」ボタンを表示（key="next_btn"）
    if st.button("➔ 次の問題へ", use_container_width=True, key="next_btn"):
        st.session_state.current_cmd = random.choice(st.session_state.master_commands)
        st.session_state.red_up = False
        st.session_state.white_up = False
        st.session_state.answered = False
        st.session_state.is_correct = False
        st.rerun()

