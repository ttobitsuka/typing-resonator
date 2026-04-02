import pandas as pd

def get_weak_keys(logs):
    if not logs:
        return []
    
    df = pd.DataFrame(logs)
    
    # キーごとの統計（平均遅延時間とミス率）を算出
    stats = df.groupby('key').agg({
        'latency': 'mean',
        'is_error': 'mean'
    })
    
    # 全体の平均遅延時間を計算
    overall_avg_latency = df['latency'].mean()
    
    # 【独自定義】平均より20%以上遅い、またはミス率が10%以上のキーを「苦手」とする
    weak_condition = (stats['latency'] > overall_avg_latency * 1.2) | (stats['is_error'] > 0.1)
    weak_keys = stats[weak_condition].index.tolist()
    
    return weak_keys
