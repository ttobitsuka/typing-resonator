import streamlit as st
import time
import pandas as pd
import plotly.express as px
from logic.analyzer import get_weak_keys
from logic.generator import generate_problem

st.set_page_config(page_title="TypingResonator", layout="wide")

# --- セッション状態の初期化 ---
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'target_word' not in st.session_state:
    st.session_state.target_word = "streamlit"
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'input_reset' not in st.session_state:
    st.session_state.input_reset = 0

st.title("⌨️ TypingResonator")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Practice")
    target = st.session_state.target_word
    st.info(f"Type this: **{target}**")

    # 入力欄のクリアを確実にするため、keyを動的に変更するテクニックを使います
    input_key = f"typing_box_{st.session_state.input_reset}"
    user_input = st.text_input("Input:", key=input_key)

    if user_input:
        end_time = time.time()
        duration = end_time - st.session_state.start_time
        
        latency = duration / len(target) if len(target) > 0 else 0
        is_correct = (user_input == target)

        if is_correct:
            # ログの記録
            for char in target:
                st.session_state.logs.append({
                    "key": char,
                    "latency": latency,
                    "is_error": False
                })
            st.success(f"Excellent! ({duration:.2f}s)")
            
            # 状態の更新
            weak_keys = get_weak_keys(st.session_state.logs)
            st.session_state.target_word = generate_problem(weak_keys)
            st.session_state.start_time = time.time()
            st.session_state.input_reset += 1  # keyを変えることで入力を強制リセット
            st.rerun()
        else:
            # ミス時のログ
            for char in target:
                st.session_state.logs.append({
                    "key": char,
                    "latency": latency,
                    "is_error": True
                })
            st.error("Miss! Try exactly the same word.")

with col2:
    st.subheader("Real-time Analysis")
    if st.session_state.logs:
        df = pd.DataFrame(st.session_state.logs)
        stats = df.groupby('key').agg({'latency': 'mean', 'is_error': 'mean'}).reset_index()
        stats['Weakness Score'] = stats['latency'] * (1 + stats['is_error'])
        
        fig = px.bar(stats, x='key', y='Weakness Score', 
                     title="Key Weakness Score",
                     color='is_error',
                     color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Start typing to see analysis!")
