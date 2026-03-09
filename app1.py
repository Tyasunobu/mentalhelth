import streamlit as st
import random
from questions import all_questions

# ページ設定
st.set_page_config(page_title="メンタルヘルス検定2種 対策アプリ", layout="centered")

sample_size = min(50, len(all_questions))

# セッションステートの初期化
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = random.sample(all_questions, sample_size)
    st.session_state.show_score = False  # 総合点表示フラグ

st.title("📒✎ メンタルヘルスマネジメント検定2種\nラインケアコース 想定問題集")
st.write(f"全{len(all_questions)}問のプールから、ランダムに{sample_size}問を出題しています。")

# 正解数をカウントする変数
correct_count = 0

for i, q in enumerate(st.session_state.selected_questions):
    st.markdown(f"### 第{i+1}問")
    st.write(q["question"])
    
    # 選択肢のラジオボタン（解答を選択）
    user_choice = st.radio("選択してください:", q["options"], key=f"q_{i}", index=None)
    
    # 裏側で正解数をカウントしておく
    if user_choice == q["answer"]:
        correct_count += 1
    
    with st.expander("解答と解説を見る"):
        if user_choice:
            if user_choice == q["answer"]:
                st.success("⭕ 正解！")
            else:
                st.error("❌ 不正解...")
        
        st.markdown(f"**【正解】**\n{q['answer']}")
        st.info(f"**【解説】**\n{q['rationale']}")
    
    st.divider()

# --- ここからが追加した採点機能 ---

# 回答送信ボタン
if st.button("📝 回答を送信して総合点を見る", type="primary"):
    st.session_state.show_score = True

# ボタンが押されたら結果を表示する
if st.session_state.get("show_score", False):
    st.markdown("---")
    st.markdown(f"<h2 style='text-align: center;'>あなたの点数は{correct_count*2} 点")
    st.markdown(f"<h2 style='text-align: center;'>あなたの正解数は {correct_count} 問 / {sample_size}問中 です！</h2>", unsafe_allow_html=True)
    
    # 7割（35問）を合格ラインとしてメッセージを切り替え
    passing_score = int(sample_size * 0.7)
    if correct_count >= passing_score:
        st.success(f"🎉 合格基準（{passing_score}問以上）をクリアしています！素晴らしいです！")
    else:
        st.warning(f"💪 合格基準（{passing_score}問以上）まであと少し！間違えた問題を復習しましょう。")
    st.markdown("---")

# --- リセットボタン ---
if st.button("🔄 問題をシャッフルして再挑戦する"):
    # 問題の入れ替えと、スコア表示フラグのクリア
    del st.session_state["selected_questions"]
    if "show_score" in st.session_state:
        del st.session_state["show_score"]
    
    # ラジオボタンの選択履歴（q_0, q_1...）もクリアして白紙に戻す
    for key in list(st.session_state.keys()):
        if key.startswith("q_"):
            del st.session_state[key]
            
    st.rerun()

st.caption("作成：Mental Health Management Consultant AI")