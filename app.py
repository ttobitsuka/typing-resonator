import streamlit as st
import time
import pandas as pd
from logic.analyzer import get_weak_keys
from logic.generator import generate_problem

st.set_page_config(page_title="TypingResonator", layout="centered")

# --- Session State の初期化 ---
if 'logs' not in st.session_state:
    st.session_state.logs = []  # 打鍵ログ：{key, latency, is_error}
if 'target_word' not in st.session_state:
    st.session_state.target_word = "streamlit"
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

st.title("⌨️ TypingResonator")
st.subheader("データサイエンスで苦手キーを克服する")

# --- メインロジック ---
target = st.session_state.target_word
st.info(f"Problem: **{target}**")

# 入力フォーム（streamlit-keyup等を使うとよりリアルタイムになりますが、まずは標準機能で）
user_input = st.text_input("Type here and press Enter:", key="typing_input")

if user_input:
    end_time = time.time()
    
    # 簡易的な速度計測（実際には1文字ずつの計測にアップグレード予定）
    duration = end_time - st.session_state.start_time if st.session_state.start_time else 0
    latency_per_char = duration / len(user_input) if len(user_input) > 0 else 0
    
    # 正誤判定
    is_correct = user_input == target
    
    # ログの記録（各キーに対して記録するロジックのプロトタイプ）
    for char in target:
        st.session_state.logs.append({
            "key": char,
            "latency": latency_per_char,
            "is_error": not is_correct
        })
    
    if is_correct:
        st.success("Perfect!")
        # 次の問題へ（ここでgenerator.pyを呼び出す）
        weak_keys = get_weak_keys(st.session_state.logs)
        st.session_state.target_word = generate_problem(weak_keys)
        st.session_state.start_time = time.time()
        st.rerun()
    else:
        st.error("Miss! Try again.")

# --- 分析セクション ---
if st.session_state.logs:
    st.divider()
    st.write("### 📊 Your Weakness Analysis")
    df = pd.DataFrame(st.session_state.logs)
    st.dataframe(df.tail(10)) # 最新のログを表示
