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

def HPBeacon(player_hp, p): # inum - 入力した数, p - 確率 1 2 3
    hp_add = player_hp
    print("> 0~9の数字を入力>")
    inum = int(random.randint(0,9)) # テスト用自動生成 #
    rnum = [i for i in range(10)]
    random.shuffle(rnum) # 確率1/1
    if 1 == p: 
        rnum = [rnum[0]] # 確率1/10
        hp_add += 10
    if 2 == p: 
        rnum = random.sample(rnum, 2) # 確率1/5
        hp_add += 5
    if 3 == p: 
        rnum = random.sample(rnum, 5) # 確率1/2
        hp_add += 3
    if 4 == p: hp_add += 1
    print(f" あなた\tコンピューター\n {inum}\t{rnum}")
    if inum in rnum:
        print("> 勝利！")
        return hp_add
    else:
        print("> 敗北...")
        return HPBeacon(player_hp, p+1)

# 初期設定 #
player_hp = 10 # プレイヤー初期HP
beacon_pop_rate = [0,1,1] # ビーコン出現率1/3  [0,1] - 1/2
monster_lv = [[2,6], [3,9]] # モンスターレベル [[stage1最低, stage1最高], [stage2最低, stage2最高]]
stage_turn = 0 # Stage turn
stage_map = [] # Stage map

console_clear()
input("[ running dinosaurs ]\npress Enter.") # スプラッシュ画面
console_clear()
stage_level = int(input("- stage level -\n1 - stage1\n2 - stage2\nchoose>"))
console_clear()

# ====================== 初期HPビーコン ====================== #
print("> はじめに、HPビーコンを使ってください。")
player_hp = HPBeacon(player_hp, 1)
print("Player HP:",player_hp)

print("> 冒険開始")
while 0 < player_hp:
    stage_map = [random.randint(monster_lv[0][0], monster_lv[0][1])*random.choice(beacon_pop_rate) for i in range(10)] # マップの生成
    print("Stage map",stage_map)
    for ent in stage_map:
        if 0 >= player_hp: break
        if ent:
            print("> モンスター出現！　レベル：",ent)
            player_hp -= ent
        else:
            print("> HPビーコン発見！")
            player_hp = HPBeacon(player_hp, 1)
            print("Player HP:",player_hp)
        stage_turn += 1

print("> ゴール！")
print("> スコア:",stage_turn)