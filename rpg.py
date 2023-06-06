import math
import random
import sys
import pygame as pg
import time
from pygame.locals import *

pg.init()

# global変数
WIDTH = 1600    # ウィンドウの横幅
HIGHT = 900     # ウィンドウの縦幅
txt_origin = ["攻撃","防御","魔法","回復","調教","逃走"]    # 勇者の行動選択肢のリスト
HP = 100        # 勇者のHP
MP = 10         # 勇者のMP
ENE_HP = 200    # 敵スライムのHP
ENE_MP = 0      # 敵スライムのMP
ATK = 10        # 勇者の攻撃力
MJC = 30        # 勇者の魔力
DEF = 10        # 勇者の防御力
TAM = 5         # ？
TAME_POINT = 20 # テイム力
ENE_ATK = 10    # 敵スライムの攻撃力
TAME = 0        # ？

class Text:
    """
    テキストボックスの表示に関するクラス
    """
    def __init__(self,syo):
        self.text = syo
    
    def draw(self, scr, text_color, x, y):
        """
        scr: screen
        text_color: テキストの色
        x: テキストのx座標
        y: テキストのy座標
        """
        font = pg.font.SysFont("hg正楷書体pro", 100)    # フォントと文字サイズ指定
        text_surface = font.render(self.text, True, text_color)     # テキストsurface
        text_rect = text_surface.get_rect(center=(x,y))     # テキストのrect取得、中心を(x, y)に指定
        scr.blit(text_surface, text_rect)   # テキスト描画

