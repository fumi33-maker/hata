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

# --- 【重要】ここがサイズ調整場所です！ ---
st.markdown(f"""
<style>
/* すべてのボタン（赤・白・決定・次へ）の共通設定 */
div.stButton > button {{
    font-size: 28px !important;    /* ← 【サイズ調整】数字を大きくするとフォントが大きくなります */
    font-weight: 900 !important;   /* ← 【太さ調整】900が最大（超太字）です */
    height: 3.5em !important;      /* ← 【ボタンの高さ】 */
    border: 3px solid #333 !important;
    border-radius: 15px !important;
}}
</style>
""", unsafe_allow_html=True)

# --- メイン画面 ---
st.title("🚩 旗揚げゲーム")

# 指示：文字サイズ 24px
st.markdown(f"""
<div style="background-color: #ffffff; padding: 15px; border-radius: 10px; border: 3px solid #333333;">
    <p style="font-size: 18px; margin: 0; color: #000000; font-weight: bold;">指示：</p>
    <p style="font-size: 24px; font-weight: 900; margin: 0; color: #000000;">【 {st.session_state.current_cmd['text']} 】</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 操作エリア（赤の旗・白の旗） ---
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

# 現在の状態：文字サイズ 20px
r_status = "🚩【上】" if st.session_state.red_up else "　【下】"
w_status = "🏳️【上】" if st.session_state.white_up else "　【下】"

st.markdown(f"""
<div style="text-align: center; font-size: 20px; padding: 15px; color: #000000; font-weight: bold;">
    現在の状態： <span style="color: red;">赤{r_status}</span> ／ <span style="color: #333;">白{w_status}</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 判定ボタンと「次の問題へ」ボタン ---
# 「決定」ボタンは回答前だけ表示
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
        st.rerun() # 結果を表示するために再描画

# 【復活！】回答済み（判定後）なら「次の問題へ」ボタンを表示
if st.session_state.answered:
    if st.button("➔ 次の問題へ", use_container_width=True):
        st.session_state.current_cmd = random.choice(st.session_state.master_commands)
        st.session_state.red_up = False
        st.session_state.white_up = False
        st.session_state.answered = False
        st.rerun()
