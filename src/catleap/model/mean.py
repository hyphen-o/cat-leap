import json
import statistics

with open("./prediction_result_no-remix.md", "w") as f:
    f.write("# 説明変数：獲得回数" + "\n")
    f.write("| | 適合率 | 再現率 | F1値 |" + "\n")
    f.write("| :-- | --: | --: | --: |" + "\n")
    # jsonの読み込み
    json_open = open("./exp_binary/[RESULT_NOT-REMIX]skf_CTScore-8.json", "r")
    json_load = json.load(json_open)

    # 精度の平均値を算出
    precision = round(
        statistics.mean([jl["precision"] for jl in json_load["score"]]), 2
    )
    recall = round(
        statistics.mean([jl["recall"] for jl in json_load["score"]]), 2
    )
    f1 = round(statistics.mean([jl["f1"] for jl in json_load["score"]]), 2)

    json_open = open("./exp_binary/[RESULT_NOT-REMIX]skf_CTScore-15.json", "r")
    json_load = json.load(json_open)

    # 精度の平均値を算出
    precision1 = round(
        statistics.mean([jl["precision"] for jl in json_load["score"]]), 2
    )
    recall1 = round(
        statistics.mean([jl["recall"] for jl in json_load["score"]]), 2
    )
    f11 = round(statistics.mean([jl["f1"] for jl in json_load["score"]]), 2)

    f.write(
        "| CTScore-{} | {} | {} | {} |".format(8, precision, recall, f1)
        + "\n"
    )
    f.write(
        "| CTScore-{} | {} | {} | {} |".format(15, precision1, recall1, f11)
        + "\n"
    )