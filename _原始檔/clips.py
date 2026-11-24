"""手機版煦暖曆落地頁 v5：動圖片段 → WORK/gif/clips/<名>/NNN.jpg（1080×1350，4:5）
規則：Widget 不翻頁、不撕頁；換天＝印刷內頁做的 Widget 淡入淡出 0.35 秒；不同場景之間硬切。
- c_unlock：情境影片 V1b 睡前床上，3/21 → 3/22 → 3/23 每天自己換好
- c_resize：尺寸切換影片 煦暖曆沙發（Grok 綠幕＋長按選單），中 → 小 → 大，1.25 倍速
- c_where ：辦公桌 9/21 → 機場 9/13 → 午休公園 11/11，硬切
- a_days／c_redeem：一頁拆解 6 天、兌換三步驟（每格 1.2 秒，10fps）
python3 -E -P clips.py [名稱...]"""
import os, sys, json, shutil
import numpy as np, cv2
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import assets as A
SB, P, MA = A.SB, A.P, A.MA
WORK = '/private/tmp/claude-501/-Users-ningchang--claude-spares-spare-83sWsf/8be7a878-1d74-40b6-a934-3282ef5f9fed/scratchpad/work'
CL = os.path.join(WORK, 'gif', 'clips')
OUT_W, OUT_H, FPS = 1080, 1350, 15
SZ = os.path.join(A.ROOT, '01_廣告投放/手機版日曆/成片/尺寸切換影片/工作檔')

def odir(n):
    d = os.path.join(CL, n); shutil.rmtree(d, ignore_errors=True); os.makedirs(d); return d

def box_for(quads, fw, fh, k=1.75, dy=0.0):
    """以手機為中心的 4:5 裁切框（原影片座標），框高＝手機高 × k"""
    q = np.median(np.array(quads, float), axis=0)
    cx, cy = q[:, 0].mean(), q[:, 1].mean(); ph = q[:, 1].max() - q[:, 1].min()
    h = min(fh, ph * k); w = h * OUT_W / OUT_H
    if w > fw: w = fw; h = w * OUT_H / OUT_W
    x0 = float(np.clip(cx - w / 2, 0, fw - w)); y0 = float(np.clip(cy - h / 2 + dy * h, 0, fh - h))
    return (x0, y0, w, h)

def comp(frame, Q, scr, box, rng):
    ow, oh = MA.OW, MA.OH; MA.OW, MA.OH = OUT_W, OUT_H
    try: a = MA.compose(frame, np.array(Q, float), scr, rng, box)
    finally: MA.OW, MA.OH = ow, oh
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

SCR = {}
def scr(md):
    if md not in SCR: SCR[md] = A.screen(md)
    return SCR[md]

def raw_seq(name, t0, dur, days, k=1.75, dy=0.0, fade=0.35):
    """days=[(md, 開始秒)]；回傳每格 PIL"""
    path = os.path.join(SB.RAW, name); tr = json.load(open(os.path.splitext(path)[0] + '_track.json'))
    cap = cv2.VideoCapture(path); fps = cap.get(cv2.CAP_PROP_FPS)
    fw, fh = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    box = box_for(tr['quads'], fw, fh, k, dy); rng = np.random.default_rng(3); out = []
    for i in range(int(round(dur * FPS))):
        t = i / FPS; fi = min(len(tr['quads']) - 1, int(round((t0 + t) * fps)))
        cap.set(cv2.CAP_PROP_POS_FRAMES, fi); ok, f = cap.read()
        j = max(n for n, (_, s) in enumerate(days) if t >= s)
        s = scr(days[j][0])
        if j > 0 and t - days[j][1] < fade:
            e = P.smooth((t - days[j][1]) / fade); s = scr(days[j - 1][0]) * (1 - e) + s * e
        out.append(comp(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), tr['quads'][fi], s, box, rng))
    return out

def save(n, frames):
    d = odir(n)
    for i, im in enumerate(frames): im.save(os.path.join(d, f'{i + 1:03d}.jpg'), quality=90)
    print(n, len(frames), flush=True)

def c_unlock():
    save('c_unlock', raw_seq('V1b_不滑_睡前床上.mp4', 1.0, 4.8, [('3/21', 0), ('3/22', 1.6), ('3/23', 3.2)], k=1.6))

def c_where():
    fr = raw_seq('V5b_不滑_辦公桌.mp4', 2.0, 1.8, [('9/21', 0)], k=1.7)
    fr += raw_seq('V4b_不滑_機場候機.mp4', 3.4, 1.8, [('9/13', 0)], k=1.7)
    fr += raw_seq('V3b_不滑_午休公園.mp4', 3.0, 1.8, [('11/11', 0)], k=1.7)
    save('c_where', fr)

def c_resize(speed=1.25):
    A.set_day('3/22')
    cfg = MA.CFG['煦暖曆']; video = os.path.join(SZ, cfg['video'])
    tr = json.load(open(os.path.splitext(video)[0] + '_track.json')); quads = MA.fix_quads(tr['quads_raw'])
    tl = P.Timeline({'kind': '煦暖曆', 'seq': ['M', 'S', 'L'], 'touches': cfg['touches'],
                     'stacks': [P.WIDGETS['煦暖曆']['M'][:1], P.WIDGETS['煦暖曆']['S'][:1], ['x:3/22']]}, 10.04)
    cap = cv2.VideoCapture(video); fw, fh = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    box = box_for(quads, fw, fh, 1.45, -0.04); rng = np.random.default_rng(3); out = []
    n = int(10.0 / speed * FPS)
    for k in range(n):
        t = min(10.0, k * speed / FPS); i = min(len(quads) - 1, int(round(t * 24)))
        cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, f = cap.read()
        s = np.asarray(P.render(tl, t)).astype(np.float32)
        out.append(comp(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), quads[i], s, box, rng))
    save('c_resize', out)

def hold(n, files, reps=12):
    d = odir(n); k = 0
    for f in files:
        for _ in range(reps):
            k += 1; shutil.copy(f, os.path.join(d, f'{k:03d}.png'))
    print(n, k, flush=True)

def a_days():
    hold('a_days', [os.path.join(A.IMG, f'a_{md.replace("/", "-")}.png') for md in A.DAYS6])

def c_redeem():
    hold('c_redeem', [os.path.join(A.IMG, f'rd{i}.jpg') for i in (1, 2, 3)], reps=14)

if __name__ == '__main__':
    sel = sys.argv[1:] or ['c_unlock', 'c_where', 'c_resize', 'a_days', 'c_redeem']
    for s in sel: globals()[s]()
