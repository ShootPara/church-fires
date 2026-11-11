import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"ignore/slide-review"
OUT.mkdir(exist_ok=True)
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",headless=True)
        page=await browser.new_page(viewport={"width":1440,"height":900})
        await page.goto((ROOT/"ignore/named-presentation/index.html").as_uri())
        for n in range(1,102):
            await page.select_option("#page",str(n))
            await page.locator(f"#slide-{n} .slide-canvas img").evaluate_all("(images)=>Promise.all(images.map(i=>i.decode().catch(()=>{})))")
            await page.locator(f"#slide-{n} .slide-canvas").screenshot(path=str(OUT/f"{n:03}.png"))
        await browser.close()
    for start in range(1,102,12):
        sheet=Image.new("RGB",(1440,6*230),"#ddd")
        draw=ImageDraw.Draw(sheet)
        for i,n in enumerate(range(start,min(start+12,102))):
            x=(i%2)*720;y=(i//2)*230
            draw.text((x+4,y+2),f"{n:03} PDF / delivered",fill="black")
            for j,path in enumerate([ROOT/f"ignore/extraction/presentation/page-{n:03}.png",OUT/f"{n:03}.png"]):
                im=Image.open(path).convert("RGB");im.thumbnail((352,198))
                sheet.paste(im,(x+j*360,y+22))
        sheet.save(OUT/f"pairs-{start:03}.jpg")
asyncio.run(main())
