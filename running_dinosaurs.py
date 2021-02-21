#                  Running Dinosaurs
# ※ cmd.exe, Linux, Visual Studio Codeでのプレイを推奨します。
import random
from time import sleep

# 初期設定 #
player_hp = 10              # プレイヤー初期HP
beacon_pop_rate = [0,1,1]   # ビーコン出現率1/3  Ex: [0,1] - 1/2
monster_lv = [[1,3], [3,6]] # モンスターレベル Ex: [[stage1最低, stage1最高], [stage2最低, stage2最高]]

# platform: 0 - cmd linux, 1 - colab, 2 - vscode
OS = 1
platform = 1
stage_turn = 0
stage_map  = []
_player_hp = 0
kill_count = 0
player_model_num = 0
hp_beacon_msg = ["１回目：＋１０ＨＰ　確率：１／１０", "２回目：＋５ＨＰ　確率：１／５", "３回目：＋３ＨＰ　確率：１／２", "４回目：＋１ＨＰ　確率：１／１"]
player_model = [ # 0-vscode, 1-colab, 2-cmd_linux -> 0-level1, 1-level2, 2-level3
    [ # vscode
        [['　','　','　','∧','　','∧',' ','__','__　 '],[' 　','／','(*','ﾟー','ﾟ)','／',' ','＼',' '],['／','|','￣','∪ ','∪',' ','￣','|','＼','／　　'],['　','|＿','＿','＿','＿','|／','']], # level1
        [['　','　','　','∧','　','∧',' ','__','__　 '],[' 　','／','(*','ﾟー','ﾟ)','／',' ','＼',' '],['／','|','￣','∪ ','∪',' ','￣','|','＼','／　　'],['　','|＿','＿','＿','＿','|／',''],['  ','  ',' ∪',' ∪']], # level2
        [['　','  ','  ','∧ ',' ∧','　'],[' 　','  ','(*','ﾟー','ﾟ)',''],['　',' 　','/　','つ','つ',''],[' ～','（','＿','_,',',ﾉ',' ']] # level3
    ],
    [ # colab
        [['　','　','　','∧',' ','∧','__','__ '],[' 　','／','(*','ﾟー','ﾟ)','／',' ','＼',' '],['／','|','￣','∪','∪','￣','|','＼','／','　　'],['　','|＿','＿','＿','＿','|／','']], # level1
        [['　','　','　','∧',' ','∧','__','__ '],[' 　','／','(*','ﾟー','ﾟ)','／',' ','＼',' '],['／','|','￣','∪','∪','￣','|','＼','／','　　'],['　','|＿','＿','＿','＿','|／',''],['  ','  ',' ∪','∪',' ']], # level2
        [['　','  ','  ','∧ ','∧',' '],[' 　','  ','(*','ﾟー','ﾟ)','  '],['　',' 　','/　','つ','つ',''],[' ～','（','＿','_,',',ﾉ']] # level3
    ],
    [ # cmd_linux
        [['　','　','　','∧',' ','∧','__','__ '],[' 　','／','(*','ﾟー','ﾟ)','／',' ','＼',' '],['／','|','￣','∪','∪','￣','|','＼','／','　　'],['　','|＿','＿','＿','＿','|／','']], # level1
        [['　','　','　','∧',' ','∧','__','__ '],[' 　','／','(*','ﾟー','ﾟ)','／',' ','＼',' '],['／','|','￣','∪','∪','￣','|','＼','／','　　'],['　','|＿','＿','＿','＿','|／',''],['  ','  ',' ∪','∪',' ']], # level2
        [['　','  ','  ','∧ ','∧',' '],[' 　','  ','(*','ﾟー','ﾟ)','  '],['　',' 　','/　','つ','つ',''],[' ～','（','＿','_,',',ﾉ']] # level3
    ]
]
monster_model = [ # 0-vscode, 1-colab, 2-cmd_linux -> 0-monster1, 1-monster2
    [ # vscode
        [["/|"],["|/", "__", "__"],['ヽ','|', 'l ','l│ '],['　', '┷-', '┷-', '┷ ']], # monster1
        [[' ,','.-','\'\'','\"¨','￣','¨`','\' ','‐ ','、'],['(,','(,','i,',',i',',,','i,',',i',',)',',)'],['　','　',' ）',' 　','（',''],[' 　','（','ﾟー','ﾟ*','　','）','']] # monster2
    ],
    [ # colab
        [['/|'],['|/','__','___',' '],['ヽ','|-',' -│',''],['  ','┷┷','┷ ','',' ']], # monster1
        [[' ,','.-','\'\'','\"¨','￣','¨`','\'‐','、 ','',''],['(,','(,','i,',',i',',,','i,',',i',',)',',)'],['　','　',' ）',' 　','（',''],[' 　','（','ﾟー','ﾟ*','  ','）','']] # monster2
    ],
    [ # cmd_linux
        [["/|"],["|/", "__", "__"],['ヽ','|', 'l ','l│ '],['　', '┷-', '┷-', '┷ ']], # monster1
        [[' ,','.-','\'\'','\"¨','￣','¨`','\'‐','、 ','',''],['(,','(,','i,',',i',',,','i,',',i',',)',',)'],['　','　',' ）',' 　','（',''],[' 　','（','ﾟー','ﾟ*','  ','）','']] # monster2
    ]
]
hp_beacon_model = [ # 0-vscode, 1-colab, 2-cmd_linux
    [['  ','__','__','__','ο-','o-','☆.'],['┏━','┛ ','  ',' ┗','━┓'],['┃┛','  ','  ','  ','┗┃'],['┃ ','  ','HP','  ',' ┃'],['┃┓','  ','  ','  ','┏┃'],['┗━','━━','━━','━━','━┛']], # vscode
    [['  ','__','__','__','ο-','o-','☆.',''],['┏┛','  ','  ','┗┓','',''],['┃┛','  ','  ','┗┃','',''],['┃ ','  ','HP','  ',' ┃',''],['┃┓','  ','  ','┏┃','',''],['┗━','━━','━┛','','','']], # colab
    [['  ','__','__','__','ο-','o-','☆.',''],['┏━','┛ ','  ',' ┗','━┓'],['┃┛','  ','  ','  ','┗┃'],['┃ ','  ','HP','  ',' ┃'],['┃┓','  ','  ','  ','┏┃'],['┗━','━━','━━','━━','━┛']] # cmd_linux
]

# 実行環境検出
console_clear_st = True
try: from google.colab import output
except ImportError:
    console_clear_st = False
    import os
    OS = 2 # windows
    platform = int(input("実行環境を選んでください。\n\n0 - Visual Studio Code\n2 - cmd.exe or Linux\n\n数字を入力してください>"))

def toem(n): # 半角数字から全角数字に変換する
    num = ["０","１","２","３","４","５","６","７","８","９"]
    em = ""
    for i in str(n): em += num[int(i)]
    return em

mdata = []
class Screen:
    BD = [0,
        ["┏","┓","┗","┛","━","┃","┃"],     # Google Colaboratory
        ["┏━","━┓","┗━","━┛","━━","┃ "," ┃"] # Windows, Linux
    ]
    def __init__(self): self.L = []

    def SET_WINDOW(self, width=50, height=5, os=1):  # width - スクリーン横幅
        self.width = width                           # os - 1 [Google Colaboratory], 2 [Windows] [Linux]
        self.height = height
        self.os = os
        BD = self.BD
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

    def SET_TEXT(self, msg="Ｍｅｓｓａｇｅ．", row=False, col=False):
        width = self.width
        height = self.height
        if not row: row = 1
        if not col: col = 1
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

    def SET_MODEL(self, model, col):
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

s = Screen()
s.SET_WINDOW(width=40, height=18, os=OS) # ウィンドウ作成

def console_clear():
    if console_clear_st: output.clear()
    else: os.system("cls")

def window_input(msg="", wait=True):
    s.WINDOW()
    res = 0
    if wait: res = input(msg)
    s.CLEAR_WINDOW()
    console_clear()
    return res

def hp_graphics(player_hp):
    global _player_hp
    if player_hp < _player_hp: hp_graphics_list = ['♥ ' if i < player_hp else '♡ ' for i in range(_player_hp)]
    else: hp_graphics_list = ['♥ ' for i in range(player_hp)]
    _player_hp = player_hp
    return hp_graphics_list

def HPBeacon(player_hp, p): # inum - 入力した数, p - 確率 1 2 3
    hp_add = player_hp
    while True:
        try:
            s.SET_TEXT("ＨＰビーコン", row=1)
            s.SET_TEXT(hp_beacon_msg[p-1], row=3)
            s.SET_TEXT_CENTER("０～９の中から数字を１つ選んでください。")
            s.SET_MODEL(hp_beacon_model[platform], col=16)
            inum = int(window_input("数字を入力 >"))
            if 9 < inum: raise
            break
        except:pass

    rnum = [i for i in range(10)]
    random.shuffle(rnum)              # 確率1/1
    if 1 == p: 
        rnum = [rnum[0]]              # 確率1/10
        hp_add += 10
        space = 2
    if 2 == p: 
        rnum = random.sample(rnum, 2) # 確率1/5
        hp_add += 5
        space = 3
    if 3 == p: 
        rnum = random.sample(rnum, 5) # 確率1/2
        hp_add += 3
        space = 4
    if 4 == p:
        hp_add += 1
        space = 10
    s.SET_TEXT_CENTER("あなた{}コンピュータ{}".format("　"*space, "　"*(space-2)), row=7)
    s.SET_TEXT_CENTER("　{}　　　　　　{}　　".format(toem(inum), "　".join([toem(i) for i in rnum]) ), row=8)
    if inum in rnum:
        s.SET_TEXT_CENTER("勝ち！", row=9)
        s.SET_TEXT_CENTER("エンターを押してください。", row=15)
        window_input()
        return hp_add
    else:
        s.SET_TEXT_CENTER("負け！", row=9)
        s.SET_TEXT_CENTER("エンターを押してください。", row=15)
        window_input()
        return HPBeacon(player_hp, p+1)

def play(player_hp=1, score=0, kill_count=0, player_model=False, player_x_axis=20, monster_model=False, monster_x_axis=40, msg=False): # monster_x_axis: min, max 10, 40
    s.SET_TEXT("ＨＰ：", row=1)
    s.SET_TEXT(hp_graphics(player_hp), row=1, col=4)
    s.SET_TEXT("スコア：", row=2)
    s.SET_TEXT(toem(score), row=2, col=5)
    s.SET_TEXT("モンスターを倒した数：", row=3)
    s.SET_TEXT(toem(kill_count), row=3, col=12)
    if msg:           s.SET_TEXT_CENTER(msg, row=5)
    if player_model:  s.SET_MODEL(model=player_model, col=player_x_axis)
    if monster_model: s.SET_MODEL(model=monster_model, col=monster_x_axis)
    s.WINDOW()

window_input(wait=False) # ターミナル初期化

# スプラッシュ画面
s.SET_TEXT_CENTER("Ｒｕｎｎｉｎｇ　Ｄｉｎｏｓａｕｒｓ", row=7)
s.SET_TEXT_CENTER("受け身は最大の攻撃である！", row=9)
s.SET_TEXT_CENTER("エンターを押してください。", row=15)
window_input()

# ステージ選択画面
s.SET_TEXT_CENTER("Ｒｕｎｎｉｎｇ　Ｄｉｎｏｓａｕｒｓ", row=7)
s.SET_TEXT_CENTER("１　－　ステージ１　平均スコア：５０", row=9)
s.SET_TEXT_CENTER("２　－　ステージ２　平均スコア：１５", row=10)
s.SET_TEXT_CENTER("ステージを選択してください。", row=15)
stage_level = int(window_input("数字を入力 >"))-1

# 初期HPビーコン
s.SET_TEXT_CENTER("冒険を始める前に、ＨＰビーコンをドロップできます。")
s.SET_TEXT_CENTER("エンターを押してください。", row=15)
window_input()

player_hp = HPBeacon(player_hp, 1) # HPBeacon

# スタート画面
s.SET_TEXT_CENTER("スタート！")
s.WINDOW()
sleep(2)
s.CLEAR_WINDOW()
console_clear()

while 0 < player_hp:
    stage_map = [random.randint(monster_lv[stage_level][0], monster_lv[stage_level][1])*random.choice(beacon_pop_rate) for i in range(10)] # マップの生成
    for ent in stage_map:
        if 0 >= player_hp: break
        monster_model_num = random.randint(0,1) # モンスターの種類
        if 10 > player_hp: player_model_num = 0
        if 12 < player_hp: player_model_num = 1
        if 15 < player_hp: player_model_num = 2
        if ent:
            for i in reversed(range(10,40)):
                msg = "モンスターが現れた！　レベル：{}".format(toem(ent))
                if 30 > i: msg=""
                play(player_hp=player_hp, score=stage_turn, kill_count=kill_count, player_model=player_model[platform][player_model_num], monster_model=monster_model[platform][monster_model_num], player_x_axis=5,  monster_x_axis=i, msg=msg)
                sleep(0.2)
                s.CLEAR_WINDOW()
                console_clear()
            player_hp -= ent
            if 0 < player_hp: kill_count += 1
        else:
            for i in reversed(range(10,40)):
                msg = "ＨＰビーコン発見！"
                if 30 > i: msg = ""
                play(player_hp=player_hp, score=stage_turn, kill_count=kill_count, player_model=player_model[platform][player_model_num], monster_model=hp_beacon_model[platform], player_x_axis=5,  monster_x_axis=i, msg=msg)
                sleep(0.2)
                s.CLEAR_WINDOW()
                console_clear()
            player_hp = HPBeacon(player_hp, 1) # HPビーコン
        stage_turn += 1

print("> ゴール！")
print("> モンスターを倒した数：",kill_count)
print("> スコア:",stage_turn)