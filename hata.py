import streamlit as st
import random

st.set_page_config(page_title="旗揚げゲーム", layout="centered")

# --- ゲームデータの初期化 ---
if 'command' not in st.session_state:
    # 指示文と、それぞれの旗を「上げるべき(True)」か「下げるべき(False)」かの正解表
    st.session_state.master_commands = [
        {"text": "赤上げて、白上げない", "red": True, "white": False},
        {"text": "赤下げて、白上げる", "red": False, "white": True},
        {"text": "赤下げないで、白下げて", "red": True, "white": False},
        {"text": "白上げないで、赤上げる", "red": True, "white": False},
        {"text": "両方上げる！", "red": True, "white": True},
        {"text": "どっちも上げない", "red": False, "white": False},
    ]
    st.session_state.current_cmd = random.choice(st.session_state.master_commands)
    st.session_state.red_clicked = False
    st.session_state.white_clicked = False
    st.session_state.answered = False

st.title("🚩 旗揚げゲーム")
st.subheader(f"指示：【 {st.session_state.current_cmd['text']} 】")

st.write("※「上げろ」と言われた旗だけを押してください。下げろと言われたら放置！")

# --- 操作エリア ---
col1, col2 = st.columns(2)

with col1:
    # ボタンを押すと「上げた」状態(True)として保持
    if st.button("🔴 赤の旗を上げる", use_container_width=True):
        st.session_state.red_clicked = True
        st.toast("赤を上げました！")

with col2:
    if st.button("⚪ 白の旗を上げる", use_container_width=True):
        st.session_state.white_clicked = True
        st.toast("白を上げました！")

# 現在の選択状況を視覚的に表示
status_red = "🚩【上】" if st.session_state.red_clicked else "　【下】"
status_white = "🏳️【上】" if st.session_state.white_clicked else "　【下】"
st.write(f"現在の状態： 赤{status_red} ／ 白{status_white}")

st.divider()

# --- 判定エリア ---
if st.button("✨ 決定！", use_container_width=True, type="primary"):
    st.session_state.answered = True
    
    # 判定ロジック：ユーザーのクリック状態と、正解データの状態が一致しているか
    correct_red = (st.session_state.red_clicked == st.session_state.current_cmd['red'])
    correct_white = (st.session_state.white_clicked == st.session_state.current_cmd['white'])
    
    if correct_red and correct_white:
        st.balloons()
        st.success("⭕ 正解！ その通り！")
    else:
        st.error("❌ 不正解... 指示をよく聞いて！")
        st.write(f"正解は： 赤={'上げ' if st.session_state.current_cmd['red'] else '下げ'}, 白={'上げ' if st.session_state.current_cmd['white'] else '下げ'} でした。")

# 次へ進むボタン
if st.session_state.answered:
    if st.button("次の問題へ"):
        st.session_state.current_cmd = random.choice(st.session_state.master_commands)
        st.session_state.red_clicked = False
        st.session_state.white_clicked = False
        st.session_state.answered = False
        st.rerun()
