import asyncio, sys
from playwright.async_api import async_playwright
async def main(src, out):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('file://' + src, wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        await pg.pdf(path=out, format='A4', print_background=True, prefer_css_page_size=False, display_header_footer=False,
                     margin=dict(top='11mm', bottom='9mm', left='18mm', right='18mm'))
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
