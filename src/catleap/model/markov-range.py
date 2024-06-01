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
    # print(transitions)
    return transitions


json_file = open(path.BAS_TO_DEV + "out-all.json", "r")
bas_to_dev = json.load(json_file)

user_names = []
sequences = []
for user in bas_to_dev:
    user_names.append(user["USER_NAME"])
    tmp = []
    for mile in user["MILES"]:
        tmp.append(mile["Before"]["Feature"])
    sequences.append(tmp)


def check_type(score: int):
    if score < 8:
        return "BASIC"
    elif score >= 8 and score < 15:
        return "DEVELOPING"
    else:
        return "MASTER"


# 二段目の値が1以下の要素を取り除く関数
def remove_low_values(d):
    for key, nested_dict in d.items():
        if isinstance(nested_dict, dict):
            keys_to_remove = [k for k, v in nested_dict.items() if v <= 0]
            for k in keys_to_remove:
                del nested_dict[k]


def evaluate_model(sequences, n, transitions, fold_num):
    try:
        y_true = []
        y_pred = []

        for sequence in sequences:

            current_state = str(sequence[len(sequence) - 3 : len(sequence) - 2])
            true_next_state = str(sequence[len(sequence) - 1])
            predicted_state = predict_next_state(transitions, current_state)

            if predicted_state is not None:
                # if (
                #     sum(eval(predicted_state)) <= sum(eval(true_next_state)) + 3
                #     and sum(eval(predicted_state)) >= sum(eval(true_next_state)) - 3
                # ):
                #     predicted_state = true_next_state
                true_next_state = check_type(sum(eval(true_next_state)))
                predicted_state = check_type(sum(eval(predicted_state)))
                # for true in true_next_states:
                #     if predicted_state is not None:
                #         if sum(eval(predicted_state)) == sum(true):
                #             true_next_state = str(true)

                y_true.append(true_next_state)
                y_pred.append(
                    predicted_state if predicted_state is not None else ""
                )  # 使用されていない状態の予測のために特別な処理
        print(y_pred)
        if not y_true or not y_pred:
            # print(sequences)
            return (None, None, None)
        true_count = 0
        if fold_num == 10:
            predictions = []
            for user_name, predict, true in zip(user_names, y_pred, y_true):
                prediction_dict = {
                    "USER_NAME": "",
                    "PREDICT": 0,
                    "PREDICT_STATE": predict,
                    "TRUE_STATE": true,
                }
                prediction_dict["USER_NAME"] = user_name
                if predict == true:
                    prediction_dict["PREDICT"] = 1
                    true_count += 1

                predictions.append(prediction_dict)
            with open(
                path.BAS_TO_DEV + f"predictions/{n}-b-to-d-either.json", "w"
            ) as f:
                json.dump(predictions, f)
        

        # precision, recall, f1_score, _ = precision_recall_fscore_support(
        #     y_true, y_pred, average="macro", zero_division=0
        # )

        print(true_count)
        print(len(y_pred))
        precision = true_count / len(y_pred)

        return precision
    except Exception as e:
        print(e)


# 交差検証
kf = KFold(n_splits=10)
precisions, recalls, f1_scores = [], [], []
for index, (train_index, test_index) in enumerate(kf.split(sequences)):
    train_seq = [sequences[i] for i in train_index]
    test_seq = [sequences[i] for i in test_index]
    transitions = train_on_sequences(train_seq, 1)
    remove_low_values(transitions)
    precision = evaluate_model(test_seq, 1, transitions, index + 1)
    if precision is not None:
        precisions.append(precision)
    if index == 9:
        # 各指標の平均を出力∆
        print("Average Precision:", precision)
