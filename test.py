import random
player_hp = 10
stage_level = 1

def HPBeacon(player_hp, p): # inum - 入力した数, p - 確率 1 2 3
    hp_add = player_hp
    inum = int(input("> 0~9の数字を入力>"))
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

print("> HPビーコン発見！")
player_hp = HPBeacon(player_hp, 1)
print("player_hp =",player_hp)