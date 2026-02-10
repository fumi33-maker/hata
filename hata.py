import streamlit as st
import random

st.set_page_config(page_title="旗揚げゲーム", layout="centered")

st.title("🚩 旗揚げゲーム")

# セッション状態の初期化
if 'command' not in st.session_state:
    st.session_state.command = "赤あげて、白あげない！"
    st.session_state.score = 0

# 指示の表示
st.info(f"指示：{st.session_state.command}")

# タブ（ボタン）の配置
col1, col2 = st.columns(2)

with col1:
    if st.button("赤の旗 🚩", use_container_width=True, type="primary"):
        # ここに判定ロジックを入れる（例：指示に「赤あげて」が含まれていたら正解など）
        st.success("赤を操作しました！")
        # 次の指示へ
        st.session_state.command = random.choice(["赤下げないで、白上げる", "白下げて、赤下げない"])

with col2:
    if st.button("白の旗 🏳️", use_container_width=True):
        st.success("白を操作しました！")
        st.session_state.command = random.choice(["赤上げて、白上げない", "両方下げる！"])

st.write(f"現在のスコア: {st.session_state.score}")
