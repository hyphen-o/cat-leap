from collections import defaultdict
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import precision_recall_fscore_support
import sys
import json

sys.path.append("../")
from constants import path


def count_transitions(sequence, n):
    transitions = defaultdict(lambda: defaultdict(int))
    for i in range(len(sequence) - n):
        current_state = tuple(map(str, sequence[i : i + n]))
        next_state = str(sequence[i + n])
        print("current_state:", current_state)
        print("next_state:", next_state)
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
    print(all_transitions)
    with open("sam.json", "w") as f:
        json.dump(all_transitions, f, indent=2)

    return all_transitions


# 複数のシーケンス

json_file = open(path.BAS_TO_DEV + "out.json", "r")
json_file2 = open(path.DEV_TO_MAS + "duplication-not-target.json", "r")
bas_to_dev = json.load(json_file)

sequences = []
for user in bas_to_dev:
    tmp = []
    for mile in user["MILES"]:
        tmp.append(mile["Before"]["Feature"])
    sequences.append(tmp)

# nを2に設定して学習
transitions_list = train_on_sequences(sequences, 2)

# current_state = [1, 2]
# predicted_next_state = predict_next_state(transitions_list[0], current_state)
# print("Predicted next state for [1, 2]:", predicted_next_state)


def evaluate_model(sequence, n, transitions):
    y_true = []
    y_pred = []

    for i in range(len(sequence) - n):
        current_state = tuple(map(str, sequence[i : i + n]))
        true_next_state = str(sequence[i + n])
        predicted_state = predict_next_state(transitions, current_state)

        y_true.append(str(true_next_state))
        y_pred.append(
            str(predicted_state) if predicted_state is not None else ""
        )  # 使用されていない状態の予測のために特別な処理

    precision, recall, f1_score, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro"
    )
    return precision, recall, f1_score


# 交差検証
kf = KFold(n_splits=10)
precisions, recalls, f1_scores = [], [], []

for train_index, test_index in kf.split(sequences):
    print(train_index)
    train_seq = [sequences[i] for i in train_index]
    test_seq = [sequences[i] for i in test_index]
    print(train_seq)
    transitions = count_transitions(train_seq, 2)
    precision, recall, f1 = evaluate_model(test_seq, 2, transitions)

    precisions.append(precision)
    recalls.append(recall)
    f1_scores.append(f1)

# 各指標の平均を出力∆
print("Average Precision:", np.mean(precisions))
print("Average Recall:", np.mean(recalls))
print("Average F1 Score:", np.mean(f1_scores))
