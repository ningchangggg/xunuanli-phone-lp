"""把 WORK/sec/*.png 與 WORK/gif/enc 整理成交付資料夾（手機版煦暖曆 v5）。python3 deliver.py"""
import os, shutil, base64, io
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
from build_page import WORK
O = os.path.dirname(HERE)
PRE = '11.25_手機版日曆_落地頁改版_v5'
SEC = [('s03', '03_誰適合手機版煦暖曆', 0), ('s03b', '03b_聖誕夜買也來得及_金光_GIF', 1), ('s04', '04_數字列', 0),
       ('s05', '05_365天Widget牆', 0), ('s05a', '05a_解鎖手機就換好_GIF', 1), ('s06', '06_一張Widget拆解_6天輪播_GIF', 1),
       ('s06a', '06a_長按換尺寸_GIF', 1), ('s07', '07_上班出差午休都看得到_GIF', 1), ('s08', '08_一封信完成兌換_GIF', 1),
       ('s09', '09_作家陣容', 0), ('s10', '10_三種桌面尺寸', 0), ('s11', '11_規格_設定頁', 0), ('s12', '12_收尾_鎖定畫面', 0)]
for sub in ['說明圖_1080寬', '動圖_MP4備用']:
    shutil.rmtree(f'{O}/{sub}', ignore_errors=True); os.makedirs(f'{O}/{sub}')
names = []
for sid, nm, g in SEC:
    if g:
        shutil.copy(f'{WORK}/gif/enc/{sid}.gif', f'{O}/說明圖_1080寬/{nm}.gif')
        shutil.copy(f'{WORK}/gif/enc/{sid}.mp4', f'{O}/動圖_MP4備用/{nm}.mp4')
        names.append((sid, nm + '.gif', g))
    else:
        Image.open(f'{WORK}/sec/{sid}.png').convert('RGB').save(f'{O}/說明圖_1080寬/{nm}.jpg', quality=90)
        names.append((sid, nm + '.jpg', g))
head = ('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>手機版煦暖曆落地頁 v5</title><style>body{margin:0;background:#888}main{max-width:432px;margin:0 auto;background:#fff}img,video{display:block;width:100%}</style><main>')
dyn = head + '\n'.join(f'<img src="說明圖_1080寬/{n}">' for _, n, _ in names) + '</main>'
open(f'{O}/{PRE}_整頁預覽_動態.html', 'w').write(dyn)
parts = []
for sid, n, g in names:
    if g:
        b = base64.b64encode(open(f'{WORK}/gif/enc/{sid}.mp4', 'rb').read()).decode()
        parts.append(f'<video autoplay muted loop playsinline src="data:video/mp4;base64,{b}"></video>')
    else:
        im = Image.open(f'{O}/說明圖_1080寬/{n}'); im = im.resize((864, round(im.height * 864 / im.width)), Image.LANCZOS)
        bio = io.BytesIO(); im.save(bio, 'JPEG', quality=86)
        parts.append(f'<img src="data:image/jpeg;base64,{base64.b64encode(bio.getvalue()).decode()}">')
open(f'{O}/{PRE}_整頁預覽_單檔整合.html', 'w').write(head + ''.join(parts) + '</main>')
ims = []
for sid, n, g in names:
    fr = {'s03b': '010'}.get(sid, '001')
    ims.append(Image.open(f'{WORK}/gif/secframes/{sid}/{fr}.png' if g else f'{O}/說明圖_1080寬/{n}').convert('RGB'))
H = sum(i.height for i in ims); st = Image.new('RGB', (1080, H)); y = 0
for i in ims: st.paste(i, (0, y)); y += i.height
st.resize((540, H // 2), Image.LANCZOS).save(f'{O}/{PRE}_整頁預覽_靜態第一格.jpg', quality=82)
shutil.copy(f'{WORK}/page.html', f'{HERE}/page.html')
print(O)
