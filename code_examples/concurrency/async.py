import time
import asyncio
import aiohttp
import aiofiles

async def write_genre(file_name):
    """
    Uses genrenator from binaryjazz.us to write a random genre to the
    name of the given file
    """

    async with aiohttp.ClientSession() as session:
        async with session.get("https://binaryjazz.us/wp-json/genrenator/v1/genre/") as response:
            genre = await response.json()

    async with aiofiles.open(file_name, "w") as new_file:
        print(f'Writing "{genre}" to "{file_name}"...')
        await new_file.write(genre)

async def main():
    tasks = []

    print("Starting...")
    start = time.time()

    for i in range(5):
        tasks.append(write_genre(f"./async/new_file{i}.txt"))

    await asyncio.gather(*tasks)

    end = time.time()
    print(f"Time to complete asyncio read/writes: {round(end - start, 2)} seconds")

asyncio.run(main())