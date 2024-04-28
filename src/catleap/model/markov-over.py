from collections import defaultdict
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import precision_recall_fscore_support
import sys
import json

sys.path.append("../")
from constants import path


# 遷移情報を記録
def count_transitions(sequence, n):
    transitions = {}
    for i in range(len(sequence) - n):
        current_state = str(sequence[i : i + n])
        next_state = str(sequence[i + n])
        if current_state in transitions:
            if next_state in transitions[current_state]:
                transitions[current_state][next_state] += 1
            else:
                transitions[current_state].update({next_state: 1})
        else:
            transitions.update({current_state: {next_state: 1}})
    return transitions


def predict_next_state(transitions, current_state):
    next_states = None
    if current_state in transitions:
        next_states = transitions[current_state]
    if not next_states:
        return None
    return max(next_states.items(), key=lambda x: x[1])[0]


def train_on_sequences(sequences, n):
    transitions = defaultdict(lambda: defaultdict(int))
    for sequence in sequences:
        for i in range(len(sequence) - n):
            current_state = str(sequence[i : i + n])
            next_state = str(sequence[i + n])
            if current_state in transitions:
                if next_state in transitions[current_state]:
                    transitions[current_state][next_state] += 1
                else:
                    transitions[current_state].update({next_state: 1})
            else:
                transitions.update({current_state: {next_state: 1}})
    return transitions


json_file = open(path.BAS_TO_DEV + "out.json", "r")
bas_to_dev = json.load(json_file)

sequences = []
for user in bas_to_dev:
    tmp = []
    for mile in user["MILES"]:
        tmp.append(mile["Before"]["Feature"])
    sequences.append(tmp)


def evaluate_model(sequences, n, transitions):
    y_true = []
    y_pred = []

    for sequence in sequences:
        current_state = str(sequence[len(sequence) - 3 : len(sequence) - 2])
        true_next_state = str(sequence[len(sequence) - 1])

        predicted_state = predict_next_state(transitions, current_state)

        y_true.append(true_next_state)
        y_pred.append(
            predicted_state if predicted_state is not None else ""
        )  # 使用されていない状態の予測のために特別な処理

        for i in range(len(sequence) - n):
            current_state = str(sequence[i : i + n])
            true_next_state = str(sequence[i + n])
            predicted_state = predict_next_state(transitions, current_state)

            y_true.append(true_next_state)
            y_pred.append(
                predicted_state if predicted_state is not None else ""
            )  # 使用されていない状態の予測のために特別な処理

    precision, recall, f1_score, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )
    return precision, recall, f1_score


# 交差検証
kf = KFold(n_splits=10)
precisions, recalls, f1_scores = [], [], []

for train_index, test_index in kf.split(sequences):
    train_seq = [sequences[i] for i in train_index]
    test_seq = [sequences[i] for i in test_index]
    transitions = train_on_sequences(train_seq, 2)
    precision, recall, f1 = evaluate_model(test_seq, 2, transitions)
    precisions.append(precision)
    recalls.append(recall)
    f1_scores.append(f1)

# 各指標の平均を出力∆
print("Average Precision:", np.mean(precisions))
print("Average Recall:", np.mean(recalls))
print("Average F1 Score:", np.mean(f1_scores))
