import matplotlib.pyplot as plt

def draw_acccumlate(props):
  """props = {
          x: list,
          precision: list,
          recall: list,
          f1: list,
          y2: list,
          y3: list,
          y4: list,
          xlabel : str,
          ylabel : str,
          title: str
          file_name: str
    }"""

  fig, ax1 = plt.subplots(figsize=(10, 6))


  # 左の軸に折れ線グラフを描画
  ax1.set_xlabel('N', fontsize=16)
  ax1.set_ylabel('スコア', color='black', fontsize=16)
  ax1.plot(props["x"], props["precision"], color='tab:red')
  ax1.plot(props["x"], props["recall"], color='tab:green',)
  ax1.plot(props["x"], props["f1"], color='tab:blue')
  ax1.tick_params(axis='y', labelcolor='black', labelsize=14)
  ax1.set_ylim(0, 1.1)
  ax1.set_xticks(props["x"])
  ax1.set_xticklabels(props["x"], fontsize=14)

  # 右の軸に積み上げ棒グラフを描画
  ax2 = ax1.twinx()  # 共有するX軸を作成
  ax2.set_ylabel('ユーザ数', color='black', fontsize=16)
  ax2.bar(props["x"], props["y3"], color='tab:orange', alpha=0.6)
  ax2.bar(props["x"],  props["y4"], bottom=props["y3"], color='tab:blue', alpha=0.6)
  ax2.bar(props["x"],  props["y2"], bottom=props["y3"] + props["y4"], color='gray', alpha=0.4)
  ax2.tick_params(axis='y', labelcolor='black', labelsize=14)

  # グラフのタイトルと凡例の設定
  fig.tight_layout()
  fig.legend(loc='upper right', bbox_to_anchor=(0.85, 1.01), fontsize=12)
  plt.savefig(props["file_name"])