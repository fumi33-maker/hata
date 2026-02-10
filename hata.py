import streamlit as st
import random

st.set_page_config(page_title="旗揚げゲーム", layout="centered")

# --- データ準備 ---
if 'master_commands' not in st.session_state:
    st.session_state.master_commands = [
        {"text": "赤上げて、白上げない", "red": True, "white": False},
        {"text": "赤下げて、白上げる", "red": False, "white": True},
        {"text": "赤下げないで、白下げて", "red": True, "white": False},
        {"text": "白上げないで、赤上げる", "red": True, "white": False},
        {"text": "赤も白も、下げない！", "red": True, "white": True},
        {"text": "どっちも上げない", "red": False, "white": False},
    ]

# --- ゲーム状態の初期化 ---
if 'current_cmd' not in st.session_state:
    st.session_state.current_cmd = random.choice(st.session_state.master_commands)
    st.session_state.red_up = False
    st.session_state.white_up = False
    st.session_state.answered = False

# --- メイン画面 ---
st.title("🚩 旗揚げゲーム")

# 【微調整】指示のサイズを1つ下げる（subheader相当から少し小さめに）
st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 10px; border-radius: 10px; border: 1px solid #ddd;">
    <p style="font-size: 18px; margin: 0; color: #555;">指示：</p>
    <p style="font-size: 22px; font-weight: bold; margin: 0;">【 {st.session_state.current_cmd['text']} 】</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 操作エリア ---
col1, col2 = st.columns(2)

# ボタンのフォントを大きくするためのカスタムCSS
st.markdown("""
<style>
div.stButton > button {
    font-size: 24px !important; /* ボタンの文字サイズを大きく */
    height: 3em !important;
}
</style>
""", unsafe_allow_html=True)

with col1:
    label_red = "🚩 赤を【下げる】" if st.session_state.red_up else "🔴 赤を【上げる】"
    if st.button(label_red, use_container_width=True):
        st.session_state.red_up = not st.session_state.red_up
        st.rerun()

with col2:
    label_white = "🏳️ 白を【下げる】" if st.session_state.white_up else "⚪ 白を【上げる】"
    if st.button(label_white, use_container_width=True):
        st.session_state.white_up = not st.session_state.white_up
        st.rerun()

# 【微調整】現在の状態のサイズを1つ下げる
r_status = "🚩【上】" if st.session_state.red_up else "　【下】"
w_status = "🏳️【上】" if st.session_state.white_up else "　【下】"

st.markdown(f"""
<div style="text-align: center; font-size: 18px; padding: 10px; color: #666;">
    現在の状態： <b>赤{r_status} ／ 白{w_status}</b>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 判定ボタン ---
if not st.session_state.answered:
    if st.button("✨ これで決定！", use_container_width=True, type="primary"):
        st.session_state.answered = True
        
        correct_red = (st.session_state.red_up == st.session_state.current_cmd['red'])
        correct_white = (st.session_state.white_up == st.session_state.current_cmd['white'])
        
        if correct_red and correct_white:
            st.balloons()
            st.success("⭕ 正解！！")
        else:
            st.error("❌ 不正解...")
            st.write(f"正解は： 赤={'上げ' if st.session_state.current_cmd['red'] else '下げ'}, 白={'上げ' if st.session_state.current_cmd['white'] else '下げ'} でした。")

# 次へ進む
if st.session_state.answered:
    if st.button("次の問題へ ➔"):
        st.session_state.current_cmd = random.choice(st.session_state.master_commands)
        st.session_state.red_up = False
        st.session_state.white_up = False
        st.session_state.answered = False
        st.rerun()
