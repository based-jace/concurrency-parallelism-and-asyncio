# Concurrency, Parallelism, and asyncio

## Intro and Overview
*What is concurrency and parallelism, and how do they apply to Python?*

There are many reasons your applications can be slow. Sometimes this is due to poor algorithmic design or the wrong choice of data structure. Sometimes, however, it's due to forces outside of our control, such as hardware constraints or the quirks of networking. That's where concurrency and parallelism fit in. They allow your programs to do multiple things at once, either at the same time, or by wasting the least possible time waiting on busy tasks.

Whether you're dealing with external web resources, reading from and writing to multiple files, or need to use a calculation-intensive function multiple times with different parameters, this post should help you maximize the efficiency and speed of your code.

First we'll delve into what concurrency and parallelism actually are and how they fit into the realm of Python using standard libraries such as threading, multiprocessing, and asyncio. The last portion of the post will compare Python's implementation of these concepts with how other languages have implemented them.

*This post assumes you already know how to work with http requests*

You can find all the code examples from this post in the [concurrency-parallelism-and-asyncio](https://github.com/based-jace/concurrency-parallelism-and-asyncio) repo on GitHub.

## Concurrency
*What is it?*

An effective definition for concurrency is "being able to perform multiple tasks at once," although it may be a bit misleading, as the tasks may-or-may-not actually be performed at exactly the same time. Instead, a process might start, then once it's waiting on a specific instruction to finish, switch to a new task, only to come back once it's no longer waiting. Once one task is finished, it switches again to an unfinished task until they have all been performed. Tasks start asynchronously, get performed asynchronously, and then finish asynchronously. 

If that was confusing to you, let's instead think of an analogy: let's say you want to make a BLT. First, you'll want to throw the bacon in a pan on medium-low heat. **While** the bacon's cooking, you can get out your tomatoes and lettuce and start preparing (washing and cutting) them. All the while, you continue checking on and occasionally flipping over your bacon. 

At this point, you've started a task, and then started and completed two more in the meantime, all while you're still waiting on the first.

Eventually you put your bread in a toaster. While it's toasting, you continue checking on your bacon. As pieces get finished, you pull them out and place them on a plate. Once your bread is done toasting, you apply to it your sandwich spread of choice, and then you can start layering on your tomatoes, lettuce, and then, once it's done cooking, your bacon. Only once everything is cooked, prepared, and layered can you place the last piece of toast onto your sandwich, slice it (optional), and eat it.

Because it requires you to perform multiple tasks at the same time, making a BLT is inherently a concurrent process, even if you are not giving your full attention to each of those tasks all at once. For all intents and purposes, for the next section, we will refer to this form of concurrency as just "concurrency." We will differentiate it later on in this post.

For this reason, concurrency is great for I/O-intensive processes -- tasks that involve waiting on web requests or file read/write operations. 

In Python, there are a few different ways to achieve concurrency. The first we'll take a look at is the threading library. 

*For our examples in this section, we're going to build a small Python program that grabs a random music genre from [Binary Jazz's Genrenator API](https://binaryjazz.us/genrenator-api/) 5 times, prints the genre to the screen, and puts each one into its own file.*

To work with threading in Python, the only import you'll need is `threading`, but for this example, I've also import `urllib` to work with http requests, `time` to determine how long the functions take to complete, and `json` to easily convert the json data returned from the Genrenator API.

Let's start with a simple function:

```python
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
```

Examining the code above, we're making a request to the Genrenator API, loading its JSON response (a random music genre), printing it, then writing it to a file.

*(without the "User-Agent" header you receive a 304)*

What we're really interested in is the next section, where the actual threading happens:

```python
threads = []

for i in range(5):
    thread = threading.Thread(
        target=write_genre, 
        args=[f"./threading/new_file{i}.txt"]
    )
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
```

We first start with a list. We then proceed to iterate 5 times, creating a new thread each time. We then start each thread, append it to our "threads" list, and iterate over our list once more just to join each thread. 

Explanation: Creating threads in Python is easy. 

To create a new thread, use `threading.Thread()`. You can pass into it the kwarg (keyword argument) "target" with a value of whatever function you would like to run on that thread. But only pass in the name of the function, not its value (meaning, for our purposes, `write_genre` and not `write_genre()`). To pass arguments, pass in "kwargs" (which takes a dict) or "args" (which takes an iterable).

Creating a thread is not the same as starting a thread, however. To do that, simply use `{the name of your thread}.start()`. Starting a thread just means starting its execution.

Lastly, when we join threads with `thread.join()`, all we're doing is telling it to make sure the thread has finished before continuing on with our code.

Before we show the potential speed improvement over non-threaded code, I took the liberty of also creating a non-threaded version of the same program (again, available on [GitHub](https://github.com/based-jace/concurrency-parallelism-and-asyncio)). Instead of creating a new thread and joining each one, it instead just calls `write_genre` in a for loop that iterates 5 times. 

*To compare speed benchmarks, I also imported the `time` library to time the execution of our scripts.*

```bash
Starting...
Writing "binary indoremix" to "./sync/new_file0.txt"...
Writing "slavic aggro polka fusion" to "./sync/new_file1.txt"...
Writing "israeli new wave" to "./sync/new_file2.txt"...
Writing "byzantine motown" to "./sync/new_file3.txt"...
Writing "dutch hate industrialtune" to "./sync/new_file4.txt"...
Time to complete synchronous read/writes: 1.42 seconds
```

Running the script, we see that it takes my computer around 1.49 seconds (along with classic music genres such as "dutch hate industrialtune"). Not too bad.

Now let's run the version we just built that uses threading:

```bash
Starting...
Writing "college k-dubstep" to "./threading/new_file2.txt"...
Writing "swiss dirt" to "./threading/new_file0.txt"...
Writing "bop idol alternative" to "./threading/new_file4.txt"...
Writing "ethertrio" to "./threading/new_file1.txt"...
Writing "beach aust shanty français" to "./threading/new_file3.txt"...
Time to complete threading read/writes: 0.77 seconds
```

The first thing that might stand out to you is the functions not being completed in order: 2 - 0 - 4 - 1 - 3

This is because of the asynchronous nature of threading: as one function waits, another one begins, and so on and so forth. Because we're able to continue performing tasks while we're waiting on others to finish (either due to networking or file I/O operations), you might also have noticed that we cut our time in half: 0.76 seconds. Whereas this might not seem like a lot now, imagine the very real case of building a web application that needs to write much more data to a file or interact with much more complex web services. 

*So if threading is so great, why don't we just end the post here?*

Because there are even better ways to perform tasks concurrently. Let's take a look at an example using asyncio. For this method, we're going to install `aiohttp` using pip -- this will allow us to make non-blocking requests and receive responses using the `async`/`await` syntax that will be introduced shortly. It also has the extra benefit of a function that converts a json response without needing to import the json library. We'll also install and import `aiofiles`, which allows non-blocking file operations. Other than `aiohttp` and `aiofiles`, import `asyncio`, which comes with the Python standard library.

*"Non-blocking" means a program doesn't have to wait for the process to complete to continue running. This is opposed to "blocking" code, which encompasses normal, synchronous I/O operations*

Once we have our imports in place, let's take a look at the asynchronous version of the `write_genre` function from our threading example:

```python
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
```

For those not familiar with the `async`/`await` syntax that can be found in many other modern languages, `async` declares that a function, for loop, or with statement **must** be used asynchronously. To call an async function, you must either use the `await` keyword from another async function or call `create_task()` directly from the event loop, which can be grabbed from `asyncio.get_event_loop()`, i.e. `loop = asyncio.get_event_loop()`.

`async with` allows awaiting async responses and file operations.

`async for` (not used here) iterates over an [asynchronous stream](https://stackoverflow.com/questions/56161595/how-to-use-async-for-in-python).

*TODO: Aside about the event loop*

Here's a walkthrough of our function:

We're using `async with` to open our client session asynchronously. The `aiohttp.ClientSession()` class is what allows us to make http requests and remain connected to a source without blocking the running of our code. We then make an async request to the Genrenator API and await the JSON response (a random music genre). In the next line, we use `async with` again with the `aiofiles` library to asynchronously open a new file to write our new genre to. We print the genre, then write it to the file. 

Unlike regular Python scripts, programming with asyncio pretty much enforces using some sort of "main" function. This is because you need to use the "async" keyword in order to use the "await" syntax, and the "await" syntax is the only way to actually perform tasks asynchronously.

*unless you're using the deprecated "yield" syntax with the @asyncio.coroutine decorator, [which will be removed in Python 3.10](https://docs.python.org/3/library/asyncio-task.html).*

Here's our main function:

```python
async def main():
    tasks = []

    for i in range(5):
        tasks.append(write_genre(f"./async/new_file{i}.txt"))

    await asyncio.gather(*tasks)

asyncio.run(main())
```

As you can see, we've declared it with "async." We then create an empty list called "tasks" to house our async tasks (calls to Genrenator and our file I/O). We append our tasks to our list, but they are *not* actually run yet. The calls don't actually get made until we schedule them with `await asyncio.gather(*tasks)`. This runs all of the tasks in our list and waits for them to finish before continuing with therest of our program. Lastly, we use `asyncio.run(main())` to run our "main" function. The `.run()` function is the entry point for our program, [and should only be called once](https://docs.python.org/3/library/asyncio-task.html#running-an-asyncio-program).

*For those not familiar, the * in front of tasks is called "argument unpacking." Just as it sounds, it unpacks our list into a series of arguments for our function. Our function is `asyncio.gather()` in this case*

And that's all we need to do. Now, running our program (the source of which includes the same timing functionality of the synchronous and threading examples)...

```python
Writing "albuquerque fiddlehaus" to "./async/new_file1.txt"...
Writing "euroreggaebop" to "./async/new_file2.txt"...
Writing "shoedisco" to "./async/new_file0.txt"...
Writing "russiagaze" to "./async/new_file4.txt"...
Writing "alternative xylophone" to "./async/new_file3.txt"...
Time to complete asyncio read/writes: 0.71 seconds
```

we see it's even faster still. And, in general, the asyncio method will always be a bit faster than the threading method. This is because when we use the "await" syntax, we essentially tell our program "hold on, I'll be right back," but our program keeps track of how long it takes us to finish what we're doing. Once we're done, our program will know, and will pick back up as soon as it's able. Threading in Python allows asynchronicity, but our program could theoretically skip around different threads that may not yet be ready, wasting time if there are threads ready to continue running.

*So when should I use threading, and when should I use asyncio?*

When you're writing new code, use asyncio. If you're needing to interface with older libraries or those that don't support asyncio, you might be better off with threading.

### Further Reading
If you want to learn more about what distinguishes Python's implementation of threadings vs asyncio, here's a [great article from Medium](https://medium.com/@nhumrich/asynchronous-python-45df84b82434).

For even better examples and explanations of threading in Python, here's [a video by Corey Schafer](https://www.youtube.com/watch?v=IEEhzQoKtQU) that goes more in-depth, including using the `concurrent.futures` library.

Lastly, for a massive deep-dive into asyncio itself, here's [an article from RealPython](https://realpython.com/async-io-python/) completely dedicated to it.

## Parallelism
*What is it?*

Parallelism is very-much related to concurrency. In fact, parallelism is a subset of concurrency: whereas a concurrent process performs multiple tasks at the same time whether they're being diverted total attention or not, a parallel process is physically performing multiple tasks all at the same time. A good example would be driving, listening to music, and eating the BLT we made in the last section. 

Because they don't require a lot of intensive effort, you can do them all at once without having to wait on anything or divert your attention away.


