import sys
import shutil

def zipper(dir_path: str, name: str):
  shutil.make_archive(name, "zip", root_dir=dir_path)


if __name__ == "__main__":
  args = sys.argv
  if len(args) < 3:
    print("コマンドライン引数の数が足りていません．")
  zipper(args[1], args[2])


