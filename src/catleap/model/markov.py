from collections import defaultdict
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import precision_recall_fscore_support

def count_transitions(sequence, n):
    transitions = defaultdict(lambda: defaultdict(int))
    for i in range(len(sequence) - n):
        current_state = tuple(sequence[i:i+n])
        next_state = sequence[i+n]
        transitions[current_state][next_state] += 1
    return transitions

def predict_next_state(transitions, current_state):
    next_states = transitions.get(tuple(current_state), {})
    if not next_states:
        return None
    return max(next_states, key=next_states.get)

def train_on_sequences(sequences, n):
    all_transitions = []
    for sequence in sequences:
        transitions = count_transitions(sequence, n)
        all_transitions.append(transitions)
    return all_transitions

# 複数のシーケンス
sequences = [
    [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0],
    [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0],
    [2, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1]
]

# nを2に設定して学習
transitions_list = train_on_sequences(sequences, 2)

# 各シーケンスの遷移表を表示（例として最初のもののみ）
print(transitions_list[0])

# 特定の状態に基づいて次の状態を予測
current_state = [1, 2]
predicted_next_state = predict_next_state(transitions_list[0], current_state)
print("Predicted next state for [1, 2]:", predicted_next_state)

def evaluate_model(sequence, n, transitions):
    y_true = []
    y_pred = []
    
    for i in range(len(sequence) - n):
        current_state = sequence[i:i+n]
        true_next_state = sequence[i+n]
        predicted_state = predict_next_state(transitions, current_state)
        
        y_true.append(true_next_state)
        y_pred.append(predicted_state if predicted_state is not None else -1)  # 使用されていない状態の予測のために特別な処理
    
    precision, recall, f1_score, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    return precision, recall, f1_score

# 2000個のデータポイントからなるシーケンス
np.random.seed(0)
sequence = np.random.randint(0, 10, 2000)  # 仮に0から9までの整数値

# 交差検証を通じて各スコアを計算
kf = KFold(n_splits=10)
precisions, recalls, f1_scores = [], [], []

for train_index, test_index in kf.split(sequence):
    train_seq = sequence[train_index]
    test_seq = sequence[test_index]
    transitions = count_transitions(train_seq, 2)
    precision, recall, f1 = evaluate_model(test_seq, 2, transitions)
    
    precisions.append(precision)
    recalls.append(recall)
    f1_scores.append(f1)

# 各指標の平均を出力
print("Average Precision:", np.mean(precisions))
print("Average Recall:", np.mean(recalls))
print("Average F1 Score:", np.mean(f1_scores))

