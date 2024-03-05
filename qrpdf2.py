from pathlib import Path
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

# 画像ファイルのパスとファイル名（=連番）をタプルで用意する
_images = tuple(Path('./img').glob('*.png'))
images = tuple(sorted(_images))
images_name = tuple(map(lambda im: im.stem , images))

# （※１）ラベルシートの設定
cards_num= (3, 8)  # カードをA4に何枚配置するか（横の枚数, 縦の枚数）
A4_mm = (210, 297)  # A4用紙のサイズをmmで指定(横、縦)
card_mm = (70, 33.9)  # 1枚のラベルのサイズをmmで指定(横、縦)
margin_mm = (0, 12.7) # 余白をmmで指定(左右、上下)

to_px = A4[0] / A4_mm[0] # mmをpxに変換
card = tuple(( x * to_px for  x in card_mm )) # カードのサイズpx
margin = tuple(( x * to_px for  x in margin_mm )) # 余白のサイズpx

# （※２）A4のpdfを作成する
file_name = 'sample.pdf'
page = canvas.Canvas(file_name, pagesize=A4)

# page.setFont('Helvetica', 80)  # ページのフォントを指定

# 源真ゴシック（ http://jikasei.me/font/genshin/）
GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Monospace-Medium.ttf"
# 日本語フォントの設定
pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))
font_size = 12
page.setFont('GenShinGothic', font_size)

# A4のpdfに必要なものを描画する
for imagen in images:
    pos = [margin[0], margin[1]] # 描画の初期地点
    i = 0
    page.setLineWidth(2)  # 線の太さを指定
    # 画像読み込み
    image = Image.open(imagen)
    while  (i < cards_num[0] * cards_num[1]):
            for y in range(cards_num[1]):
                for x in range(cards_num[0]):

                    # （※３）図形（長方形、直線）とテキストの描画
                    page.rect(pos[0], pos[1], card[0], card[1]) 
                    # page.line(pos[0] + card[0]/12, pos[1] + card[1]/4, pos[0] + card[0]/2 - 5, pos[1] + card[1]/4)
                    page.setFont("GenShinGothic", font_size)
                    # ファイルのフルパスからファイル名を取得
                    file_name_with_extension = os.path.basename(imagen)
                    # ファイル名から拡張子を取り除く
                    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
                    page.drawString(pos[0] + card[0]/12 -5 , pos[1] + card[1]/4 + 50, file_name_without_extension)

                    # （※４）画像の挿入
                    page.drawInlineImage(image, pos[0] + card[0]/2 + 30, pos[1] + card[1]/12 - 5, width=card[0]/3, height= card[0]/3)
                    i += 1
                    pos[0] += card[0]

                pos[0] = margin[0]
                pos[1] += card[1]
    page.showPage()

# PDFファイルを保存
page.save()
