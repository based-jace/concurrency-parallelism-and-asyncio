import asyncio
import time
from math import floor
from multiprocessing import cpu_count

import aiofiles
import aiohttp
from bs4 import BeautifulSoup


async def get_and_scrape_pages(num_pages: int, output_file: str):
    """
    Makes {{ num_pages }} requests to Wikipedia to receive {{ num_pages }} random
    articles, then scrapes each page for its title and appends it to {{ output_file }},
    separating each title with a tab: "\\t"

    #### Arguments
    ---
    num_pages: int -
        Number of random Wikipedia pages to request and scrape

    output_file: str -
        File to append titles to
    """
    async with \
    aiohttp.ClientSession() as client, \
    aiofiles.open(output_file, "a+", encoding="utf-8") as f:

        for _ in range(num_pages):
            async with client.get("https://en.wikipedia.org/wiki/Special:Random") as response:
                if response.status > 399:
                    # I was getting a 429 Too Many Requests at a higher volume of requests
                    response.raise_for_status()

                page = await response.text()
                soup = BeautifulSoup(page, features="html.parser")
                title = soup.find("h1").text

                await f.write(title + "\t")

        await f.write("\n")


async def main():
    NUM_PAGES = 100
    OUTPUT_FILE = "./wiki_titles.tsv" # File to append our scraped titles to

    await get_and_scrape_pages(NUM_PAGES, OUTPUT_FILE)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Time to complete: {round(time.time() - start, 2)} seconds.")
