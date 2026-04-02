import streamlit as st
import time
import pandas as pd
import plotly.express as px
from logic.analyzer import get_weak_keys
from logic.generator import generate_problem

# ページ設定
user_input = st.text_input("Input:", key="typing_box", value=st.session_state.get('typing_box_value', ''))
# --- セッション状態の初期化 ---
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'target_word' not in st.session_state:
    st.session_state.target_word = "streamlit"
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# --- タイトル・UI ---
st.title("⌨️ TypingResonator")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Practice")
    target = st.session_state.target_word
    st.info(f"Type this: **{target}**")

    # 入力フォーム（Enterで確定）
    # スマホ入力でもバグりにくいよう、確定時に処理を走らせます
    user_input = st.text_input("Input:", key="typing_box")

    if user_input:
        end_time = time.time()
        duration = end_time - st.session_state.start_time
        
        # 1文字あたりの平均速度を計算
        latency = duration / len(target) if len(target) > 0 else 0
        is_correct = (user_input == target)

        # ログに記録（各文字について正確性と速度を保存）
        for char in target:
            st.session_state.logs.append({
                "key": char,
                "latency": latency,
                "is_error": not is_correct
            })

        if is_correct:
            st.success(f"Excellent! ({duration:.2f}s)")
            # 苦手キーを分析
            weak_keys = get_weak_keys(st.session_state.logs)
            # 次の問題をセット
            st.session_state.target_word = generate_problem(weak_keys)
            st.session_state.start_time = time.time()
            
            # --- ここが修正ポイント ---
            # 直接 typing_box をいじるのではなく、valueに渡している変数を空にする
            st.session_state['typing_box_value'] = ''
            st.rerun()


        else:
            st.error("Miss! Try exactly the same word.")

with col2:
    st.subheader("Real-time Analysis")
    if st.session_state.logs:
        df = pd.DataFrame(st.session_state.logs)
        
        # キーごとの統計
        stats = df.groupby('key').agg({'latency': 'mean', 'is_error': 'mean'}).reset_index()
        
        # 苦手度スコアの可視化 (速度とミス率を掛け合わせる)
        stats['Weakness Score'] = stats['latency'] * (1 + stats['is_error'])
        
        fig = px.bar(stats, x='key', y='Weakness Score', 
                     title="Key Weakness (Higher is worse)",
                     color='is_error',
                     color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Start typing to see your data analysis!")

# --- データ詳細 ---
if st.checkbox("Show raw log data"):
    st.table(pd.DataFrame(st.session_state.logs).tail(10))
