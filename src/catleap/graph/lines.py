
import matplotlib.pyplot as plt
import numpy as np
import japanize_matplotlib

def draw_lines(props):
  """props = {
          x: list,
          y1: list,
          y2: list,
          y3: list,
          xlabel : str,
          ylabel : str,
          title: str
          file_name: str
    }"""
  
  # 3本の折れ線グラフを異なる色で描画
  plt.figure(figsize=(10, 5))
  plt.plot(props.x, props.y1, '-r', label='適合率') 
  plt.plot(props.x, props.y2, '-g', label='再現率') 
  plt.plot(props.x, props.y3, '-b', label='F1値') 

  plt.xticks(np.arange(0, 20, 1))

  # グラフのタイトルと軸ラベルを設定
  plt.xlabel('作品数')
  plt.ylabel('スコア')

  # 凡例を表示
  plt.legend()

  # y軸の表示範囲を制限してtan(x)の急激な変動を抑える
  plt.ylim(0, 1.0)
  plt.tight_layout()
  plt.savefig(props.file_name)
