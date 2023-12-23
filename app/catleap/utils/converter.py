import csv
import json
import pandas as pd


def json_to_csv(input_path: str, output_path: str):
    # CSVファイルの読み込み
    with open(input_path, "r") as f:
        d_reader = csv.DictReader(f)
        d_list = [row for row in d_reader]
        print(d_list)

    # JSONファイルへの書き込み
    with open(output_path, "w") as f:
        json.dump(d_list, f)


def group_by_colname(data: pd.DataFrame, col_name: str):
    return data.groupby(col_name).apply(lambda group: group.values.tolist()).to_list()
