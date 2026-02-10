import streamlit as st
import random

st.set_page_config(page_title="旗揚げゲーム", layout="centered")

# --- マスタデータ（指示のリスト） ---
if 'master_commands' not in st.session_state:
    st.session_state.master_commands = [
        {"text": "赤上げて、白上げない", "red": True, "white": False},
        {"text": "赤下げて、白上げる", "red": False, "white": True},
        {"text": "赤下げないで、白下げて", "red": True, "white": False},
        {"text": "白上げないで、赤上げる", "red": True, "white": False},
        {"text": "赤も白も、下げない！", "red": True, "white": True},
        {"text": "どっちも上げない", "red": False, "white": False},
    ]

# --- ゲーム状態の初期化（ここがポイント！） ---
if 'current_cmd' not in st.session_state:
    # 初回だけ指示を決める
    st.session_state.current_cmd = random.choice(st.session_state.master_commands)
    st.session_state.red_clicked = False
    st.session_state.white_clicked = False
    st.session_state.answered = False

# --- メイン画面 ---
st.title("🚩 旗揚げゲーム")

# 枠で囲って指示を強調
with st.container(border=True):
    st.subheader(f"指示：【 {st.session_state.current_cmd['text']} 】")

st.write("※「上げろ」と言われた旗だけを押してください。")

# --- 操作エリア ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🔴 赤の旗を上げる", use_container_width=True):
        st.session_state.red_clicked = True
        # st.rerun() を入れないことで、指示を固定したまま状態だけ保持

with col2:
    if st.button("⚪ 白の旗を上げる", use_container_width=True):
        st.session_state.white_clicked = True

# 現在、自分がどの旗を上げているか確認用（これがないと不安なので）
r_mark = "🚩" if st.session_state.red_clicked else "　"
w_mark = "🏳️" if st.session_state.white_clicked else "　"
st.markdown(f"### 現在の状態: 赤{r_mark} / 白{w_mark}")

st.divider()

# --- 判定ボタン ---
if not st.session_state.answered:
    if st.button("✨ 決定！", use_container_width=True, type="primary"):
        st.session_state.answered = True
        
        # 判定
        correct_red = (st.session_state.red_clicked == st.session_state.current_cmd['red'])
        correct_white = (st.session_state.white_clicked == st.session_state.current_cmd['white'])
        
        if correct_red and correct_white:
            st.balloons()
            st.success("⭕ 正解！！")
        else:
            st.error("❌ 不正解...")
            st.write(f"正解は： 赤={'上げ' if st.session_state.current_cmd['red'] else '下げ'}, 白={'上げ' if st.session_state.current_cmd['white'] else '下げ'} でした。")

# 次へ進む（ここで初めて指示をリセットする）
if st.session_state.answered:
    if st.button("次の問題へ ➔"):
        st.session_state.current_cmd = random.choice(st.session_state.master_commands)
        st.session_state.red_clicked = False
        st.session_state.white_clicked = False
        st.session_state.answered = False
        st.rerun()
