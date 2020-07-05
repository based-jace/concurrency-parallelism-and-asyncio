import time
from urllib.request import Request, urlopen
import json
import threading

def write_genre(file_name):
    """
    Uses genrenator from binaryjazz.us to write a random genre to the
    name of the given file
    """

    req = Request("https://binaryjazz.us/wp-json/genrenator/v1/genre/", headers={'User-Agent': 'Mozilla/5.0'})
    genre = json.load(urlopen(req))

    with open(file_name, "w") as new_file:
        print(f'Writing "{genre}" to "{file_name}"...')
        new_file.write(genre)

threads = []

print("Starting...")
start = time.time()

for i in range(5):
    thread = threading.Thread(
        target=write_genre,
        args=[f"./threading/new_file{i}.txt"]
    )
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()
print(f"Time to complete threading read/writes: {round(end - start, 2)} seconds")
