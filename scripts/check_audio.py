import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
  page=await b.new_page(viewport={'width':1440,'height':900})
  await page.goto((Path.cwd()/'ignore/named-presentation/index.html').as_uri())
  assert await page.locator('#narration').is_enabled()
  await page.click('.cover-speaker'); await page.wait_for_timeout(500)
  assert await page.locator('#slide-1 audio').evaluate('(a)=>!a.paused && a.currentTime>0')
  await page.click('#narration')
  assert await page.locator('#slide-1 audio').evaluate('(a)=>a.paused')
  await page.screenshot(path='ignore/audio-controls-cover.png')
  await page.select_option('#page','6')
  assert await page.locator('#page option:checked').inner_text() == '006 \u00b7 Investigating the causes'
  assert not await page.locator('#page').evaluate("e=>/[\u00c2\u00c3\ufffd]/.test(e.textContent)")
  await page.screenshot(path='ignore/updated-slide-006.png')
  await page.select_option('#page','21'); await page.click('#narration'); await page.wait_for_timeout(600)
  assert await page.locator('#slide-21 audio').evaluate('(a)=>!a.paused && a.currentTime>0')
  await page.select_option('#page','22'); assert await page.locator('#narration').is_disabled()
  assert await page.locator('#slide-21 audio').evaluate('(a)=>a.paused')
  await page.select_option('#page','44'); assert await page.locator('#recording option').count()==2
  await page.select_option('#recording','1'); await page.click('#narration'); await page.wait_for_timeout(500)
  assert await page.locator('#slide-44 audio').nth(1).evaluate('(a)=>!a.paused && a.currentTime>0')
  await page.click('#read')
  assert await page.locator('#slide-44 [data-transcript=\"1\"]').is_visible()
  assert not await page.locator('#slide-44 [data-transcript=\"0\"]').is_visible()
  for number, title in [('51', 'FEARS WALLS MAY CRUMBLE'), ('52', 'ANOTHER CHURCH FIRE'), ('73', 'The Cornerstone Story')]:
   await page.select_option('#page',number)
   assert await page.locator('#narration').is_enabled()
   await page.click('#read')
   assert title in await page.locator(f'#slide-{number} .transcript').inner_text()
  await page.select_option('#page','75'); v=page.locator('#slide-75 .slide-canvas video'); await v.evaluate('(v)=>v.play()'); await page.wait_for_timeout(500)
  assert await v.evaluate('(v)=>v.videoWidth===1280 && v.currentTime>0')
  await page.screenshot(path='ignore/audio-controls-video.png')
  await page.click('#fullscreen'); await page.wait_for_timeout(200); assert await page.locator('#fullscreen').get_attribute('aria-label')=='Exit fullscreen'
  await page.click('#fullscreen'); await page.wait_for_timeout(200); assert await page.locator('#fullscreen').get_attribute('aria-label')=='Fullscreen'
  await b.close()
  print('PASS: replacement audio playback, silent continuation, multi-clip slide, video playback, fullscreen icons')
asyncio.run(main())
