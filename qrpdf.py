from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# PDFファイルの設定
pdf_file = "output.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4  # A4サイズ

# 余白の設定
margin = 2 * cm

# 枠の数
x, y = 2, 5  # 例: 3x4の枠

# 枠のサイズ計算
cell_width = (width - 2 * margin) / x
cell_height = (height - 2 * margin) / y

# 源真ゴシック（ http://jikasei.me/font/genshin/）
GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Monospace-Medium.ttf"

# 日本語フォントの設定
#c.registerFont("GenShinGothic", "./GenShinGothic-Monospace-Medium.ttf")  # フォントファイルへのパスを指定
#font_size = 10

pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))
font_size = 10
c.setFont('GenShinGothic', font_size)

# imgフォルダからPNG画像を読み込む
img_folder = "./img"
images = [f for f in os.listdir(img_folder) if f.endswith('.png')]

# 画像とファイル名をPDFに配置
for i, image_file in enumerate(images):
    row = i % y
    col = i // y
    if col >= x:  # x*yの枠を超えたら停止
        break
    
    # 画像の配置位置計算
    x_pos = margin + col * cell_width
    y_pos = height - margin - (row + 1) * cell_height
    
    # 画像を読み込んでサイズを調整
    img_path = os.path.join(img_folder, image_file)
    img = Image.open(img_path)
    img_width, img_height = img.size
    scale = min(cell_width / img_width, (cell_height - font_size * 1.5) / img_height)
    img = img.resize((int(img_width * scale), int(img_height * scale)), Image.Resampling.LANCZOS))
    
    # 画像をPDFに挿入
    c.drawInlineImage(img, x_pos, y_pos - img.size[1], width=img.size[0], height=img.size[1])
    
    # ファイル名を表示
    c.setFont("GenShinGothic", font_size)
    c.drawString(x_pos, y_pos - font_size * 1.5, image_file)

# PDFファイルを保存
c.save()
