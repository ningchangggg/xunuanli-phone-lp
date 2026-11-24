"""手機版煦暖曆落地頁 v8（2026-11-25）：結構照幹話曆新版落地頁（旅行 v28 規範的區塊順序），
視覺語言換成 iPhone 介面（Widget 方塊、毛玻璃對話框、動態島、設定頁、鎖定畫面）。
字一律思源黑體（手機版日曆規則）。產出 WORK/page.html，432 寬。"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = '/private/tmp/claude-501/-Users-ningchang--claude-spares-spare-83sWsf/8be7a878-1d74-40b6-a934-3282ef5f9fed/scratchpad/work'
V = 'v8'

P = [
    dict(n='01', who='怕忘記撕的人', say='日曆好美好想買，<br>可是怕自己忘記撕？很浪費...', img='p1', w='p1_w', wpos='right:14px;bottom:14px', spos='max-width:310px',
         nar='不用撕也不會忘，<mark>解鎖手機</mark>，今天的日曆語錄都已更新好！'),
    dict(n='02', who='喜歡文字的人', say='每天都想讀到，<br>一句剛剛好的話', img='p2', w='p2_w', wpos='right:14px;bottom:14px',
         nar='365 則作家語錄，<mark>滑開手機</mark>剛好講中你那天的心情。'),
    dict(n='03', who='交換禮物', say='朋友在國外，<br>交換禮物寄不過去', img='p3', w='p3_w', wpos='left:14px;bottom:14px',
         nar='轉寄一封兌換碼就送到，他每天<mark>解鎖手機</mark>都會想起你。'),
    dict(n='04', who='聖誕禮物', say='今年聖誕，<br>也想送自己一份禮物', img='p4', w='p4_w', wpos='right:14px;bottom:14px',
         nar='一份<mark>每天都會打開</mark>的禮物，陪你走過 2027 的每一天。'),
]
CAPS6 = ['<small>1 月 1 日</small>這會是美好的一年', '<small>2 月 14 日</small>愛是慢慢散步，慢慢喜歡你',
         '<small>3 月 21 日</small>我祝福我自己，這會是個美好的一年', '<small>9 月 28 日</small>真正的安全感是對自己的信任，允許自己脆弱',
         '<small>11 月 11 日</small>壓力大的時候，深呼吸', '<small>12 月 25 日</small>聖誕快樂']
RD = [('01', '收到 Email', '兌換碼寄到你訂購時填的 Email。'),
      ('02', 'App 輸入兌換碼', '從「我的電子日曆」進入兌換畫面。'),
      ('03', '日曆加入帳號', '2027 年 1 月 1 日起，每天自動開啟。')]

CSS = '''
:root{--bg:#F7F0E6;--bg2:#F1E7DA;--ink:#2B241F;--co:#C96D45;--wine:#7A2136;--gray:#6E6B66;--line:#E4DACB}
*{box-sizing:border-box;margin:0;padding:0}
body{width:432px;font-family:"Noto Sans CJK TC",sans-serif;font-weight:400;color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased}
section{position:relative;background:var(--bg);padding:40px 22px 44px}
.alt{background:var(--bg2)}
.eb{font-size:14px;font-weight:500;color:var(--co);letter-spacing:.16em;text-align:center}
h2{font-weight:500;font-size:28px;line-height:1.44;text-align:center;margin-top:10px;letter-spacing:.02em}
h2 .h2s{font-size:23.5px;letter-spacing:0}
h2 .u,.how h3 .u{background:linear-gradient(transparent 62%,rgba(201,109,69,.26) 62%)}
.lead{font-size:14.5px;line-height:1.8;text-align:center;margin-top:12px;color:var(--gray)}
mark{color:var(--wine);font-weight:500;background:linear-gradient(transparent 60%,rgba(201,109,69,.2) 60%);padding:0 1px}
.en{letter-spacing:.2em;font-weight:700}
.shadow{box-shadow:0 10px 28px rgba(43,36,31,.13)}
/* 受眾卡 */
.ac{position:relative;margin-top:34px}
.ac .tag{position:relative;z-index:3;display:inline-flex;align-items:center;gap:9px;background:var(--ink);color:#fff;border-radius:999px;padding:5px 16px 5px 5px;font-size:19px;font-weight:500;margin:0 0 -16px 10px;box-shadow:0 6px 14px rgba(0,0,0,.18)}
.ac .tag .no{background:var(--wine);border-radius:999px;padding:4px 10px 4px 11px;font-size:11px;letter-spacing:.14em;font-weight:700}
.ac .box{background:#fff;border-radius:28px;overflow:hidden}
.ac .pic{position:relative;height:400px;background-size:cover;background-position:center}
.say{position:absolute;left:14px;top:30px;z-index:2;max-width:250px;padding:11px 16px 12px;border-radius:22px;border-bottom-left-radius:6px;background:rgba(255,255,255,.8);-webkit-backdrop-filter:blur(16px) saturate(1.3);backdrop-filter:blur(16px) saturate(1.3);font-size:18px;line-height:1.45;font-weight:500;box-shadow:0 6px 18px rgba(0,0,0,.14)}
.ac .wd{position:absolute;width:136px;height:136px;z-index:2;filter:drop-shadow(0 10px 16px rgba(0,0,0,.38))}
.ac .nar{padding:17px 16px 18px;font-size:15.5px;line-height:1.7;white-space:nowrap}
/* 檔期 */
#s03b{padding:6px 22px 30px}
.xm{position:relative;overflow:hidden;background:#B83A35;border-radius:22px;padding:20px 12px 22px;text-align:center;color:#fff;box-shadow:0 10px 24px rgba(120,30,30,.25)}
.xm:before{content:"";position:absolute;inset:7px;border:2px solid #E2BE6E;border-radius:16px;pointer-events:none}
.xm .sm{font-size:10px;letter-spacing:.3em;color:#F3D99B}
.xm .big{font-size:33px;font-weight:500;letter-spacing:.1em;margin-top:4px;background:linear-gradient(180deg,#FFF6DA 10%,#F1CF7E 55%,#D9A94A 90%);-webkit-background-clip:text;color:transparent}
.xm .sh{position:absolute;top:-30%;bottom:-30%;width:90px;left:-40%;transform:skewX(-22deg);background:linear-gradient(90deg,transparent,rgba(255,236,180,.55),transparent);animation:sweep 2.5s linear infinite}
.xm .sp{position:absolute;width:14px;height:14px;margin:-7px;opacity:0;background:radial-gradient(circle,#FFF4C8 0 18%,transparent 20%),linear-gradient(0deg,transparent 45%,#FFE7A0 45% 55%,transparent 55%),linear-gradient(90deg,transparent 45%,#FFE7A0 45% 55%,transparent 55%);animation:tw 2.5s linear infinite}
@keyframes sweep{0%{left:-40%}55%{left:120%}100%{left:120%}}
@keyframes tw{0%,100%{opacity:0;transform:scale(.4)}12%{opacity:1;transform:scale(1.15) rotate(20deg)}26%{opacity:0;transform:scale(.4)}}
/* 數字列：Widget 方塊 */
#s04{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:8px 22px 40px}
#s04>div{aspect-ratio:1;background:#fff;border-radius:26px;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(43,36,31,.1)}
#s04>div:nth-child(2){background:var(--wine);color:#fff}
#s04 .n{font-size:40px;font-weight:500;line-height:1;color:var(--wine)}
#s04>div:nth-child(2) .n{color:#fff}
#s04 .n small{font-size:17px;margin-left:2px}
#s04 .c{font-size:13px;margin-top:9px;text-align:center;line-height:1.4}
/* 內頁全貌：Widget 牆 */
.wallp{position:relative;margin-top:24px;border-radius:36px;padding:18px 16px 18px;background:linear-gradient(160deg,#3A2E3A 0%,#2A2533 45%,#1C2633 100%);overflow:hidden;height:560px}
.wallp .g{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.wallp img{width:100%;display:block;filter:drop-shadow(0 4px 8px rgba(0,0,0,.35))}
.wallp:after{content:"";position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(transparent,#1C2633 88%)}
.badge{position:absolute;z-index:3;min-width:30px;height:30px;padding:0 9px;border-radius:999px;background:#FF3B30;color:#fff;font-size:15px;font-weight:700;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(255,59,48,.35)}
.wallp .more{position:absolute;z-index:3;left:0;right:0;bottom:22px;text-align:center;color:#fff;font-size:15px;letter-spacing:.12em;font-weight:500}
/* HOW TO USE */
.how .hd{text-align:center}
.how .no{display:inline-block;background:var(--wine);color:#fff;border-radius:999px;padding:6px 15px;font-size:11.5px}
.how h3{font-weight:500;font-size:27px;line-height:1.44;margin-top:14px}
.how p.d{font-size:14.5px;line-height:1.8;color:var(--gray);margin-top:10px}
.how .pn{position:relative;margin-top:22px;border-radius:28px;overflow:hidden;background:#fff}
.how .ph{height:490px;background-size:cover;background-position:center}
.how .bar{display:flex;align-items:center;gap:10px;background:var(--ink);color:#fff;padding:13px 18px}
.how .bar .st{color:#E9A07F;font-size:12px}
.how .bar .cn{font-size:16px;flex:1;font-weight:500}
.how .bar .ee{font-size:10px;color:#BDB3AA}
.pill{position:absolute;z-index:3;display:flex;align-items:center;gap:7px;padding:8px 14px;border-radius:999px;background:rgba(255,255,255,.82);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);font-size:14px;font-weight:500;box-shadow:0 6px 16px rgba(0,0,0,.16)}
.pill i{width:8px;height:8px;border-radius:50%;background:var(--co)}
/* 一頁拆解 */
#s06 .pn{margin-top:22px;background:#fff;border-radius:28px;overflow:hidden}
#s06 .cap{background:#F4E9E0;padding:11px 12px 12px;height:66px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-size:15px;font-weight:500;line-height:1.4;color:var(--ink)}
#s06 .cap small{font-size:11.5px;letter-spacing:.14em;color:var(--co);font-weight:700}
#s06 .pg{position:relative;height:276px;background-size:236px 236px;background-repeat:no-repeat;background-position:76px 20px}
#s06 .pg:before{content:"";position:absolute;left:76px;top:20px;width:236px;height:236px;border-radius:20px;box-shadow:0 10px 24px rgba(43,36,31,.22)}
#s06 .ln{position:absolute;border-top:1.5px dashed #9C8F84;height:0}
#s06 .lb{position:absolute;width:62px;display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11.5px;font-weight:500;line-height:1.3;text-align:center}
#s06 .lb b{width:22px;height:22px;border-radius:50%;background:var(--wine);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11.5px;font-weight:700}
/* 兌換 */
#s08 .steps{display:flex;justify-content:space-between;padding:16px 18px 6px;background:#fff}
#s08 .st3{flex:1;text-align:center;font-size:12.5px;font-weight:500;color:#B5ACA3}
#s08 .st3 b{display:flex;margin:0 auto 5px;width:26px;height:26px;border-radius:50%;background:#E8E1D8;color:#fff;align-items:center;justify-content:center;font-size:11.5px}
#s08 .st3.on{color:var(--wine)}#s08 .st3.on b{background:var(--wine)}
#s08 .rdw{position:relative;height:350px;background:#fff}
#s08 .rd{position:absolute;left:96px;top:16px;width:196px;height:234px;border-radius:18px;background-size:cover;background-position:center;box-shadow:0 10px 24px rgba(43,36,31,.2)}
#s08 .rdt{position:absolute;left:20px;right:20px;top:272px;text-align:center}
#s08 .rdt .a{font-size:19px;font-weight:500}
#s08 .rdt .b{font-size:14px;color:var(--gray);margin-top:6px;line-height:1.6}
/* 作家 */
#s09 .card{margin-top:22px;background:#fff;border-radius:28px;padding:22px 14px 18px}
#s09 .gr{display:grid;grid-template-columns:repeat(4,1fr);row-gap:16px}
#s09 figure{text-align:center}
#s09 .av{width:72px;height:72px;margin:0 auto;border-radius:50%;background-size:cover;background-position:center 18%;box-shadow:0 4px 10px rgba(43,36,31,.16)}
#s09 figcaption{font-size:12.5px;margin-top:7px;font-weight:500;line-height:1.3}
#s09 .tip{text-align:center;font-size:13px;color:var(--gray);margin-top:16px;padding-top:14px;border-top:1px solid var(--line)}
/* 尺寸 */
#s10 .ph3{display:flex;justify-content:space-between;margin-top:24px}
#s10 figure{width:118px;text-align:center}
#s10 .ip{position:relative;width:118px;height:250px;border-radius:24px;background:#1d1b1c;padding:5px;box-shadow:0 10px 22px rgba(43,36,31,.22)}
#s10 .ip div{width:100%;height:100%;border-radius:19px;background-size:cover;background-position:top center}
#s10 .k{display:flex;flex-direction:column;align-items:center;gap:6px;margin-top:12px;font-size:13px;font-weight:500}
#s10 .k b{width:22px;height:22px;border-radius:6px;background:var(--wine);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px}
#s10 .nt{margin-top:18px;text-align:center;font-size:13.5px;color:var(--gray);background:#fff;border-radius:16px;padding:11px 10px}
/* 規格：設定頁 */
#s11 .set{margin-top:22px;background:#fff;border-radius:22px;overflow:hidden}
#s11 .top{display:flex;align-items:center;justify-content:space-between;padding:14px 18px 12px;border-bottom:1px solid var(--line)}
#s11 .top .a{font-size:13px;color:var(--co);font-weight:500}
#s11 .top .b{font-size:16px;font-weight:500}
#s11 .row{display:flex;gap:12px;padding:12px 18px 12px 0;margin-left:18px;border-bottom:1px solid var(--line);font-size:14.5px;line-height:1.5}
#s11 .row:last-child{border-bottom:none}
#s11 .row .k{width:46px;flex:none;color:var(--ink);font-weight:500}
#s11 .row .v{flex:1;text-align:right;color:var(--gray)}
/* 收尾：鎖定畫面 */
#s12{padding-bottom:48px}
.lock{position:relative;height:640px;border-radius:44px;overflow:hidden;background-size:cover;background-position:center;color:#fff;box-shadow:0 14px 34px rgba(30,24,28,.3);border:6px solid #1d1b1c}
.lock .isl{position:absolute;left:50%;top:12px;width:104px;height:30px;margin-left:-52px;border-radius:999px;background:#000}
.lock .dt{text-align:center;margin-top:62px;font-size:15px;font-weight:500;letter-spacing:.06em;opacity:.92}
.lock .tm{text-align:center;font-size:88px;font-weight:300;line-height:1;margin-top:4px;letter-spacing:-.01em}
.lock .wd{display:block;width:224px;height:224px;margin:24px auto 0;filter:drop-shadow(0 12px 20px rgba(0,0,0,.4))}
.lock .msg{text-align:center;font-size:22px;line-height:1.55;font-weight:500;margin-top:26px;text-shadow:0 2px 10px rgba(0,0,0,.35)}
.lock .bt{position:absolute;bottom:26px;width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.18);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.lock .bt svg{width:22px;height:22px;margin:12px}
.lock .hb{position:absolute;left:50%;bottom:10px;width:128px;height:5px;margin-left:-64px;border-radius:9px;background:rgba(255,255,255,.85)}
.end{display:flex;align-items:center;justify-content:center;gap:10px;margin-top:20px}
.end .en{font-size:10.5px;color:var(--co)}
.end .t{font-size:16px;font-weight:500}
'''

def s03():
    h = '''<section id="s03" class="alt"><div class="eb">誰適合手機版煦暖曆？</div>
<h2>聖誕禮物 x 交換禮物<br><span class="u h2s">遠距離好友也能及時收到的聖誕禮物</span></h2>'''
    for x in P:
        wd = f'<img class="wd" src="img/{x["w"]}.png" style="{x["wpos"]}">' if x['w'] else ''
        h += f'''<div class="ac"><div class="tag"><span class="no en">NO.{x['n']}</span>{x['who']}</div>
<div class="box shadow"><div class="pic" style="background-image:url(img/{x['img']}.jpg)"><div class="say" style="{x.get('spos', '')}">{x['say']}</div>{wd}</div>
<div class="nar">{x['nar']}</div></div></div>'''
    return h + '</section>'

def s03b():
    sp = ''.join(f'<i class="sp" style="left:{x}%;top:{y}%;animation-delay:{d}s"></i>' for x, y, d in
                 [(8, 18, 0), (90, 22, .5), (93, 74, 1.0), (6, 78, 1.5), (50, 8, 2.0)])
    return f'<section id="s03b" class="alt"><div class="xm"><div class="sh"></div>{sp}<div class="en sm">CHRISTMAS ・ INSTANT DELIVERY</div><div class="big">聖誕夜買也來得及</div></div></section>'

def s04():
    return '''<section id="s04" class="alt"><div><div class="n">365</div><div class="c">則作家<br>暖心語錄</div></div>
<div><div class="n">3<small>種</small></div><div class="c">桌面<br>Widget 尺寸</div></div>
<div><div class="n">2<small>系統</small></div><div class="c">iOS<br>Android</div></div></section>'''

def s05():
    imgs = ''.join(f'<img src="img/wall/{k:02d}.png">' for k in range(1, 25))
    return f'''<section id="s05"><div class="eb">從元旦到跨年</div>
<h2>365 天，<br><span class="u">每天都有一句溫柔</span></h2>
<div class="lead">每一天都是一張新的風景，<br>和一位作家寫給今天的話。</div>
<div style="position:relative"><div class="wallp"><div class="g">{imgs}</div><div class="more">每天一張，一年 365 張</div></div>
<div class="badge" style="right:-6px;top:-10px">365</div></div></section>'''

def how(n, sid, h, d, clip, cn, ee, pill, ppos, cls=''):
    return f'''<section id="{sid}" class="how {cls}"><div class="hd"><span class="no en">HOW TO USE {n:02d}</span>
<h3>{h}</h3><p class="d">{d}</p></div>
<div class="pn shadow"><div class="ph" data-clip="{clip}" style="background-image:url(gif/clips/{clip}/001.jpg)"></div>
<div class="pill" style="{ppos}"><i></i>{pill}</div>
<div class="bar"><span class="st en">STEP {n:02d}</span><span class="cn">{cn}</span><span class="ee en">{ee}</span></div></div></section>'''

def s06():
    LB = [('l', 26, '1', '月份'), ('r', 26, '2', '節氣<br>倒數日'), ('l', 70, '3', '日期'),
          ('r', 98, '4', '今日指南'), ('l', 150, '5', '作家語錄'), ('r', 206, '6', '作者出處')]
    lbs = ''
    for side, y, n, t in LB:
        y += 20
        if side == 'l': lbs += f'<span class="lb" style="left:4px;top:{y - 12}px"><b>{n}</b>{t}</span><i class="ln" style="left:62px;width:18px;top:{y}px"></i>'
        else: lbs += f'<span class="lb" style="right:4px;top:{y - 12}px"><b>{n}</b>{t}</span><i class="ln" style="right:62px;width:18px;top:{y}px"></i>'
    return f'''<section id="s06" class="alt"><div class="eb">一張 Widget 有什麼？</div>
<h2>一天一句，<br><span class="u">剛好接住今天的你</span></h2>
<div class="pn shadow"><div class="cap" data-caps="a_days">{CAPS6[0]}</div>
<div class="pg" data-clip="a_days" style="background-image:url(gif/clips/a_days/001.png)">{lbs}</div></div></section>'''

def s08():
    def steps(k): return ''.join(f'<div class="st3{" on" if i == k else ""}"><b>{a}</b>{b}</div>' for i, (a, b, _) in enumerate(RD))
    def txt(k): return f'<div class="a">{RD[k][1]}</div><div class="b">{RD[k][2]}</div>'
    caps = []
    for k in range(3): caps += [{'c_redeem_s': steps(k), 'c_redeem_t': txt(k)}] * 14
    json.dump(caps, open(f'{WORK}/gif/caps_c_redeem.json', 'w'), ensure_ascii=False)
    return f'''<section id="s08" class="how"><div class="hd"><span class="no en">HOW TO USE 04</span>
<h3>一封信，<br>帶你完成兌換</h3><p class="d">付款後 Email 收到兌換碼，<br>在煦暖曆 App 輸入就完成。</p></div>
<div class="pn shadow"><div class="steps" data-caps="c_redeem_s">{steps(0)}</div>
<div class="rdw"><div class="rd" data-clip="c_redeem" style="background-image:url(gif/clips/c_redeem/001.png)"></div><div class="rdt" data-caps="c_redeem_t">{txt(0)}</div></div>
<div class="bar"><span class="st en">STEP 04</span><span class="cn">完成兌換</span><span class="ee en">REDEEM</span></div></div></section>'''

def s09():
    W = ['Queenie Kao', '周慕姿', '喬心誌', '林達陽', '沈希默', '知寒', '連俞涵', '陳繁齊']
    gr = ''.join(f'<figure><div class="av" style="background-image:url(img/au{i + 1}.jpg)"></div><figcaption>{n}</figcaption></figure>' for i, n in enumerate(W))
    return f'''<section id="s09"><div class="eb">作家陣容</div>
<h2>他們為了 2027 的你，<br>預備這段話</h2>
<div class="lead">365 位作家，用最深刻的體悟，<br>陪你走過未來每一天。</div>
<div class="card shadow"><div class="gr">{gr}</div><div class="tip">還有更多作家與好書摘句，一起陪你 365 天</div></div></section>'''

def s10():
    K = [('S', '小', '保留桌面空間'), ('M', '中', '語錄清楚展開'), ('L', '大', '完整閱讀每日內容')]
    ph = ''.join(f'<figure><div class="ip"><div style="background-image:url(img/scr_{a}.png)"></div></div><div class="k"><b>{b}</b>{c}</div></figure>' for a, b, c in K)
    return f'''<section id="s10" class="alt"><div class="eb">桌面尺寸</div>
<h2>三種尺寸，<br><span class="u">挑一個最適合你的桌面</span></h2>
<div class="ph3">{ph}</div>
<div class="nt">Android 依裝置與桌面配置，自由選擇比例</div></section>'''

def s11():
    rows = [('名稱', '2027 手機版煦暖曆'), ('內容', '365 則作家暖心語錄'), ('開放', '2027 年 1 月 1 日起，每天開放一頁'),
            ('尺寸', 'iOS 小・中・大<br>Android 依裝置選擇比例'), ('支援', 'iOS 16.4、Android 7.0 以上'),
            ('兌換', '付款後 Email 寄送兌換碼'), ('購買', '一次買斷，不是訂閱制'), ('回顧', '年度結束後，仍可在 App 回顧')]
    rr = ''.join(f'<div class="row"><span class="k">{a}</span><span class="v">{b}</span></div>' for a, b in rows)
    return f'''<section id="s11"><div class="eb">規格</div>
<h2>買一次，<br><span class="u">陪你一整年</span></h2>
<div class="set shadow"><div class="top"><span class="a">‹ 一般</span><span class="b">關於本日曆</span><span style="width:40px"></span></div>{rr}</div></section>'''

def s12():
    fl = '<svg viewBox="0 0 24 24" fill="#fff"><path d="M8 2h8v4l-2 3v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V9L8 6z"/></svg>'
    cam = '<svg viewBox="0 0 24 24" fill="#fff"><path d="M9 4h6l1.5 2H20a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h3.5z"/><circle cx="12" cy="13" r="3.6" fill="#555"/></svg>'
    return f'''<section id="s12" class="alt"><div class="lock" style="background-image:url(img/lock_bg.jpg)"><div class="isl"></div>
<div class="dt">1月1日 星期五</div><div class="tm">7:30</div>
<img class="wd" src="img/lock_w.png"><div class="msg">日曆會忘記撕，<br>手機卻不會忘記開。</div>
<div class="bt" style="left:30px">{fl}</div><div class="bt" style="right:30px">{cam}</div><div class="hb"></div></div>
<div class="end"><span class="en">TO BE CONTINUED</span><span class="t">明天，還有一句</span></div></section>'''

def build():
    os.makedirs(f'{WORK}/gif', exist_ok=True)
    json.dump([{'a_days': c} for c in CAPS6 for _ in range(12)], open(f'{WORK}/gif/caps_a_days.json', 'w'), ensure_ascii=False)
    body = (s03() + s03b() + s04() + s05()
        + how(1, 's05a', '早上解鎖手機，<br>今天那一句已經換好', '不用撕，也不怕忘，<br>每天打開手機就看得到。', 'c_unlock', '打開手機', 'UNLOCK', '每天自動更新', 'right:14px;top:14px')
        + s06()
        + how(2, 's06a', '長按 Widget，<br>換一個喜歡的大小', 'iOS 小、中、大三種尺寸，<br>Android 依桌面自由調整比例。', 'c_resize', '換尺寸', 'RESIZE', '長按就能換', 'left:14px;top:14px', 'alt')
        + how(3, 's07', '上班、出差、午休，<br>打開手機就看得到', '不用帶厚厚的紙本，<br>日曆跟著手機去任何地方。', 'c_where', '隨身帶著', 'ANYWHERE', '在哪都看得到', 'right:14px;top:14px')
        + s08() + s09() + s10() + s11() + s12())
    # 說明句一行放不下就四張一起縮（同一個字級）
    body += "<script>(()=>{const n=[...document.querySelectorAll('.ac .nar')];let f=15.5;const ok=()=>n.every(e=>e.scrollWidth<=e.clientWidth);while(!ok()&&f>12){f-=.1;n.forEach(e=>e.style.fontSize=f+'px')}document.body.dataset.narfs=f.toFixed(1)})()</script>"
    html = f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=432"><title>手機版煦暖曆落地頁 {V}</title><style>{CSS}</style></head><body>{body}</body></html>'
    open(f'{WORK}/page.html', 'w').write(html)
    print('ok')

if __name__ == '__main__':
    build()
