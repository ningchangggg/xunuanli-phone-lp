"""手機版煦暖曆落地頁 v5（2026-11-25）：產生頁面用的靜態素材 → img/
- Widget：印刷 PDF 重排（widgets.xw_widget），跟實體煦暖曆同一天同一頁
- 受眾卡照片：手機版情境圖綠幕原圖重新合成，Widget 換成卡片上放大的那一天（手機裡跟放大卡同一天）
- 交換禮物卡：IG 封面「實拍 875＋iPhone」第一格（實體與手機都是 2027 元旦）
- 三種尺寸：phone_screen 的 iPhone 主畫面（小／中／大）
python3 -E -P assets.py"""
import os, sys, datetime, shutil, json
from functools import lru_cache
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○煦暖曆'
IMG = os.path.join(HERE, 'img'); os.makedirs(IMG, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, '01_廣告投放/手機版日曆/成片/小編開箱/工作檔'))
import storyboard as SB
P, MA, TR = SB.P, SB.MA, SB.TR
sys.path.insert(0, os.path.join(ROOT, '99_系統工具/產品廣告圖工具/實體x手機GIF'))
import widgets as XW

WK = '一二三四五六日'
_ORIG_ICON = P.icon.__wrapped__

def set_day(md):
    """主畫面「行事曆」圖示換成那一天（原本固定寫週五 22）"""
    mo, da = map(int, md.split('/')); wk = '週' + WK[datetime.date(2027, mo, da).weekday()]
    @lru_cache(None)
    def icon(name):
        if name != 'Calendar': return _ORIG_ICON(name)
        s = int(P.ICON * P.PT)
        im = Image.new('RGBA', (s, s), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
        d.text((s / 2, s * 0.24), wk, font=P.font(10.5, 'Medium'), fill=(232, 58, 48), anchor='mm')
        d.text((s / 2, s * 0.62), str(da), font=P.sf(33, 'Light'), fill=(20, 20, 22), anchor='mm')
        m = P.rmask(s, s, int(s * 0.225)); out = Image.new('RGBA', (s, s), (0, 0, 0, 0)); out.paste(im, (0, 0), m)
        return out
    P.icon = icon; P.app_sprite.cache_clear(); P.static_bg.cache_clear()

@lru_cache(None)
def widget(md):
    """1148 正方、圓角透明的 Widget（RGBA）"""
    return XW.xw_widget(md)

def save_widget(md, px, name):
    widget(md).resize((px, px), Image.LANCZOS).save(os.path.join(IMG, name))

def screen(md, size='L'):
    set_day(md)
    src = f'x:{md}' if size == 'L' else P.WIDGETS['煦暖曆'][size][0]
    return SB.screen('煦暖曆', size, src)

def compose_still(path, md, box, out_wh):
    """綠幕原圖重新合成：box=(x0,y0,w,h) 原圖座標，輸出 out_wh"""
    im = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB); Q, _ = TR.quad_of(im)
    ow, oh = MA.OW, MA.OH; MA.OW, MA.OH = out_wh
    try: a = MA.compose(im, np.array(Q, float), screen(md), np.random.default_rng(1), box)
    finally: MA.OW, MA.OH = ow, oh
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def green_info(path):
    im = cv2.imread(path); a = im.astype(int)
    g = (a[..., 1] - np.maximum(a[..., 0], a[..., 2])) > 60; ys, xs = np.nonzero(g)
    return im.shape[1], im.shape[0], (xs.min(), ys.min(), xs.max(), ys.max())

GREEN = os.path.join(ROOT, '99_系統工具/產品廣告圖工具/手機版情境圖/綠幕原圖')
# 受眾卡：(輸出名, 綠幕原圖, 手機裡那天, 裁切框中心偏移)
CARDS = [('p1', '00_煦暖曆_S1_週一早餐窗邊.jpg', '4/17'),
         ('p2', '01_煦暖曆_S2_午後窗邊閱讀.jpg', '1/7'),
         ('p4', '02_煦暖曆_S3_夜晚沙發毛毯.jpg', '12/25')]
PIC_W, PIC_H = 960, 1000          # 卡片照片 384×400（2.5 倍）

