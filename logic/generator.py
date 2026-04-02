import random

def generate_problem(weak_keys):
    # 基本の単語リスト（本来はjson等から読み込むのが理想）
    default_words = ["python", "streamlit", "github", "typing", "logic", "data"]
    
    if not weak_keys:
        return random.choice(default_words)
    
    # 苦手キーが含まれている単語を優先的に選ぶ
    priority_words = [w for w in default_words if any(k in w for k in weak_keys)]
    
    if priority_words:
        return random.choice(priority_words)
    else:
        # 苦手キーが含まれる単語がリストにない場合、苦手キーを組み合わせた練習文字列を作る
        return "".join(random.choices(weak_keys, k=5))
