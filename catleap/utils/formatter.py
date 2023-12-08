import csv
import json


def json_to_csv(input_path, output_path):
    # CSVファイルの読み込み
    with open(input_path, "r") as f:
        d_reader = csv.DictReader(f)
        d_list = [row for row in d_reader]
        print(d_list)

    # JSONファイルへの書き込み
    with open(output_path, "w") as f:
        json.dump(d_list, f)
