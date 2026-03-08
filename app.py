# app.py
import streamlit as st
import random

# 作成した別ファイル（questions.py）から all_questions を読み込む
from questions import all_questions

# ---- Streamlit アプリ UI ----
st.set_page_config(page_title="メンタルヘルス検定2種 対策アプリ", layout="centered")

st.title("📒✎ メンタルヘルスマネジメント検定2種\nラインケアコース 想定問題集（難易度調整版）")
st.write("全50問のオリジナル問題集です。ひっかけ問題や詳細な知識を問う問題を含んでいます。選択肢を選んで「解答と解説を見る」を押してください。")

# 問題数が50問に満たない場合は、ある分だけを出題する
sample_size = min(50, len(all_questions))

# セッションステートを使って、リロード時のみ問題をランダム抽出する
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = random.sample(all_questions, sample_size)

st.write(f"全{len(all_questions)}問のプールから、ランダムに{sample_size}問を出題しています。")

# 問題をループして表示
for i, q in enumerate(st.session_state.selected_questions):
    st.markdown(f"### 第{i+1}問")
    st.write(q["question"])
    
    # 選択肢のラジオボタン（解答を選択）
    user_choice = st.radio("選択してください:", q["options"], key=f"q_{i}", index=None)
    
    # 解答と解説をアコーディオン（開閉式）で表示
    with st.expander("解答と解説を見る"):
        if user_choice:
            if user_choice == q["answer"]:
                st.success("⭕ 正解！")
            else:
                st.error("❌ 不正解...")
        
        st.markdown(f"**【正解】**\n{q['answer']}")
        st.info(f"**【解説】**\n{q['rationale']}")
    
    st.divider()

# 新しい問題をやり直すボタン
if st.button("🔄 問題をシャッフルして再挑戦する"):
    del st.session_state["selected_questions"]
    st.rerun()

st.caption("作成：Mental Health Management Consultant AI")