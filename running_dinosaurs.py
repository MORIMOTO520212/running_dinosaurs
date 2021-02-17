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

def HPBeacon(inum): # HP Beacon
    randint = random.randint(0,9)
    if inum == randint:
        if not inum: inum = 1
        return [inum, randint, True]
    else: return [inum, randint, False]

player_hp = 10 # Player HP
stage_turn = 0 # Stage turn
stage_map = [] # Stage map
console_clear()
input("[ running dinosaurs ]\npress Enter.") # スプラッシュ画面
console_clear()
stage_level = int(input("- stage level -\n1 - stage1\n2 - stage2\nchoose>"))
console_clear()

# ====================== 初期HPビーコン ====================== #
ires = HPBeacon(int(input("- 初期HPビーコン -\n0~9の数字を入力>")))
print(f"あなた\tコンピューター\n{ires[0]}\t{ires[1]}")
if ires[2]:
    print("> 勝利！")
    player_hp = (stage_level * 10) * (ires[0] + 1)
else: print("> 敗北...")
print("Player HP:",player_hp)


print("> 冒険開始")
while 0 < player_hp:
    stage_map = [1*random.randint(0,3)*random.randint(0,1) for i in range(10)] # マップの生成
    print("Stage map",stage_map)
    for ent in stage_map:
        if 0 >= player_hp: break
        if ent:
            print("> モンスター出現！　レベル：",ent)
            player_hp -= ent
        else:
            print("> HPビーコン発見")
            inp = random.randint(0,9) # テスト用自動入力
            print("0~9の数字を入力>",inp)
            ires = HPBeacon(inp)
            print(f"あなた\tコンピューター\n{ires[0]}\t{ires[1]}")
            if ires[2]:
                print("> 勝利！")
                player_hp = (stage_level * 10) * (ires[0] + 1)
            else: print("> 敗北...")
            print("Player HP:",player_hp)
        stage_turn += 1

print("> ゴール！")
print("> スコア:",stage_turn)