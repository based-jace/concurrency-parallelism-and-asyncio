import concurrent.futures, urllib.request
from multiprocessing import cpu_count
from bs4 import BeautifulSoup
from math import floor

import time

def get_and_scrape_pages(num_pages: int, output_file: str):
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
    with open(output_file, "a+", encoding="utf-8") as f:
        for _ in range(num_pages):
            with urllib.request.urlopen('https://en.wikipedia.org/wiki/Special:Random') as response:
                if response.status > 399:
                    # I was getting a 429 Too Many Requests at a higher volume of requests
                    raise Exception(f'Received a {response.status} instead of 200.')

                page = response.read()
                soup = BeautifulSoup(page, features="html.parser")
                title = soup.find("h1").text
                f.write(title + "\t")

        f.write("\n")

def main():
    NUM_PAGES = 100 # Number of pages to scrape altogether
    NUM_CORES = cpu_count() # Our number of CPU cores (including logical cores)
    OUTPUT_FILE = "./wiki_titles.tsv" # File to append our scraped titles to

    PAGES_PER_CORE = floor(NUM_PAGES / NUM_CORES)
    PAGES_FOR_FINAL_CORE = PAGES_PER_CORE + NUM_PAGES % PAGES_PER_CORE # For our final core

    futures = []
    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
        for i in range(NUM_CORES - 1):
            new_future = executor.submit(
                get_and_scrape_pages, # Function to perform
                # v Arguments v
                num_pages=PAGES_PER_CORE,
                output_file=OUTPUT_FILE,
            )
            futures.append(new_future)

        futures.append(
            executor.submit(
                get_and_scrape_pages,
                PAGES_FOR_FINAL_CORE, OUTPUT_FILE
            )
        )

    concurrent.futures.wait(futures)

if __name__ == "__main__":
    start = time.time()
    main()
    print(f'Time to complete: {round(time.time() - start, 2)} seconds.')