class Button:
    """
    勇者の行動選択ボタンに関するクラス
    """
    def __init__(self, x, y, width, height, color, hover_color, text, text_color, action, num, text2, hp_mp):
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
        text2: ?
        hp_mp: ?
        """
        self.rect = pg.Rect(x, y, width, height)    # rectを四角形を描画するsurfaceで初期化
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.num = num
        self.text2 = text2
        self.hp_mp = hp_mp

    def draw(self,scr):
        """
        ボタンを描画するメソッド
        scr: ディスプレイのsurface
        """
        pg.draw.rect(scr, self.color, self.rect)    # ボタンとなる四角形を描画
        font = pg.font.SysFont("hg正楷書体pro", 50)  # フォント指定
        text_surface = font.render(self.text, True, self.text_color)    # テキストsurface
        text_rect = text_surface.get_rect(center=self.rect.center)      # テキストの中心値指定
        scr.blit(text_surface, text_rect)   # ボタン描画

    def handle_event(self, event, scr, fight_img, win2):
        """
        勇者の行動の切り替えメソッド
        event: event
        scr: screen
        fight_img: 勇者の攻撃エフェクト
        win2: ?
        """
        # マウスボタンが押されたかつ左クリック(event.button == 1)の場合
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # マウスの座標がボタンの範囲内にあれば
            if self.rect.collidepoint(event.pos):
                act = self.action(self.num, self.text2, self.hp_mp, scr, fight_img, win2)   # action関数を実行
                return act
            
def calculate_damage(damage, defense):
    """
    ダメージ計算に関する関数
    """
    defense_diff = damage - defense
    if defense_diff < 0:
        defense_diff = 0
    return defense_diff
        
class HP_MP:
    """
    戦闘時のターンとヒットポイントとマジックポイントに関するクラス
    """
    def __init__(self, turn):
        """
        初期化メソッド
        turn: 勇者のターンか敵スライムのターンか判断する（0: 敵スライムのターン、1: 勇者のターン）
        """
        self.hp = HP
        self.mp = MP
        self.turn = turn
        self.e_hp = ENE_HP
        self.font = pg.font.SysFont("hg正楷書体pro", 50)
        self.pl_hp = self.font.render(f"HP:{self.hp} MP:{self.mp}", True, (255,255,255))
        self.ene_hp = self.font.render(f"HP:{self.e_hp}", True, (255,255,255))
        self.PL_action = ""
        
    def PL(self, hp, mp):
        """
        勇者のHP, MPに関するメソッド
        hp: 勇者のヒットポイント
        mp: 勇者のマジックポイント
        """
        self.hp = hp
        self.mp = mp
        self.pl_hp = self.font.render(f"HP:{self.hp} MP:{self.mp}", True, (255,255,255))    # 勇者のHP, MPのテキストsurface
        
    def ENE(self, e_hp):
        """
        敵スライムのHPに関するメソッド
        e_hp: 敵スライムのヒットポイント
        """
        self.e_hp = e_hp
        self.ene_hp = self.font.render(f"HP:{self.e_hp}", True, (255,255,255))  # 敵スライムのHPのテキストsurface


def action(i, text: Text, hp_mp: HP_MP, screen, fight_img, win2):
    """
    勇者の行動に関する関数
    i: index (0:攻撃, 1:防御, 2:魔法, 3:回復, 4:調教, 5:逃走)
    text: 
    hp_mp: ターン
    screen: screen
    fight_img: 勇者の攻撃エフェクト
    win2: 状況説明のテキストボックス
    """
    # gloabal変数
    global HP, ENE_HP, TAME, is_mouse_pressed

    hp = int(hp_mp.hp)          # 勇者のHP
    mp = int(hp_mp.mp)          # 勇者のMP
    ene_hp = int(hp_mp.e_hp)    # 敵スライムのHP
    is_mouse_pressed = False    # マウスが押されているかの判定をFalseにする

    if hp_mp.turn==1:    # 勇者のターンだったら
        # 攻撃
        if txt_origin[i]=="攻撃":   # 攻撃ボタンが押されたら
            ene_hp -= ATK           # スライムのHPを減らす
            if ene_hp <= 0:         # スライムのHPが0以下になったら
                ene_hp = 0          # スライムのHPを0にする
            text.text = f"{ATK}ダメージ与えた"  # スライムにダメージが入ったときのテキスト
            hp_mp.ENE(ene_hp)
            hp_mp.turn = 0      # 敵スライムのターンにする
            # 攻撃エフェクト
            toka = 0            # 攻撃エフェクトの透過度
            for j in range(25):
                toka += 10      # 透過度を10増やす
                if toka > 255:
                    toka = 0
                fight_img.set_alpha(toka)
                screen.blit(fight_img,[200, 100])   # 攻撃エフェクト描画
                pg.display.update()
            time.sleep(0.1)

        # 防御
        if txt_origin[i] == "防御":
            text.text = "盾を構えた"
            hp_mp.turn = 0      # 敵スライムのターンにする
        #防御が押されたら
        if(i == 1):
            is_mouse_pressed = True

    # 調教：使用時の敵HPによって成功率が変わる
    if i == 4:
        m = random.randint(0, ENE_HP)   # 0以上スライムのHPの値以下の乱数を生成
        # i = 0  #絶対成功する
        if m <= (ENE_HP - ene_hp):
            print("ていむ成功！！！")
            TAME = 1
        else:
            TAME = 2
        hp_mp.turn = 0          # スライムのターンにする

    if txt_origin[i] == "魔法": # 魔法が押されたら
        if mp > 0:          # MPが0より大きかったら
            ene_hp -= MJC   # スライムのHPを勇者の魔力の分だけ減らす
            if ene_hp <= 0: # スライムのHPが0以下になったら
                ene_hp = 0  # スライムのHPを0にする
            mp-=1           # 勇者のmpを1減らす
            hp_mp.turn = 0  # スライムのターンにする
            text.text = f"{MJC}ダメージ与えた"
        else:               # 0以下だったら
            text.text = "MPが足りません"
        hp_mp.ENE(ene_hp)
        hp_mp.PL(hp,mp)

    # 回復
    if txt_origin[i]=="回復":   # 回復が押されたら
        if hp < HP and mp > 0:  # 勇者の現在のHPが元のHPより小さい and 勇者のMPが0より大きい場合
            nokori = HP - hp    # 減った分のHP
            if nokori > MJC:    # 減った分のHPが魔力より大きかったら
                hp += MJC       # HPを魔力分回復
            else:               # 減った分のHPが魔力以下だったら
                hp += nokori    # 減った分のHPだけHPを増やす
            mp -= 1         # MPを1減らす
            if hp >= HP:    # 勇者の現在のHPが元のHP以上だったら
                hp = HP     # 現在のHPを元のHPにする
            hp_mp.PL(hp,mp)
            text.text = f"{MJC}回復した"
            hp_mp.turn = 0  # 敵スライムのターンにする
        elif mp < 1:        # 勇者のMPが1未満だったら
            text.text = "MPが足りません"
        elif hp >= 50:
            text.text = "体力が満タンです"
    
    # 逃走
    if txt_origin[i] == "逃走": # 逃走が押されたら
        text.text = "勇者は逃げ出した"
        screen.blit(win2,[50,50])       # 状況説明のテキストボックスの表示
        text.draw(screen, (255, 255, 255), WIDTH/2, 150)    # テキストを表示
        pg.display.update()     # displayのアップデート
        time.sleep(3)           # 3秒止めて
        sys.exit()              # プログラム終了

    if hp_mp.turn == 0:         # スライムのターンだったら、
        hp_mp.PL_action = txt_origin[i] # 

def ENE_action(PL_action,hp_mp:HP_MP,text:Text, screen, ene_img, attack_slime):
    hp = int(hp_mp.hp)
    mp = int(hp_mp.mp)
    current_time = time.time() #ここからワイの実装
    attack_interval = 5 #攻撃の間隔
    last_attack_time = 0 #攻撃時刻
    keika_time = current_time - last_attack_time
    for k in range(30):
        if  keika_time >= attack_interval: #スライムの攻撃
            attack_x = random.randint(0, WIDTH - ene_img.get_width())
            attack_y = random.randint(0, HIGHT - ene_img.get_width())
            last_attack_time = current_time
            time.sleep(0.01) #攻撃の速さ
        screen.blit(attack_slime,[attack_x,attack_y]) #ここもワイ
        pg.display.update()
    if PL_action=="防御":
        damege = ENE_ATK - DEF
        hp -= damege
        hp_mp.PL(hp,mp)
    else:
        damege = ENE_ATK
        hp -= damege
        hp_mp.PL(hp,mp)
    text.text=f"{damege}ダメージくらった"
    hp_mp.turn=1
        
def main():
    """
    main関数
    """
    global WIDTH, HIGHT, txt_origin, HP, ENE_HP, TAME    # global変数
    
    turn = 1    # 勇者のターンにする

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
    # 攻撃エフェクト
    attack_slime = pg.image.load("./ex05/fig/momoka.png")       # スライムの攻撃エフェクト
    attack_slime = pg.transform.scale(attack_slime, (300, 200))
    toka = 0    # 攻撃エフェクトの透過度
    fight_img = pg.image.load("./ex05/fig/fight_effect.png")    # 勇者の攻撃エフェクト
    fight_img = pg.transform.scale(fight_img,(WIDTH,HIGHT))
    # テキストボックス
    win = pg.image.load("./ex05/fig/win.png")
    win = pg.transform.scale(win,(WIDTH/4, HIGHT/2))    # 行動選択のテキストボックス
    win2 = pg.transform.scale(win,(WIDTH-100, HIGHT/4)) # 状況説明のテキストボックス  
    # フォント
    font1 = pg.font.SysFont("hg正楷書体pro", 100)
    font2 = pg.font.SysFont("hg正楷書体pro", 50)
    # テキスト
    syo = "野生のスライムが現れた"
    text = Text(syo)
    fight_txt = "スライムを倒した！"
    txt = []    # 選択ボタンを描画するsurfaceのリスト
    text_surface = HP_MP(turn)

    font3 = pg.font.SysFont(None, 200)
    die_text = "You died" # 死亡メッセージ

    for i,tx in enumerate(txt_origin):
        # インスタンス化
        if i%2==0:
            button = Button(125, 500+(i//2)*100, 100, 50, 
                            (50,50,50), (0,0,0), tx, 
                            (255,255,255), action, 
                            i, text, text_surface)
        else:
            button = Button(275, 500+(i//2)*100, 100, 50, 
                            (50,50,50), (0,0,0), tx, 
                            (255,255,255), action, 
                            i, text, text_surface)
        txt.append(button)

    # 繰り返し文    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return    # ×ボタンが押されたらプログラム終了

            for button in txt:
                button.handle_event(event, screen, fight_img, win2)

                #変更箇所
                if  TAME == 1:
                    text.text = "ていむ成功！！"
                elif TAME == 2:
                    text.text = "ていむ失敗..."
                    TAME = 0

        screen.blit(bg_img,[0, 0])      # 背景描画
        screen.blit(ene_img,[WIDTH/2-ene_rct.width/2+100, HIGHT/2]) # 敵スライム描画
        screen.blit(win,[50, 400])      # テキストボックス描画
        screen.blit(win2,[50, 50])      # 行動選択のテキストボックス描画

        if  text_surface.e_hp <= 0:
            text.text = fight_txt
            text_surface.turn=2
        x = 200
        for chr in text.text:
            rendered_text = font1.render(chr, True, (255, 255, 255))
            text_width = rendered_text.get_width()
            screen.blit(rendered_text,[x, 100])
            x += text_width
        for i in txt:
            i.draw(screen)  # ボタン描画
        screen.blit(text_surface.pl_hp,[100, 350])   # 勇者のHP,MP表示
        screen.blit(text_surface.ene_hp,[WIDTH/2-ene_rct.width/2+225, HIGHT/2-50])    # 敵スライムのHP表示
        pg.display.update()     # ディスプレイのアップデート
        clock.tick(100)         # 時間

        if text_surface.hp <= 0: # HPが0になったら
            die_text2 = font3.render(die_text, True, (255, 0, 0))
            screen.blit(die_text2, (600, 450)) # 600, 450の位置に赤色で"You died"を表示する
            pg.display.update()
            time.sleep(3)
            pg.quit()

        if text_surface.e_hp <= 0 or TAME == True:
            pg.display.update()
            time.sleep(3)
            sys.exit()
        
        if text_surface.turn == 0:
            time.sleep(1)
            text.text="相手の攻撃"
            screen.blit(win2,[50,50])
            text.draw(screen, (255,255,255), WIDTH/2,150)
            pg.display.update()
            time.sleep(1)
            PL_action = text_surface.PL_action
            ENE_action(PL_action, text_surface, text, screen, ene_img, attack_slime)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()