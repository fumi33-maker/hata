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
    st.session_state.red_up = False    # 「上げているか」の状態を保存
    st.session_state.white_up = False
    st.session_state.answered = False

# --- メイン画面 ---
st.title("🚩 旗揚げゲーム")

with st.container(border=True):
    st.subheader(f"指示：【 {st.session_state.current_cmd['text']} 】")

st.write("※ボタンを押すたびに「上げ」「下げ」が切り替わります。")

# --- 操作エリア ---
col1, col2 = st.columns(2)

with col1:
    # 赤の旗ボタン
    label_red = "🚩 赤を【下げる】" if st.session_state.red_up else "🔴 赤を【上げる】"
    if st.button(label_red, use_container_width=True):
        # 状態を反転させる（TrueならFalseに、FalseならTrueに）
        st.session_state.red_up = not st.session_state.red_up
        st.rerun() # 状態を即座にラベルに反映させるために再描画

with col2:
    # 白の旗ボタン
    label_white = "🏳️ 白を【下げる】" if st.session_state.white_up else "⚪ 白を【上げる】"
    if st.button(label_white, use_container_width=True):
        st.session_state.white_up = not st.session_state.white_up
        st.rerun()

# 現在の状態を表示
r_status = "🚩【上】" if st.session_state.red_up else "　【下】"
w_status = "🏳️【上】" if st.session_state.white_up else "　【下】"

st.markdown(f"""
<div style="text-align: center; font-size: 24px; padding: 10px; border: 2px solid #eee; border-radius: 10px;">
    現在の状態： <b>赤{r_status} ／ 白{w_status}</b>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 判定ボタン ---
if not st.session_state.answered:
    if st.button("✨ これで決定！", use_container_width=True, type="primary"):
        st.session_state.answered = True
        
        # 判定
        correct_red = (st.session_state.red_up == st.session_state.current_cmd['red'])
        correct_white = (st.session_state.white_up == st.session_state.current_cmd['white'])
        
        if correct_red and correct_white:
            st.balloons()
            st.success("⭕ 正解！！ お見事！")
        else:
            st.error("❌ 不正解... 指示をよく見て！")
            st.write(f"正解は： 赤={'上げ' if st.session_state.current_cmd['red'] else '下げ'}, 白={'上げ' if st.session_state.current_cmd['white'] else '下げ'} でした。")

# 次へ進む
if st.session_state.answered:
    if st.button("次の問題へ ➔"):
        st.session_state.current_cmd = random.choice(st.session_state.master_commands)
        st.session_state.red_up = False
        st.session_state.white_up = False
        st.session_state.answered = False
        st.rerun()
