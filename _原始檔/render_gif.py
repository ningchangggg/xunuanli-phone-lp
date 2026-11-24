"""把有 data-clip 的區塊逐格截圖 → WORK/gif/secframes/<區塊>/NNN.png；s03b 金光 25 格。
caps_<clip>.json：每格一個 {data-caps 名: innerHTML}。python3 render_gif.py [區塊...]"""
import asyncio, os, sys, shutil, json
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_page import WORK
FR = WORK + '/gif/secframes'
async def main():
    sel = sys.argv[1:]
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='chrome')
        pg = await b.new_page(viewport={'width': 432, 'height': 900}, device_scale_factor=2.5)
        await pg.goto('file://' + WORK + '/page.html'); await pg.wait_for_timeout(800); await pg.evaluate('document.fonts.ready')
        await pg.evaluate("document.getAnimations().forEach(a=>{a.pause();a.currentTime=600})")
        items = await pg.eval_on_selector_all('[data-clip]', 'els=>els.map(e=>[e.closest("section").id,e.dataset.clip])')
        for sec, clip in items:
            if sel and sec not in sel: continue
            od = f'{FR}/{sec}'; shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
            files = sorted(os.listdir(f'{WORK}/gif/clips/{clip}'))
            cf = f'{WORK}/gif/caps_{clip}.json'; caps = json.load(open(cf)) if os.path.exists(cf) else None
            for i, f in enumerate(files):
                url = f'gif/clips/{clip}/{f}'
                await pg.evaluate('''async ([c,u,t])=>{const im=new Image();im.src=u;await im.decode();document.querySelector(`[data-clip="${c}"]`).style.backgroundImage=`url(${u})`;if(t){for(const k in t){document.querySelector(`[data-caps="${k}"]`).innerHTML=t[k]}};await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))}''', [clip, url, caps[i] if caps else None])
                await pg.locator('#' + sec).screenshot(path=f'{od}/{i + 1:03d}.png')
            print(sec, clip, len(files), flush=True)
        if not sel or 's03b' in sel:
            od = f'{FR}/s03b'; shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
            for i in range(25):
                await pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={i * 100}}})")
                await pg.locator('#s03b').screenshot(path=f'{od}/{i + 1:03d}.png')
            print('s03b', 25)
        await b.close()
asyncio.run(main())
