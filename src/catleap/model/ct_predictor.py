# ライブラリの読み込み
import pandas as pd
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
import json
import statistics
import os
from tqdm import tqdm


def binary_classify(df):
    """
    2つの結果を返却する
    1. クラスデータ：実測値と予測値の列を含む
    2. 実行結果のデータ：予測精度と重要度
    """

    rfc = RandomForestClassifier(
        max_features="sqrt",  # 使用する説明変数の個数は特徴量の個数の平方根
        n_estimators=200,  # 作成する木の数
        random_state=42,  # 乱数の設定
        class_weight="balanced",  # 不均衡への対応
    )

    # StratifiedKFoldについて
    # 参考：https://qiita.com/chorome/items/54e99093050a9473a189
    skf = StratifiedKFold(
        n_splits=10, random_state=42, shuffle=True  # 10分割交差検証  # 乱数の設定  # データを選択方法はランダム
    )

    X = df.iloc[:, :-1]  # 説明変数の列
    y = df.iloc[:, -1]  # 目的変数の列

    class_results = []
    dict_pred_results = dict()
    dict_pred_results["score"] = []
    dict_pred_results["importance"] = []

    for train_i, test_i in skf.split(X, y):
        # 訓練データの抽出
        X_train, y_train = X.iloc[train_i], y.iloc[train_i]

        # 検証データの抽出
        X_test, y_test = X.iloc[test_i], y.iloc[test_i]

        # モデルの学習
        rfc.fit(X_train, y_train)

        # 二値分類の実行
        y_pred = rfc.predict(X_test)

        # 結果を記録
        y_pred = pd.Series(y_pred, index=y_test.index, name="PredClass")
        class_results.append(pd.concat([y_test, y_pred], axis=1))

        # 予測精度を記録
        dict_score = dict()
        dict_score["precision"] = precision_score(y_test, y_pred)
        dict_score["recall"] = recall_score(y_test, y_pred)
        dict_score["f1"] = f1_score(y_test, y_pred, zero_division=0.0)
        dict_pred_results["score"].append(dict_score)

        # 説明変数の重要度を記録
        dict_importance = dict()
        for val, score in zip(list(X_train.columns), list(rfc.feature_importances_)):
            dict_importance[val] = score
        dict_pred_results["importance"].append(dict_importance)

    class_results = pd.concat(class_results)

    return class_results, dict_pred_results


def convert_binary_data(df):
    """
    説明変数の値を0，1に変換する
    """

    for i in range(0, len(df.columns) - 1):
        df.iloc[:, i] = df.iloc[:, i].apply(lambda x: 1 if x > 0 else 0)

    return df


if __name__ == "__main__":
    # ==========================================================
    # 実行箇所
    # - 1ループ目：獲得回数
    # - 2ループ目：獲得有無
    # ==========================================================
    for i in range(1, 20):
        for path in ["./exp_count/", "./exp_binary/"]:
            os.makedirs(path, exist_ok=True)
            for ctscore in [8]:
                #  データの読み込みとモデルの実行
                df = pd.read_csv(
                    "./feature/CT{}-{}.csv".format(ctscore, i), index_col=["UserName"]
                )
                if "binary" in path:
                    # df = convert_binary_data(df)
                    break

                class_results, dict_pred_results = binary_classify(df)

                # ファイル出力
                class_results.to_csv(
                    path + "[RESULT]class_CTScore-{}_{}.csv".format(ctscore, i),
                    index=True,
                )
                with open(
                    path + "[RESULT]skf_CTScore-{}_{}.json".format(ctscore, i), "w"
                ) as f:
                    f.write(json.dumps(dict_pred_results, indent=4))

        # ==========================================================
        # 予測精度の出力
        # ==========================================================
        with open(f"./prediction_result_{i}.md", "w") as f:
            for path in ["./exp_count/"]:
                caption = "# 説明変数：獲得回数" if "count" in path else "# 説明変数：獲得経験"
                f.write(caption + "\n")
                f.write("| | 適合率 | 再現率 | F1値 |" + "\n")
                f.write("| :-- | --: | --: | --: |" + "\n")

                for cs in ["8", "15"]:
                    # jsonの読み込み
                    json_open = open(
                        path + "[RESULT]skf_CTScore-" + cs + f"_{i}.json", "r"
                    )
                    json_load = json.load(json_open)

                    # 精度の平均値を算出
                    precision = round(
                        statistics.mean([jl["precision"] for jl in json_load["score"]]),
                        2,
                    )
                    recall = round(
                        statistics.mean([jl["recall"] for jl in json_load["score"]]), 2
                    )
                    f1 = round(
                        statistics.mean([jl["f1"] for jl in json_load["score"]]), 2
                    )

                    f.write(
                        "| CTScore-{} | {} | {} | {} |".format(
                            cs, precision, recall, f1
                        )
                        + "\n"
                    )

                f.write("\n")
