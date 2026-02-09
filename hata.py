import streamlit as st
import random
import time

st.set_page_config(page_title="Streamlit旗揚げゲーム", layout="centered")

# --- タイトルとルール説明 ---
st.title("🚩 旗揚げゲーム")
st.write("指示通りにボタンを押してください。間違えたり、制限時間を過ぎるとゲームオーバー！")

# --- セッション状態の初期化 ---
if 'game_status' not in st.session_state:
    st.session_state.game_status = "waiting" # waiting, playing, gameover
    st.session_state.score = 0
    st.session_state.command = ""
    st.session_state.answer_red = False  # True=上げ, False=下げ
    st.session_state.answer_white = False

# --- コマンド生成関数 ---
def next_command():
    # 旗の状態（上げ・下げ）をランダムに決定
    st.session_state.answer_red = random.choice([True, False])
    st.session_state.answer_white = random.choice([True, False])
    
    # 指示文の作成
    red_text = "赤上げて" if st.session_state.answer_red else "赤下げて"
    white_text = "白上げて" if st.session_state.answer_white else "白下げて"
    st.session_state.command = f"【 {red_text} 】【 {white_text} 】"

def start_game():
    st.session_state.game_status = "playing"
    st.session_state.score = 0
    next_command()

# --- ゲーム画面の構築 ---
if st.session_state.game_status == "waiting":
    st.button("ゲーム開始！", on_click=start_game, type="primary")

elif st.session_state.game_status == "playing":
    # 指示の表示
    st.subheader(st.session_state.command)
    
    # 旗の操作（チェックボックスを旗に見立てる）
    col1, col2 = st.columns(2)
    with col1:
        red_up = st.checkbox("🚩 赤い旗（チェックで上げる）", key="red")
    with col2:
        white_up = st.checkbox("🏳️ 白い旗（チェックで上げる）", key="white")

    # 決定ボタン
    if st.button("これで確定！"):
        if red_up == st.session_state.answer_red and white_up == st.session_state.answer_white:
            st.session_state.score += 1
            st.toast("正解！次いくよ！")
            next_command()
            st.rerun()
        else:
            st.session_state.game_status = "gameover"
            st.rerun()

    st.write(f"現在のスコア: {st.session_state.score}")

elif st.session_state.game_status == "gameover":
    st.error(f"あーっ！間違えました！ スコア: {st.session_state.score}")
    if st.button("リトライ"):
        st.session_state.game_status = "waiting"
        st.rerun()
        