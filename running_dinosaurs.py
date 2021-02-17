import random
from time import sleep

# 実行環境検出
console_clear_st = True
try: from google.colab import output
except ImportError:
    console_clear_st = False
    import os
def console_clear():
    if console_clear_st: output.clear()
    else: os.system("cls")

player_hp = 0

input("[ running dinosaurs ]\npress Enter.") # スプラッシュ画面
console_clear()
stage_level = int(input("- stage level -\n1 - stage1\n2 - stage2\nchoose>"))
console_clear()
hp_beacon = int(input("- HPビーコン -\n0~9の数字を入力>"))

if stage_level == 1:
    random.randint(0,9)
if stage_level == 2: