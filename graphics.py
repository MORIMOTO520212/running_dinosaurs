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
OS = 2
s.SET_WINDOW(width=40, height=18, os=OS)

def window_input(msg, wait=True):
    s.WINDOW()
    res = 0
    if wait: res = input(msg)
    s.CLEAR_WINDOW()
    console_clear()
    return res

# スプラッシュ画面
#s.SET_TEXT_CENTER("Ｒｕｎｎｉｎｇ　Ｄｉｎｏｓａｕｒｓ", row=7)
#s.SET_TEXT_CENTER("受け身は最大の攻撃である！", row=9)
#s.SET_TEXT_CENTER("エンターを押してください。", row=15)
#s.WINDOW()

# ステージ選択画面
#s.SET_TEXT_CENTER("Ｒｕｎｎｉｎｇ　Ｄｉｎｏｓａｕｒｓ", row=7)
#s.SET_TEXT_CENTER("１　－　ステージ１", row=9)
#s.SET_TEXT_CENTER("２　－　ステージ２", row=10)
#s.SET_TEXT_CENTER("ステージを選択してください。", row=15)
#s.WINDOW()
#stage_level = int(input("数字を入力 >"))-1

# モンスター配置  引数：(list)model - モデルデータ (int)col - モデル横位置 (min+1-左端, max-1-右端)
#s.SET_MODEL(model=[monster_model_data], col=x)

player_hp = 5

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

# プレイ画面
_player_hp = 0
def hp_graphics(player_hp):
    global _player_hp
    if player_hp < _player_hp: hp_graphics_list = ['♥ ' if i < player_hp else '♡ ' for i in range(_player_hp)]
    else: hp_graphics_list = ['♥ ' for i in range(player_hp)]
    _player_hp = player_hp
    return hp_graphics_list

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


play(player_hp=player_hp, score=10, kill_count=3, player_model=player_model[2][0], monster_model=hp_beacon_model[2], player_x_axis=5,  monster_x_axis=30, msg="")

# HPビーコン　入力
#hp_beacon_msg = ["１回目：＋１０ＨＰ　確率：１／１０", "２回目：＋５ＨＰ　確率：１／５", "３回目：＋３ＨＰ　確率：１／２", "４回目：＋１ＨＰ　確率：１／１"]
#s.SET_TEXT("ＨＰビーコン", row=1)
#s.SET_TEXT(hp_beacon_msg[0], row=3)
#s.SET_TEXT_CENTER("０～９の中から数字を１つ選んでください。")
#s.SET_MONSTER(hp_beacon_model_data, col=16)
#s.WINDOW()
#inum = input("数字を入力 >")

# HPビーコン　結果
#s.SET_TEXT_CENTER("あなた　　コンピュータ", row=7)
#s.SET_TEXT_CENTER("　{}　　　　　　{}　　".format(toem(4), toem(6)), row=8)
#s.SET_TEXT_CENTER("勝ち！", row=9)
#s.WINDOW()