import random

def toem(n): # 半角数字から全角数字に変換する
    num = ["０","１","２","３","４","５","６","７","８","９"]
    em = ""
    for i in str(n):
        em += num[int(i)]
    return em

def re_uni_txt(text):
    # replace color script.
    # 一色のみ対応
    pattern = r".*?(\033\[.*?m).*"
    res = re.match(pattern, text)
    uni_txt = []
    if res:
        dec = res.group(1)
        text = text.replace(dec, "@").replace("\033[00m", "#")
        i = 0
        while i < len(text):
            uni_txt.append(text[i])
            if text[i] == "@":
                if i:
                    uni_txt[i-1] += dec
                    uni_txt.remove("@")
                else:
                    uni_txt[i] = dec + text[i+1]
                    i += 1
            elif text[i] == "#":
                uni_txt[i-2] += "\033[00m"
            i += 1
        try:
            uni_txt.remove("#")
        except: pass
        return uni_txt
    return text

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

    def SET_TITLE(self, title="ＮｏＴｉＴｌｅ"):
        width = self.width
        BD = self.BD
        os = self.os
        title = re_uni_txt(title) # 装飾文字変換
        title_len = len(title)
        b_len = int((width - title_len) / 2)
        for i in range(width):
            x = i - b_len - 1

            if i == b_len:
                self.L[0][i] = BD[os][5]
            if i == b_len + title_len + 1:
                self.L[0][i] = BD[os][6]
            if i > b_len and x < title_len:
                self.L[0][i] = title[x]
    
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
        try:
            msg = re_uni_txt(msg) # 装飾文字変換
        except: pass
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

    def SEAT_CREATE(self, row=3, vacant="empty"):
        width = self.width
        seat_label = ["A ", "B ", "C ", "D ", "E ", "  ", "F ", "G ", "H ", "I ", "J "]
        seat_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]
        no_vacant = []

        if "empty" == vacant: vacant = 5
        if "slight" == vacant: vacant = 1

        b_len = int((width - 30) / 2) # 横15席
        for h in range(len(seat_label)):
            if seat_label[h] != "  ":
                self.L[h+row][b_len] = seat_label[h]
                x = 0
                for i in range(width):
                    if i > b_len and i%2 == 1:
                        if not random.randint(0, vacant): # 5. 余裕あり 1. 残りわずか
                            self.L[h+row][i] = empty+"　"+d.end()
                            no_vacant.append(seat_label[h].replace(" ","")+seat_num[x]) # ex-> [A03, E01, F15]
                        else:
                            self.L[h+row][i] = seat_num[x]
                        x += 1
                    if i > b_len and i%2 == 0:
                        self.L[h+row][i] = "  "
                    if x == len(seat_num):
                        break

        return no_vacant, self.L # 満席 座席表データ


    def MOVIE_LIST_CREATE(self ,page=1, view_num=4, row=4, col=1):
        width = self.width
        page_end = int(len(mdata)/view_num)
        if len(mdata)%view_num: page_end += 1
        if page > page_end:
            page = page_end
        if page < 1:
            page = 1
        table_num_end = view_num*page
        table_num_start = table_num_end - view_num
        if len(mdata)%view_num:
            page_end += 1
        for i in range(len(mdata)):
            if  i >= table_num_start and i < table_num_end:
                # 映画番号
                str_num = toem(i+1)
                title   = str_num+"．"+mdata[i]["title"]
                # 映画タイトル
                date       = mdata[i]["date"]
                hour       = mdata[i]["hour"]
                restricted = mdata[i]["restricted"]
                metadata   = re_uni_txt(f"　{date}　上映時間：{hour}　レイティング：{green + restricted + d.end()}")
                if "ＰＧ１２" == restricted:
                    metadata   = re_uni_txt(f"　{date}　上映時間：{hour}　レイティング：{red + restricted + d.end()}")

                for c in range(len(title)): # 1行目表示
                    if c == width-2: break  # 折り返しなし
                    self.L[row][c+col] = title[c]
                for c in range(len(metadata)): # 2行目表示
                    self.L[row+1][c+col] = metadata[c]
                for _ in range(width): # border
                    if not _: continue
                    if _ == width-1: continue 
                    self.L[row+2][_] = self.BD[self.os][4]
                row += 3
        return page
    
    def TIMETABLE_CREATE(self, f=False, page=1, view_num=4, row=4, col=1):
        width = self.width
        no_vacant = [] # 満席の番号
        timetbl_lst = mdata[f]["timetbl"]
        table_num = view_num*page
        page = table_num - view_num
        for i in range(len(timetbl_lst)):
            if i >= page and i < table_num:
                # タイムテーブル番号
                str_num = toem(i+1)
                if "full" == timetbl_lst[i][2]:
                    no_vacant.append(i+1)
                screen = timetbl_lst[i][0] # スクリーン
                time = timetbl_lst[i][1] # 上映時間
                vacant = timetbl_lst[i][2] # 空席状況
                for i in range(len(vacant_list)):
                    if vacant == vacant_list[i][0]:
                        vacant = vacant_list[i][self.os] # 記号置き換え
                timetbl = str_num+"．"+screen+"　　"+time+"　"
                timetbl = [_ for _ in timetbl]
                timetbl.append(vacant)

                for c in range(len(timetbl)): # 1行目表示
                    self.L[row][c+col] = timetbl[c]
                for _ in range(width): # border
                    if not _: continue
                    if _ == width-1: continue 
                    self.L[row+1][_] = self.BD[self.os][4]
                row += 2
        return no_vacant

    def WINDOW(self, data=False): # 出力  [data(list)] 画面データをセットできる
        if data: L = data
        else: L = self.L
        for line in L:
            for raw in line:
                print(raw, end="")
            print()

s = Screen()
s.SET_WINDOW(width=40, height=18, os=OS)