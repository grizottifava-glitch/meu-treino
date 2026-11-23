import asyncio
from playwright.async_api import async_playwright
INIT="""(()=>{const RD=Date; const start=RD.now(); const base=new RD(2026,10,9,20,0,0).getTime();
 const now=()=>base+(RD.now()-start);
 function D(...a){ if(!(this instanceof D)) return new RD(now()).toString(); return a.length? new RD(...a) : new RD(now()); }
 D.prototype=RD.prototype; D.now=now; D.UTC=RD.UTC; D.parse=RD.parse; window.Date=D; })()"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={"width":390,"height":844})
        await ctx.add_init_script(INIT); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        await pg.goto("file:///home/claude/v7.html"); await pg.wait_for_timeout(400)
        await pg.click("#todayBox [data-move='2026-11-09']"); await pg.wait_for_timeout(250)
        await pg.screenshot(path="d1.png")
        await pg.click("[data-mto='2026-11-10']"); await pg.wait_for_timeout(300)
        await pg.click("#todayBox [data-alc='2026-11-09']"); await pg.click("#todayBox [data-alcd='2026-11-09|1']")
        await pg.evaluate("window.scrollTo(0,0)"); await pg.screenshot(path="d2.png")
        await pg.click(".tabs button[data-v='v-cal']"); await pg.wait_for_timeout(200); await pg.screenshot(path="d3.png")
        # swap test: move tuesday(10) to wed(11) -> swap
        await pg.click("#grid [data-open='2026-11-10']"); await pg.click(".sheet [data-move='2026-11-10']"); await pg.click("[data-mto='2026-11-11']"); await pg.wait_for_timeout(300)
        r=await pg.evaluate("JSON.parse(localStorage.getItem('plano-corrida-extra-v1')).runAt")
        print(r)
        await pg.click("#closeSheet")
        await pg.click("#grid [data-open='2026-11-09']"); await pg.click(".sheet [data-undo='2026-11-09']"); await pg.wait_for_timeout(200)
        print(await pg.evaluate("JSON.parse(localStorage.getItem('plano-corrida-extra-v1')).runAt"))
        print(errs); await b.close()
asyncio.run(main())
