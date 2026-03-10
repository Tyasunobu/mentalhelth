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
    st.session_state.current_q_index = 0 # 現在の問題番号（0スタート）

# ==========================================
# 📊 結果表示画面（採点モード）
# ==========================================
if st.session_state.show_score:
    st.title("📊 採点結果")
    
    # 全問をループして正解数をカウント
    correct_count = 0
    for i, q in enumerate(st.session_state.selected_questions):
        # ユーザーの解答をセッションから取得（未解答は None になる）
        user_choice = st.session_state.get(f"q_{i}")
        if user_choice == q["answer"]:
            correct_count += 1

    st.markdown("---")
    st.markdown(f"<h2 style='text-align: center;'>あなたの点数は {correct_count * 2} 点</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>正解数は {correct_count} 問 / {sample_size}問中 です！</h2>", unsafe_allow_html=True)
    
    # 7割（35問）を合格ラインとしてメッセージを切り替え
    passing_score = int(sample_size * 0.7)
    if correct_count >= passing_score:
        st.success(f"🎉 合格基準（{passing_score}問以上）をクリアしています！素晴らしいです！")
    elif correct_count >= passing_score * 0.5:
        st.warning(f"💪 合格基準（{passing_score}問以上）まであと少し！間違えた問題を復習しましょう。")
    else:
        st.error(f"💪 合格基準（{passing_score}問以上）努力あるのみ！！諦めないで！！やればできる！！")
    st.markdown("---")

    # リセットボタン
    if st.button("🔄 問題をシャッフルして再挑戦する", use_container_width=True):
        # セッションの初期化
        del st.session_state["selected_questions"]
        del st.session_state["show_score"]
        del st.session_state["current_q_index"]
        
        # ラジオボタンの選択履歴（q_0, q_1...）もクリアして白紙に戻す
        for key in list(st.session_state.keys()):
            if key.startswith("q_"):
                del st.session_state[key]
                
        st.rerun()

    st.caption("作成：Mental Health Management Consultant AI")

# ==========================================
# 📝 1問1答の解答画面（テストモード）
# ==========================================
else:
    # 現在の問題インデックスと問題データを取得
    q_idx = st.session_state.current_q_index
    q = st.session_state.selected_questions[q_idx]

    st.title("📒✎ メンタルヘルスマネジメント検定2種\nラインケアコース 想定問題集")
    st.write(f"全{len(all_questions)}問のプールから、ランダムに{sample_size}問を出題しています。")
    
    # 進行度をプログレスバーで表示
    progress_val = (q_idx + 1) / sample_size
    st.progress(progress_val)
    st.write(f"**第 {q_idx + 1} 問 / 全 {sample_size} 問**")
    
    # 問題文の表示
    st.markdown(f"### {q['question']}")
    
    # 選択肢のラジオボタン
    # keyに f"q_{q_idx}" を指定することで、解答が自動的に裏側に保存されます。前後の問題に移動しても選択状態が維持されます。
    user_choice = st.radio("選択してください:", q["options"], key=f"q_{q_idx}", index=None)
    
    # 解答と解説のアコーディオン
    with st.expander("解答と解説を見る"):
        if user_choice:
            if user_choice == q["answer"]:
                st.success("⭕ 正解！")
            else:
                st.error("❌ 不正解...")
        
        st.markdown(f"**【正解】**\n{q['answer']}")
        st.info(f"**【解説】**\n{q['rationale']}")
    
    st.divider()

    # --- ナビゲーションボタン（前へ / 次へ） ---
    col1, col2 = st.columns(2)
    
    with col1:
        if q_idx > 0:
            if st.button("◀ 前の問題へ", use_container_width=True):
                st.session_state.current_q_index -= 1
                st.rerun()
                
    with col2:
        if q_idx < sample_size - 1:
            if st.button("次の問題へ ▶", type="primary", use_container_width=True):
                st.session_state.current_q_index += 1
                st.rerun()

    st.write("") # 少し余白

    # --- 中断 / 完了ボタン ---
    # 最終問題かそうでないかでボタンの文言と色を変える
    if q_idx < sample_size - 1:
        if st.button("📝 回答を中断して結果を見る", use_container_width=True):
            st.session_state.show_score = True
            st.rerun()
    else:
        if st.button("📝 すべての回答を送信して結果を見る", type="primary", use_container_width=True):
            st.session_state.show_score = True
            st.rerun()

    st.caption("作成：Mental Health Management Consultant AI")