from urllib.parse import urlparse

import asyncio
import aiohttp

from utils import PageData, extract_page_data


class AsyncCrawler:
    def __init__(
        self,
        base_url: str,
        base_domain: str,
        page_data: PageData,
        visited: set[str],
        lock: asyncio.Lock,
        max_concurrency: int,
        max_pages: int,
    ) -> None:
        self.base_url = base_url
        self.base_domain = base_domain
        self.page_data = page_data
        self.visited = visited
        self.lock = lock
        self.max_concurrency = max_concurrency
        self.max_page = max_pages

        self.should_stop = False
        self.semaphore = asyncio.Semaphore(value=int(self.max_concurrency))
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        if self.should_stop:
            return False

        async with self.lock:
            if normalized_url in self.visited:
                return False
            else:
                self.visited.add(normalized_url)
                if len(self.visited) >= int(self.max_page):
                    self.should_stop = True
                    print("Reached maximum number of pages to crawl")
                return True

    async def get_html(self, url):
        print(f"Requesting: {url}")
        try:
            headers = {"User-Agent": "BootCrawler/1.0"}
            async with self.session.get(url, headers=headers) as res:
                if res.status >= 400:
                    print("debug")
                    print(res)
                    raise Exception("Request failed")

                res_content_type = res.headers.get("Content-Type", "")
                if "text/html" not in res_content_type:
                    raise Exception("Malformed response")

                return await res.text()
        except Exception as e:
            print(f"Exception: {e}")
            return None

    async def crawl_page(self, current_url=None):

        if self.should_stop:
            return self.page_data

        # check if the base url and the current url are on same domain
        parsed_current_url = urlparse(current_url)
        current_domain = parsed_current_url.hostname
        if self.base_domain != current_domain:
            return self.page_data
        # check the cache
        normalized_current_url = (
            f"{parsed_current_url.hostname}{parsed_current_url.path}"
        )
        should_visit = await self.add_page_visit(normalized_current_url)
        if not should_visit:
            return self.page_data

        async with self.semaphore:
            current_html = await self.get_html(current_url)
            if current_html is None:
                return self.page_data
            current_data = extract_page_data(current_html, current_url)
        async with self.lock:
            self.page_data[normalized_current_url] = current_data

        tasks = []
        for link in current_data["outgoing_links"]:
            tasks.append(asyncio.create_task(self.crawl_page(link)))

        await asyncio.gather(*tasks)

        return self.page_data

    async def crawl(self):
        page_data = await self.crawl_page(self.base_url)
        return page_data
