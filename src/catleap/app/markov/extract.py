import pandas as pd

# Load the CSV files into dataframes
for i in range(1, 19):
  # Load the CSV files into dataframes
  df_A = pd.read_csv(f'users/{i}-dtom.csv')
  df_B = pd.read_csv('CTScore-8.csv')

  # Ensure the data is sorted by UserName
  df_A.sort_values(by='UserName', inplace=True)
  df_B.sort_values(by='UserName', inplace=True)

  # Compare predictions: Correct prediction is when Class == PredClass
  correct_A = df_A[df_A['Class'] == df_A['PredClass']]
  correct_B = df_B[df_B['Class'] == df_B['PredClass']]

  # Identify users that are only in one dataframe but not the other
  only_in_A = correct_A[~correct_A['UserName'].isin(df_B['UserName'])]
  only_in_B = correct_B[~correct_B['UserName'].isin(df_A['UserName'])]

  # Identify users that are in both dataframes
  in_both = correct_A[correct_A['UserName'].isin(df_B['UserName'])]

  # Find users in both dataframes but correct only in A
  only_correct_in_A = in_both[~in_both['UserName'].isin(correct_B['UserName'])]

  # Find users in both dataframes but correct only in B
  correct_in_B = correct_B[correct_B['UserName'].isin(df_A['UserName'])]
  only_correct_in_B = correct_in_B[~correct_in_B['UserName'].isin(correct_A['UserName'])]

  # Combine the results
  only_correct_in_A_total = pd.concat([only_in_A, only_correct_in_A])
  only_correct_in_B_total = pd.concat([only_in_B, only_correct_in_B])

  # Save the results to separate CSV files
  only_correct_in_A_total.to_csv(f'{i}_only_correct_in_A_dtom.csv', index=False)
  only_correct_in_B_total.to_csv(f'{i}_only_correct_in_B_dtom.csv', index=False)

  print("Outputs saved to 'only_correct_in_A.csv' and 'only_correct_in_B.csv'")