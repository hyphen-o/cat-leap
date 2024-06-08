from collections import defaultdict
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
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
    for seq in sequences:
        sequence = seq["SEQUENCE"]
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


json_file = open(path.DEV_TO_MAS + "out-all.json", "r")
bas_to_dev = json.load(json_file)

user_names = []
sequences = []
for user in bas_to_dev:
    user_names.append(user["USER_NAME"])
    tmp = []
    for mile in user["MILES"]:
        tmp.append(mile["Before"]["Feature"])
    sequences.append({
        "USER_NAME": user["USER_NAME"],
        "SEQUENCE": tmp
    })

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
        counts = {
            "all-count": 0,
            "pred-count": 0,
            "correct-count": 0,
            "false-count": 0,
            "user": []
        }

        for seq in sequences:
            user_name = seq["USER_NAME"]
            sequence = seq["SEQUENCE"]

            if len(sequence) < n + 1:
                continue
            current_state = str(sequence[len(sequence) - (n + 2) : len(sequence) - 2])
            if current_state:
                counts["all-count"] += 1
            true_next_state = str(sequence[len(sequence) - 1])
            predicted_state = predict_next_state(transitions, current_state)

            if predicted_state is not None:
                # if (
                #     sum(eval(predicted_state)) <= sum(eval(true_next_state)) + 3
                #     and sum(eval(predicted_state)) >= sum(eval(true_next_state)) - 3
                # ):
                #     predicted_state = true_next_state
                true_next_state = 1 if sum(eval(true_next_state)) >= 15 else 0
                predicted_state = 1 if sum(eval(predicted_state)) >= 15 else 0
                # for true in true_next_states:
                #     if predicted_state is not None:
                #         if sum(eval(predicted_state)) == sum(true):
                #             true_next_state = str(true)

                counts["user"].append({
                    "USER_NAME": user_name,
                    "PREDICT": 1 if predicted_state == true_next_state else 0,
                    "PREDICT_STATE": predicted_state,
                    "TRUE_STATE": true_next_state
                })

                y_true.append(true_next_state)
                y_pred.append(
                    predicted_state if predicted_state is not None else ""
                )  # 使用されていない状態の予測のために特別な処理
        if not y_true or not y_pred:
            # print(sequences)
            return None, None, None, None
        true_count = 0
        # if fold_num == 10:
        predictions = []
        #     print(len(y_pred))
        #     print(len(y_true))
        counts["pred-count"] = len(y_pred)
        for predict, true in zip(y_pred, y_true):
            prediction_dict = {
                "USER_NAME": "",
                "PREDICT": 0,
                "PREDICT_STATE": predict,
                "TRUE_STATE": true,
            }
            prediction_dict["USER_NAME"] = user_name
            if predict == true:
                counts["correct-count"] += 1
                prediction_dict["PREDICT"] = 1
                true_count += 1

            predictions.append(prediction_dict)
        with open(
            path.BAS_TO_DEV + f"predictions/{n}-d-to-m-either.json", "w"
        ) as f:
            json.dump(predictions, f)
        
        counts["false-count"] = counts["pred-count"] - counts["correct-count"]

        # precision = precision_score(y_true, y_pred)
        # recall = recall_score(y_true, y_pred)
        # f1 = f1_score(y_true, y_pred, zero_division=0.0)

        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average="macro", zero_division=0
        )

        # precision = true_count / len(y_pred)        

        return precision, recall, f1, counts
    except Exception as e:
        print(e)

result = {
    "num": [],
    "precision": [],
    "recall": [],
    "f1": [],
    "all-count": [],
    "correct-count": [],
    "false-count": []
}
# 交差検証
for n in range(1, 19):
    kf = KFold(n_splits=10)
    precisions, recalls, f1_scores = [], [], []
    users = []
    count = 0 
    all_count = 0
    correct_count = 0
    false_count = 0
    for index, (train_index, test_index) in enumerate(kf.split(sequences)):
        train_seq = [sequences[i] for i in train_index]
        test_seq = [sequences[i] for i in test_index]
        transitions = train_on_sequences(train_seq, n)
        remove_low_values(transitions)
        precision,recall, f1, counts = evaluate_model(test_seq, n, transitions, index + 1)
        if counts:
            all_count += counts["all-count"]
            correct_count += counts["correct-count"]
            false_count += counts["false-count"]
            users += counts["user"]
        if precision is not None and recall is not None and f1_score is not None:
            count += 1
            precisions.append(precision)
            recalls.append(recall)
            f1_scores.append(f1)
        if index == 9:
            # 各指標の平均を出力∆
            result["num"].append(n)
            result["precision"].append(sum(precisions) / count)
            result["recall"].append(sum(recalls) / count)
            result["f1"].append(sum(f1_scores) / count)
            result["all-count"].append(all_count)
            result["correct-count"].append(correct_count)
            result["false-count"].append(false_count)
            with open(
                f"../app/markov/users/{n}-dtom.json", "w"
            ) as f:
                json.dump(users, f)
            print(correct_count)
            print(users)
            print(false_count)
            print("Average Precision:", sum(precisions) / count)
            print("Average Precision:", sum(recalls) / count)
            print("Average Precision:", sum(f1_scores) / count)

with open(
    f"../app/markov/markov-d-to-m-binary.json", "w"
) as f:
    json.dump(result, f)