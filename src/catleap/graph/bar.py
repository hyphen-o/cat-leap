import matplotlib.pyplot as plt
import japanize_matplotlib


def draw_bar(x: list, y: list):
    # 棒グラフの描画
    plt.bar(x, y, color="blue")

    # グラフの装飾
    plt.xlabel("重複数")
    plt.ylabel("出現回数")
    plt.title("DEVELOPINGからMASTER")
    plt.grid(True)

    # グラフの表示
    plt.savefig("DEV_TO_MAS_dup.png")
