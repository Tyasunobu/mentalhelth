# # app.py
# import streamlit as st
# import random

# # 作成した別ファイル（questions.py）から all_questions を読み込む
# from questions import all_questions

# # ---- Streamlit アプリ UI ----
# st.set_page_config(page_title="メンタルヘルス検定2種 対策アプリ", layout="centered")

# st.title("📒✎ メンタルヘルスマネジメント検定2種\nラインケアコース 想定問題集（難易度調整版）")
# st.write("全50問のオリジナル問題集です。ひっかけ問題や詳細な知識を問う問題を含んでいます。選択肢を選んで「解答と解説を見る」を押してください。")

# # 問題数が50問に満たない場合は、ある分だけを出題する
# sample_size = min(50, len(all_questions))

# # セッションステートを使って、リロード時のみ問題をランダム抽出する
# if "selected_questions" not in st.session_state:
#     st.session_state.selected_questions = random.sample(all_questions, sample_size)

# st.write(f"全{len(all_questions)}問のプールから、ランダムに{sample_size}問を出題しています。")

# # 問題をループして表示
# for i, q in enumerate(st.session_state.selected_questions):
#     st.markdown(f"### 第{i+1}問")
#     st.write(q["question"])
    
#     # 選択肢のラジオボタン（解答を選択）
#     user_choice = st.radio("選択してください:", q["options"], key=f"q_{i}", index=None)
    
#     # 解答と解説をアコーディオン（開閉式）で表示
#     with st.expander("解答と解説を見る"):
#         if user_choice:
#             if user_choice == q["answer"]:
#                 st.success("⭕ 正解！")
#             else:
#                 st.error("❌ 不正解...")
        
#         st.markdown(f"**【正解】**\n{q['answer']}")
#         st.info(f"**【解説】**\n{q['rationale']}")
    
#     st.divider()

# # 新しい問題をやり直すボタン
# if st.button("🔄 問題をシャッフルして再挑戦する"):
#     del st.session_state["selected_questions"]
#     st.rerun()

# st.caption("作成：Mental Health Management Consultant AI")

import streamlit as st
import random
from questions import all_questions

# ---- 初期設定と状態管理 ----
st.set_page_config(page_title="メンタルヘルス検定2種 対策アプリ", layout="centered")

# アプリの状態を管理する変数（初めて開いた時に初期化）
if "selected_questions" not in st.session_state:
    # 50問に満たない場合はある分だけ抽出
    sample_size = min(50, len(all_questions))
    st.session_state.selected_questions = random.sample(all_questions, sample_size)

# 採点画面に遷移したかどうかを判定するフラグ
if "is_submitted" not in st.session_state:
    st.session_state.is_submitted = False

# ---- 画面表示ロジック ----

# 1. 【解答画面】（まだ送信ボタンが押されていない場合）
if not st.session_state.is_submitted:
    st.title("📒✎ メンタルヘルスマネジメント検定2種\nラインケアコース 想定問題集")
    st.write("全問解答した後、一番下の「回答を送信」ボタンを押してください。")
    
    total_q = len(st.session_state.selected_questions)
    st.write(f"（全{total_q}問 / 1問1点の{total_q}点満点）")
    st.divider()

    # 問題表示ループ
    for i, q in enumerate(st.session_state.selected_questions):
        st.markdown(f"**問{i+1}**")
        st.write(q["question"])
        # keyを設定することで、ユーザーの選択が自動的に st.session_state[f"q_{i}"] に保存されます
        st.radio("選択してください:", q["options"], key=f"q_{i}", index=None)
        st.write("") # 少し余白を空ける

    st.divider()
    
    # 送信ボタン
    if st.button("📝 回答を送信して採点する", type="primary"):
        # ボタンが押されたらフラグをTrueにして画面を再読み込み
        st.session_state.is_submitted = True
        st.rerun()

# 2. 【採点・結果画面】（送信ボタンが押された後）
else:
    st.title("📊 採点結果")
    
    correct_count = 0
    total_q = len(st.session_state.selected_questions)

    # まず結果のリストを表示するためのコンテナ（枠）を作成
    results_container = st.container()
    
    with results_container:
        st.markdown("### 解答と解説")
        for i, q in enumerate(st.session_state.selected_questions):
            # ユーザーの解答を取得（未解答の場合は None）
            user_answer = st.session_state.get(f"q_{i}")
            correct_answer = q["answer"]
            
            # 正誤判定
            if user_answer == correct_answer:
                is_correct = True
                correct_count += 1
                mark = "〇"
                color = "green"
            else:
                is_correct = False
                mark = "×"
                color = "red"
            
            # 結果の表示
            st.markdown(f"**問{i+1}： <span style='color:{color}; font-size:1.2em;'>{mark}</span>**", unsafe_allow_html=True)
            
            # 未解答や間違えた場合のみ、ユーザーの解答を表示
            if user_answer is None:
                st.write(f"あなたの解答： *(未解答)*")
            elif not is_correct:
                st.write(f"あなたの解答： {user_answer}")
                
            st.write(f"**正解：** {correct_answer}")
            st.info(f"**解説：**\n{q['rationale']}")
            st.divider()

    # 総合得点の計算（1問1点）
    total_score = correct_count
    passing_score = int(total_q * 0.7) # 7割が合格ライン（50問なら35点）
    
    st.markdown("---")
    st.markdown(f"<h2 style='text-align: center;'>正解 {total_score} 点 / {total_q}点満点</h2>", unsafe_allow_html=True)
    
    # 合格基準の判定メッセージ
    if total_score >= passing_score:
        st.success(f"🎉 合格基準（{passing_score}点以上）をクリアしました！素晴らしいです！")
    else:
        st.warning(f"💪 合格基準（{passing_score}点以上）まであと少し！解説を読んで復習しましょう。")

    st.markdown("---")

    # リトライボタン
    if st.button("🔄 もう一度最初から挑戦する"):
        # セッション状態をクリアして最初の画面に戻る
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.caption("作成：Mental Health Management Consultant AI")