def cards():
    for name, f, md in CARDS:
        path = os.path.join(GREEN, f); W, H, (gx0, gy0, gx1, gy1) = green_info(path)
        ch = min(H, W * PIC_H / PIC_W); cw = ch * PIC_W / PIC_H               # 盡量大的框
        ph = gy1 - gy0
        if ch > ph * 2.6: ch = ph * 2.6; cw = ch * PIC_W / PIC_H              # 手機不要太小
        cx = (gx0 + gx1) / 2; cy = (gy0 + gy1) / 2 - ch * 0.04                # 手機略偏下，上方留給通知卡
        x0 = float(np.clip(cx - cw / 2, 0, W - cw)); y0 = float(np.clip(cy - ch / 2 + ch * 0.06, 0, H - ch))
        compose_still(path, md, (x0, y0, cw, ch), (PIC_W, PIC_H)).save(os.path.join(IMG, f'{name}.jpg'), quality=90)
        save_widget(md, 340, f'{name}_w.png')
        print(name, md, (round(x0), round(y0), round(cw), round(ch)), flush=True)
    # 03 交換禮物：IG 封面實拍 875＋iPhone（元旦），手機在右
    src = os.path.join(ROOT, '01_廣告投放/手機版日曆/圖文/IG輪播_4比5/工作檔/封面單品情境/換頁/_test_無字.jpg')    # 無字版（frame_00 有烤進 IG 封面標題）
    im = Image.open(src).convert('RGB'); print('875 frame', im.size)
    w, h = im.size; cw = w; ch = cw * PIC_H / PIC_W                         # 全寬，上方多留牆面放對話框（不壓到日曆頂蓋）
    x0 = 0; y0 = 135
    im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((PIC_W, PIC_H), Image.LANCZOS).save(os.path.join(IMG, 'p3.jpg'), quality=90)
    save_widget('1/1', 340, 'p3_w.png')

WALL = ['1/1', '1/7', '1/12', '1/20', '2/3', '2/14', '2/25', '3/8', '3/21', '4/1', '4/17', '5/1', '5/20', '6/6',
        '6/21', '7/7', '7/16', '8/8', '8/26', '9/13', '9/21', '9/28', '10/10', '10/22', '11/11', '11/26', '12/25', '12/31']
DAYS6 = ['1/1', '2/14', '3/21', '9/28', '11/11', '12/25']

def wall():
    os.makedirs(os.path.join(IMG, 'wall'), exist_ok=True)
    for i, md in enumerate(WALL):
        widget(md).resize((230, 230), Image.LANCZOS).save(os.path.join(IMG, 'wall', f'{i + 1:02d}.png'))
    print('wall', len(WALL), flush=True)

def anatomy():
    for md in DAYS6:
        save_widget(md, 620, f'a_{md.replace("/", "-")}.png')
    print('anatomy', flush=True)

def lock():
    """收尾鎖定畫面：桌布用 1/1 那張照片（印刷頁的照片）＋暗角，Widget 1/1"""
    b = XW.xw_blocks('1/1'); ph = XW.cover(b['photo'].convert('RGB'), 960, 1500, fy=0.45)
    ph = ph.filter(ImageFilter.GaussianBlur(26))
    a = np.asarray(ph).astype(np.float32) * 0.62 + np.array([20, 16, 22], np.float32) * 0.38
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(IMG, 'lock_bg.jpg'), quality=88)
    save_widget('1/1', 620, 'lock_w.png')

def sizes():
    for sz in ['S', 'M', 'L']:
        s = screen('3/22', sz)
        Image.fromarray(np.clip(s, 0, 255).astype(np.uint8)).resize((330, round(330 * s.shape[0] / s.shape[1])), Image.LANCZOS).save(os.path.join(IMG, f'scr_{sz}.png'))
    print('sizes', flush=True)

def authors():
    src = os.path.join(ROOT, '04_內容企劃/_多產品/落地頁改版設計_1122/11.24_煦暖曆_落地頁改版_v9_六色經典底座同步輪播_規格圖裁上方/_原始檔/img')
    for i in range(1, 9): shutil.copy(os.path.join(src, f'w{i}.jpg'), os.path.join(IMG, f'au{i}.jpg'))

def redeem():
    p = os.path.join(ROOT, '01_廣告投放/手機版日曆/圖文/IG輪播_4比5/工作檔/商品頁原圖/共用/使用說明.png')
    im = Image.open(p).convert('RGB')
    for i, box in enumerate([(78, 550, 318, 836), (382, 550, 620, 836), (683, 550, 922, 836)]):
        im.crop(tuple(round(v * 1.5) for v in box)).save(os.path.join(IMG, f'rd{i + 1}.jpg'), quality=92)

if __name__ == '__main__':
    sel = sys.argv[1:] or ['cards', 'wall', 'anatomy', 'lock', 'sizes', 'authors', 'redeem']
    for s in sel: globals()[s]()
