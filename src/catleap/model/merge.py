import pandas as pd

# 2つのCSVファイルを読み込む
df1 = pd.read_csv('./ct_score/CTScore-8.csv')  # ファイル1の読み込み
df2 = pd.read_csv('./feature/CT8-19.csv')  # ファイル2の読み込み
df2 = df2.drop(columns=['Class'])

# 'UserName'列をキーにして2つのDataFrameを結合
merged_df = df2.merge(df1, on='UserName')
merged_df = merged_df.drop(columns=['Unnamed: 0'])
# 新しいCSVファイルに保存
merged_df.to_csv('./feature/merged_19.csv', index=False)