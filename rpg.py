import math
import random
import sys
import pygame as pg

# global変数
WIDTH = 1600    # ウィンドウの横幅
HIGHT = 900     # ウィンドウの縦幅
txt_origin = ["攻撃","防御","魔法","回復","調教","逃走"]    # 勇者の行動選択肢のリスト
HP = 50         # 勇者のHP
MP = 10         # 勇者のMP
ENE_HP = 10     # 敵スライムのHP

class Button:
    """
    勇者の行動選択ボタンに関するクラス
    """
    def __init__(self, x, y, width, height, color, hover_color, text, text_color, action, num):
        """
        初期化メソッド
        x: ボタンのx座標
        y: ボタンのy座標
        width: ボタンの横幅
        height: ボタンの縦幅
        color: ボタンの色
        hover_color: マウスカーソルがボタンの上にある時のボタンの色
        text: 行動選択肢の文字
        text_color: 文字の色
        action: action関数
        num: index(0:攻撃, 1:防御, 2:魔法, 3:回復, 4:調教, 5:逃走)
        """
        self.rect = pg.Rect(x, y, width, height)    # rectを四角形を描画するsurfaceで初期化
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.num = num

    def draw(self,scr):
        """
        ボタンを描画するメソッド
        scr: surface
        """
        pg.draw.rect(scr, self.color, self.rect)    # ボタンとなる四角形を描画
        font = pg.font.SysFont("hg正楷書体pro", 50)  # フォント指定
        text_surface = font.render(self.text, True, self.text_color)    # テキストsurface
        text_rect = text_surface.get_rect(center=self.rect.center)      # テキストの中心値指定
        scr.blit(text_surface, text_rect)   # ボタン描画

    def handle_event(self, event):
        """
        イベントの切り替えメソッド
        event: ？
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action(self.num)
    
        
def action(i):
    """
    勇者の行動をプリントする関数
    i: index (0:攻撃, 1:防御, 2:魔法, 3:回復, 4:調教, 5:逃走)
    """
    p = ["攻撃","防御","魔法","回復","調教","逃走"]
    print(p[i])
        
def main():
    """
    main関数
    """
    global WIDTH, HIGHT, txt_t, txt_origin     # global変数

    bg_image = "./ex05/fig/back.png"
    pg.display.set_caption("RPG of くそげー")   # ウィンドウの名前
    screen = pg.display.set_mode((WIDTH, HIGHT))    # 1600x900のdisplay surface
    clock  = pg.time.Clock()                        # 時間
    # surface
    # 背景
    bg_img = pg.image.load(bg_image)
    bg_img = pg.transform.scale(bg_img,(WIDTH,HIGHT))
    # 敵スライム
    ene_img = pg.image.load("./ex05/fig/ene.png")
    ene_rct = ene_img.get_rect()
    # テキストボックス
    win = pg.image.load("./ex05/fig/win.png")
    win = pg.transform.scale(win,(WIDTH/4,HIGHT/2))
    win2 = pg.transform.scale(win,(WIDTH-100,HIGHT/4))
    # フォント
    font1 = pg.font.SysFont("hg正楷書体pro", 100)
    font2 = pg.font.SysFont("hg正楷書体pro", 50)
    # テキスト
    text = "野生のスライムが現れた"
    txt = []    # 選択ボタンを描画するsurfaceのリスト
    text_surface1 = font2.render(f"HP:{HP} MP:{MP}", True, (255,255,255))   # 勇者のHP,MPのテキストsurface
    text_surface2 = font2.render(f"HP:{ENE_HP}", True, (255,255,255))       # 敵スライムのHPのテキストsurface
    # 勇者の行動選択ボタンを描画するsurfaceを作成しリストtxtに追加
    for i,tx in enumerate(txt_origin):
        # インスタンス化
        if i%2==0:
            button = Button(125, 500+(i//2)*100, 100, 50, (50,50,50), (0,0,0), tx, (255,255,255), action, i)
        else:
            button = Button(275, 500+(i//2)*100, 100, 50, (50,50,50), (0,0,0), tx, (255,255,255), action, i)
        txt.append(button)

    # 繰り返し文    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return    # ×ボタンが押されたらプログラム終了

            for button in txt:                  # ？
                button.handle_event(event)

        screen.blit(bg_img,[0, 0])      # 背景描画
        screen.blit(ene_img,[WIDTH/2-ene_rct.width/2+100, HIGHT/2]) # 敵スライム描画
        screen.blit(win,[50, 400])      # テキストボックス描画
        screen.blit(win2,[50, 50])      # 行動選択のテキストボックス描画

        x = 200
        for chr in text:
            rendered_text = font1.render(chr, True, (255, 255, 255))
            text_width = rendered_text.get_width()
            screen.blit(rendered_text,[x, 100])
            x += text_width
        for i in txt:
            i.draw(screen)  # ボタン描画

        screen.blit(text_surface1,[100, 350])   # 勇者のHP,MP表示
        screen.blit(text_surface2,[WIDTH/2-ene_rct.width/2+225, HIGHT/2-50])    # 敵スライムのHP表示
        
        pg.display.update()     # ディスプレイのアップデート
        clock.tick(100)         # 時間

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()