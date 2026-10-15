import asyncio
import sys
import traceback
from urllib.parse import urlparse


from crawl import AsyncCrawler


async def crawl_site_async(base_url, max_pages: int, max_conc: int):
    parsed = urlparse(base_url)
    crawler = AsyncCrawler(
        base_url,
        base_domain=parsed.hostname,
        page_data={},
        visited=set(),
        lock=asyncio.Lock(),
        max_concurrency=max_conc,
        max_pages=max_pages,
    )
    async with crawler:
        data = await crawler.crawl()
        return data


async def main():
    arglen = len(sys.argv)
    if arglen > 4:
        print("too many arguments provided")
        sys.exit(1)
    elif arglen < 4:
        print("provide url max_concurrency max_pages")
        sys.exit(1)

    base_url = sys.argv[1]
    max_conc = sys.argv[2]
    max_pages = sys.argv[3]
    print(f"starting crawl of: {base_url}")
    try:
        page_data = await crawl_site_async(
            base_url, max_pages=max_pages, max_conc=max_conc
        )
        print("Crowl done, sties")
        for page in page_data:
            print(page)

    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
