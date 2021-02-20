import random
from time import sleep

# 初期設定 #
player_hp = 10              # プレイヤー初期HP
beacon_pop_rate = [0,1,1]   # ビーコン出現率1/3  Ex: [0,1] - 1/2
monster_lv = [[1,3], [3,9]] # モンスターレベル Ex: [[stage1最低, stage1最高], [stage2最低, stage2最高]]

#   変数名        説明
#   ent          モンスターのレベル
#   player_hp    プレイヤーのHP
#   starge_turn  総ターン数
#   stage_map    HPビーコンやモンスターの配置マップ
#   stage_level  ステージのレベル. stage1 - int(0), stage2 - int(1)
#   monster_lv   モンスターのレベル. ステージによって変化する.
#
#   関数名            引数           説明
#   console_clear()  None           ターミナルの出力結果を初期化する.
#   HPBeacon()       player_hp, p   HPビーコンの関数. 引数のplayer_hpには現在のHP, pには確率モード(1,2,3)を指定する.
#   

OS = 1
stage_turn = 0 # Stage turn
stage_map  = [] # Stage map
_player_hp = 0

# 実行環境検出
console_clear_st = True
try: from google.colab import output
except ImportError:
    console_clear_st = False
    import os
    OS = 2

def toem(n): # 半角数字から全角数字に変換する
    num = ["０","１","２","３","４","５","６","７","８","９"]
    em = ""
    for i in str(n):
        em += num[int(i)]
    return em

mdata = []
class Screen:
    BD = [0,
        ["┏","┓","┗","┛","━","┃","┃"],     # Google Colaboratory
        ["┏━","━┓","┗━","━┛","━━","┃ "," ┃"] # Windows, Linux
    ]
    def __init__(self):
        self.L = []

    def SET_WINDOW(self, width=50, height=5, os=1):  # width - スクリーン横幅
        self.width = width                           # os - 1 [Google Colaboratory], 2 [Windows] [Linux]
        self.height = height
        self.os = os
        BD = self.BD
        # ウィンドウのリストを作成
        for _ in range(height):
            self.L.append(["  " for x in range(width)])
        
        for i in range(height):
            # 上部の角
            if i == 0:
                self.L[0][0]       = BD[os][0]
                self.L[0][width-1] = BD[os][1]
                continue
            # 下部の角
            if i == len(self.L)-1:
                self.L[len(self.L)-1][0]       = BD[os][2]
                self.L[len(self.L)-1][width-1] = BD[os][3]
                continue
            # 左右の縦線
            self.L[i][0]       = BD[os][5]
            self.L[i][width-1] = BD[os][6]
        # 上部と下部の線
        for i in range(width):
            if i != 0 and i != width-1:
                self.L[0][i]             = BD[os][4] # top border
                self.L[len(self.L)-1][i] = BD[os][4] # bottom border
    
    def SET_TEXT_CENTER(self, msg="Ｍｅｓｓａｇｅ．", row=False):
        width = self.width
        height = self.height
        if not row:
            c_height = int(height / 2)-1 # 縦中央　自動設定
        else: 
            c_height = row # 個人設定
        b_len = int((width - len(msg)) / 2)
        for i in range(width):
            x = i - b_len - 1
            if i > b_len and x < len(msg):
                self.L[c_height][i] = msg[x]

    def SET_TEXT(self, msg="Ｍｅｓｓａｇｅ．", row=False, col=False, position="top,left"):
        #   arguments
        #   msg      - 全角の文字を指定する.
        #   row      - 文字の縦の位置. 1 ~ max-width. 左寄せのみ.
        #   position - 文字の位置. [top] [center] [bottom] [right] [left] 2つ指定
        #              例）position="center,left"
        #   rowはpositionより優先
        width = self.width
        height = self.height
        position = position.split(",")
        if not row:
            if "top"    == position[0]: row = 1
            if "center" == position[0]: row = int(height / 2)
            if "bottom" == position[0]: row = height-2
        if not col:
            if "left"   == position[1]: col = 1
            if "right"  == position[1]: col = width - len(msg)-1
        
        x = 0
        for h in range(height):
            if h < row: continue
            if h == height-1: break
            for c in range(width):
                if c < col: continue
                if c == width-1: break # 終端
                if x >= len(msg): break
                self.L[h][c] = msg[x]
                x += 1
        return True

    def SET_MONSTER(self, model, col):
        model_heigh = len(model)
        width = self.width
        height = self.height
        mrow = 0
        for h in range(height):
            if h < height-1-model_heigh: continue # 地に足つける
            if h == height-1: break
            mw = 0
            for d in range(width):
                if d <= col: continue
                if d == width-1: break # 終端
                if mw == len(model[mrow]): break
                self.L[h][d] = model[mrow][mw]
                mw += 1
            mrow += 1


    def CLEAR_WINDOW(self):
        width = self.width
        height = self.height
        os = self.os
        BD = self.BD
        for h in range(height):
            if h == height-1: break
            for w in range(width):
                if 0 == w: continue
                if w == width-1: break
                if 0 == h:
                    self.L[h][w] = BD[os][4] # top border
                else:
                    self.L[h][w] = "  "
        return False

    def WINDOW(self, data=False): # 出力
        if data: L = data
        else: L = self.L
        for line in L:
            for raw in line:
                print(raw, end="")
            print()

def console_clear():
    if console_clear_st: output.clear()
    else: os.system("cls")

def hp_graphics(player_hp):
    global _player_hp
    if player_hp < _player_hp: hp_graphics_list = ['♥ ' if i < player_hp else '♡ ' for i in range(_player_hp)]
    else: hp_graphics_list = ['♥ ' for i in range(player_hp)]
    _player_hp = player_hp
    return hp_graphics_list

def HPBeacon(player_hp, p): # inum - 入力した数, p - 確率 1 2 3
    hp_add = player_hp
    print("> 0~9の数字を入力>")
    inum = int(random.randint(0,9))   # テスト用自動生成 #
    rnum = [i for i in range(10)]
    random.shuffle(rnum)              # 確率1/1
    if 1 == p: 
        rnum = [rnum[0]]              # 確率1/10
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

s = Screen()
s.SET_WINDOW(width=40, height=18, os=OS) # ウィンドウ作成
console_clear()

# スプラッシュ画面
s.SET_TEXT_CENTER("Ｒｕｎｎｉｎｇ　Ｄｉｎｏｓａｕｒｓ", row=7)
s.SET_TEXT_CENTER("受け身は最大の攻撃である！", row=9)
s.SET_TEXT_CENTER("エンターを押してください。", row=15)
s.WINDOW()
input()
console_clear()
s.CLEAR_WINDOW()

# ステージ選択画面
s.SET_TEXT_CENTER("Ｒｕｎｎｉｎｇ　Ｄｉｎｏｓａｕｒｓ", row=7)
s.SET_TEXT_CENTER("１　－　ステージ１", row=9)
s.SET_TEXT_CENTER("２　－　ステージ２", row=10)
s.SET_TEXT_CENTER("ステージを選択してください。", row=15)
s.WINDOW()
stage_level = int(input("数字を入力 >"))-1
console_clear()
s.CLEAR_WINDOW()

# 初期HPビーコン
print("> 冒険を始める前に、HPビーコンをドロップできます。")
player_hp = HPBeacon(player_hp, 1)
print("Player HP:",player_hp)

print("> 冒険開始")
while 0 < player_hp:
    stage_map = [random.randint(monster_lv[stage_level][0], monster_lv[stage_level][1])*random.choice(beacon_pop_rate) for i in range(10)] # マップの生成
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