# Concurrency, Parallelism, and asyncio

## Intro and Overview
*What are concurrency and parallelism, and how do they apply to Python?*

There are many reasons your applications can be slow. Sometimes this is due to poor algorithmic design or the wrong choice of data structure. Sometimes, however, it's due to forces outside of our control, such as hardware constraints or the quirks of networking. That's where concurrency and parallelism fit in. They allow your programs to do multiple things at once, either at the same time or by wasting the least possible time waiting on busy tasks.

Whether you're dealing with external web resources, reading from and writing to multiple files, or need to use a calculation-intensive function multiple times with different parameters, this post should help you maximize the efficiency and speed of your code.

First, we'll delve into what concurrency and parallelism are and how they fit into the realm of Python using standard libraries such as threading, multiprocessing, and asyncio. The last portion of this post will compare Python's implementation of `async`/`awai` with how other languages have implemented them.

*This post assumes you already know how to work with HTTP requests*

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

To work with threading in Python, the only import you'll need is `threading`, but for this example, I've also imported `urllib` to work with HTTP requests, `time` to determine how long the functions take to complete, and `json` to easily convert the json data returned from the Genrenator API.

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

*Without the "User-Agent" header you will receive a 304.*

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

We first start with a list. We then proceed to iterate 5 times, creating a new thread each time. Next, we start each thread, append it to our "threads" list, and then iterate over our list one last time to join each thread. 

Explanation: Creating threads in Python is easy. 

To create a new thread, use `threading.Thread()`. You can pass into it the kwarg (keyword argument) "target" with a value of whatever function you would like to run on that thread. But only pass in the name of the function, not its value (meaning, for our purposes, `write_genre` and not `write_genre()`). To pass arguments, pass in "kwargs" (which takes a dict of your kwargs) or "args" (which takes an iterable containing your args -- in this case a list).

Creating a thread is not the same as starting a thread, however. To start your thread, use `{the name of your thread}.start()`. Starting a thread means "starting its execution."

Lastly, when we join threads with `thread.join()`, all we're doing is ensuring the thread has finished before continuing on with our code.

### Threads
*But what exactly is a thread?*

A thread is a way of allowing your computer to break up a single process/program into many lightweight pieces that execute in parallel. Somewhat confusingly, Python's standard implementation of threading limits threads to only being able to execute one at a time due to something called the Global Interpreter Lock (GIL). The GIL is necessary because CPython's (Python's default implementation) memory management is not thread-safe. Because of this limitation, threading in Python is concurrent, but not parallel. To get around this, Python has a separate `multiprocessing` module not limited by the GIL that spins up separate processes, enabling parallel execution of your code. Using the `multiprocessing` module is nearly identical to using the `threading` module.

*More info about Python's GIL and thread safety can be found on [Real Python](https://realpython.com/python-gil/) and Python's [official docs](https://docs.python.org/2.0/api/threads.html).*

*We'll take a more in-depth look at multiprocessing in Python shortly.*

Before we show the potential speed improvement over non-threaded code, I took the liberty of also creating a non-threaded version of the same program (again, available on [GitHub](https://github.com/based-jace/concurrency-parallelism-and-asyncio)). Instead of creating a new thread and joining each one, it instead calls `write_genre` in a for loop that iterates 5 times. 

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

Upon running the script, we see that it takes my computer around 1.49 seconds (along with classic music genres such as "dutch hate industrialtune"). Not too bad.

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

This is because of the asynchronous nature of threading: as one function waits, another one begins, and so on. Because we're able to continue performing tasks while we're waiting on others to finish (either due to networking or file I/O operations), you may also have noticed that we cut our time roughly in half: 0.76 seconds. Whereas this might not seem like a lot now, it's easy to imagine the very real case of building a web application that needs to write much more data to a file or interact with much more complex web services. 

*So, if threading is so great, why don't we end the post here?*

Because there are even better ways to perform tasks concurrently. Let's take a look at an example using asyncio. For this method, we're going to install `aiohttp` using `pip`. This will allow us to make non-blocking requests and receive responses using the `async`/`await` syntax that will be introduced shortly. It also has the extra benefit of a function that converts a JSON response without needing to import the `json` library. We'll also install and import `aiofiles`, which allows non-blocking file operations. Other than `aiohttp` and `aiofiles`, import `asyncio`, which comes with the Python standard library.

*"Non-blocking" means a program will allow other threads to continue running while it's waiting. This is opposed to "blocking" code, which stops execution of your program completely. Normal, synchronous I/O operations suffer from this limitation.*

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

For those not familiar with the `async`/`await` syntax that can be found in many other modern languages, `async` declares that a function, `for` loop, or `with` statement **must** be used asynchronously. To call an async function, you must either use the `await` keyword from another async function or call `create_task()` directly from the event loop, which can be grabbed from `asyncio.get_event_loop()`, i.e. `loop = asyncio.get_event_loop()`.

`async with` allows awaiting async responses and file operations.

`async for` (not used here) iterates over an [asynchronous stream](https://stackoverflow.com/questions/56161595/how-to-use-async-for-in-python).

### The Event Loop
Event loops are constructs inherent to asynchronous programming that allow performing tasks asynchronously. As you're reading this article, I can safely assume you're probably not too familiar with the concept. However, even if you've never written an async application, you have experience with event loops every time you use a computer. Whether your computer is listening for keyboard input, you're playing online multiplayer games, or you're browsing Reddit while you have files copying in the background, an event loop is the driving force that keeps everything working smoothly and efficiently. In its purest essence, an event loop is a process that waits around for triggers and then performs specific (programmed) actions once those triggers are met. They often return a "promise" (JavaScript syntax) or "future" (Python syntax) of some sort to denote that a task has been added. Once the task is finished, the promise or future returns a value passed back from the called function (assuming the function does return a value).

The idea of performing a function in response to another function is called a "callback."

*For another take on callbacks and events, [here's a great answer on StackOverflow](https://stackoverflow.com/questions/9596276/how-to-explain-callbacks-in-plain-english-how-are-they-different-from-calling-o/9652434#9652434).*

Here's a walkthrough of our function:

We're using `async with` to open our client session asynchronously. The `aiohttp.ClientSession()` class is what allows us to make HTTP requests and remain connected to a source without blocking the execution of our code. We then make an async request to the Genrenator API and await the JSON response (a random music genre). In the next line, we use `async with` again with the `aiofiles` library to asynchronously open a new file to write our new genre to. We print the genre, then write it to the file. 

Unlike regular Python scripts, programming with asyncio pretty much enforces using some sort of "main" function. This is because you need to use the "async" keyword in order to use the "await" syntax, and the "await" syntax is the only way to actually run other async functions.

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

As you can see, we've declared it with "async." We then create an empty list called "tasks" to house our async tasks (calls to Genrenator and our file I/O). We append our tasks to our list, but they are *not* actually run yet. The calls don't actually get made until we schedule them with `await asyncio.gather(*tasks)`. This runs all of the tasks in our list and waits for them to finish before continuing with the rest of our program. Lastly, we use `asyncio.run(main())` to run our "main" function. The `.run()` function is the entry point for our program, [and it should generally only be called once](https://docs.python.org/3/library/asyncio-task.html#running-an-asyncio-program).

*For those not familiar, the * in front of tasks is called "argument unpacking." Just as it sounds, it unpacks our list into a series of arguments for our function. Our function is `asyncio.gather()` in this case*

And that's all we need to do. Now, running our program (the source of which includes the same timing functionality of the synchronous and threading examples)...

```bash
Writing "albuquerque fiddlehaus" to "./async/new_file1.txt"...
Writing "euroreggaebop" to "./async/new_file2.txt"...
Writing "shoedisco" to "./async/new_file0.txt"...
Writing "russiagaze" to "./async/new_file4.txt"...
Writing "alternative xylophone" to "./async/new_file3.txt"...
Time to complete asyncio read/writes: 0.71 seconds
```

we see it's even faster still. And, in general, the asyncio method will always be a bit faster than the threading method. This is because when we use the "await" syntax, we essentially tell our program "hold on, I'll be right back," but our program keeps track of how long it takes us to finish what we're doing. Once we're done, our program will know, and will pick back up as soon as it's able. Threading in Python allows asynchronicity, but our program could theoretically skip around different threads that may not yet be ready, wasting time if there are threads ready to continue running.

*So when should I use threading, and when should I use asyncio?*

When you're writing new code, use asyncio. If you need to interface with older libraries or those that don't support asyncio, you might be better off with threading.

### Testing asyncio with Pytest
It turns out testing async functions with Pytest is as easy as testing synchronous functions. Just install the `pytest-asyncio` package with `pip`, mark your tests with the `async` keyword, and apply a decorator that lets `pytest` know it's asynchronous: `@pytest.mark.asyncio`. Let's look at an example. 

First, let's write an arbitrary async function in a file called "hello_asyncio.py"

```python
import asyncio # Make sure this is imported

async def say_hello(name: str):
    """ Sleeps for two seconds, then prints 'Hello, {{ name }}!' """
    try:
        if type(name) != str:
            raise TypeError('"name" must be a string')
        if name == "":
            raise ValueError('"name" cannot be empty')
    except (TypeError, ValueError):
        raise
    
    print('Sleeping...')
    await asyncio.sleep(2)
    print(f"Hello, {name}!")
```

The function takes a single string argument: "name." Upon ensuring that "name" is a string with a length greater than 1, our function asynchronously sleeps for two seconds, then prints "Hello, {name}!" to the console. 

*The difference between `asyncio.sleep()` and `time.sleep()` is that `asyncio.sleep()` is non-blocking.*

Now let's test it with Pytest. In the same directory as "hello_asyncio.py," create a file called "test_hello_asyncio.py," then open it in your favorite text editor.

Let's start with our imports:

```python
import pytest # Note: pytest-asyncio does not require a separate import
import asyncio

from hello_asyncio import say_hello
```

Then we'll create a test with proper input:

```python
@pytest.mark.parametrize('name', [
    'Robert Paulson',
    'Seven of Nine',
    'x Æ a-12'
])
@pytest.mark.asyncio
async def test_say_hello(name):
    await say_hello(name)
```

Things to note:
* The `@pytest.mark.asyncio` decorator - this lets Pytest work asynchronously
* Our test uses the `async` syntax
* We're `await`ing our async function as we would if we were running it outside of a test

Now let's run our test with the verbose `-v` option:

```bash
pytest -v
...
collected 3 items

test_hello_asyncio.py::test_say_hello[Robert Paulson] PASSED    [ 33%]
test_hello_asyncio.py::test_say_hello[Seven of Nine] PASSED     [ 66%]
test_hello_asyncio.py::test_say_hello[x \xc6 a-12] PASSED       [100%]
```

Looks good. Next we'll write a couple of tests with bad input. Back inside of "test_hello_asyncio.py," let's create a class called "TestSayHelloThrowsExceptions" 

```python
class TestSayHelloThrowsExceptions:
    @pytest.mark.parametrize('name', [
        '', 
    ])
    @pytest.mark.asyncio
    async def test_say_hello_value_error(self, name):
        with pytest.raises(ValueError):
            await say_hello(name)

    @pytest.mark.parametrize('name', [
        19,
        {'name', 'Diane'},
        []
    ])
    @pytest.mark.asyncio
    async def test_say_hello_type_error(self, name):
        with pytest.raises(TypeError):
            await say_hello(name)
```

Again, we decorate our tests with `@pytest.mark.asyncio`, mark our tests with the `async` syntax, then call our function with `await`.

Running our tests again:

```bash
pytest -v
...
collected 7 items

test_hello_asyncio.py::test_say_hello[Robert Paulson] PASSED                                    [ 14%]
test_hello_asyncio.py::test_say_hello[Seven of Nine] PASSED                                     [ 28%]
test_hello_asyncio.py::test_say_hello[x \xc6 a-12] PASSED                                       [ 42%]
test_hello_asyncio.py::TestSayHelloThrowsExceptions::test_say_hello_value_error[] PASSED        [ 57%]
test_hello_asyncio.py::TestSayHelloThrowsExceptions::test_say_hello_type_error[19] PASSED       [ 71%]
test_hello_asyncio.py::TestSayHelloThrowsExceptions::test_say_hello_type_error[name1] PASSED    [ 85%]
test_hello_asyncio.py::TestSayHelloThrowsExceptions::test_say_hello_type_error[name2] PASSED    [100%]
```

*If you're interested, here's [a more advanced tutorial on asyncio testing](https://stefan.sofa-rockers.org/2016/03/10/advanced-asyncio-testing/)*

### Further Reading
If you want to learn more about what distinguishes Python's implementation of threading vs asyncio, here's a [great article from Medium](https://medium.com/@nhumrich/asynchronous-python-45df84b82434).

For even better examples and explanations of threading in Python, here's [a video by Corey Schafer](https://www.youtube.com/watch?v=IEEhzQoKtQU) that goes more in-depth, including using the `concurrent.futures` library.

Lastly, for a massive deep-dive into asyncio itself, here's [an article from Real Python](https://realpython.com/async-io-python/) completely dedicated to it.

## Parallelism
*What is it?*

Parallelism is very-much related to concurrency. In fact, parallelism is a subset of concurrency: whereas a concurrent process performs multiple tasks at the same time whether they're being diverted total attention or not, a parallel process is physically performing multiple tasks all at the same time. A good example would be driving, listening to music, and eating the BLT we made in the last section. 

Because they don't require a lot of intensive effort, you can do them all at once without having to wait on anything or divert your attention away. 

Now let's take a look at how to implement this in Python. We could use the `multiprocessing` library, but let's use the `concurrent.futures` library instead -- it eliminates the need to manage your number of process manually. Because the major benefit of multiprocessing happens when you perform multiple cpu-heavy tasks, we're going to compute the squares of 1 million (1000000) to 1 million and 16 (1000016).

The only import we'll need is `concurrent.futures`.

```python
import concurrent.futures

if __name__ == "__main__":
    pow_list = [i for i in range(1000000, 1000016)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(pow, i, i) for i in pow_list]

    for f in concurrent.futures.as_completed(futures):
        print('okay')
```

Because I'm developing on a Windows machine, I'm using `if __name__ == "main"`. This is necessary because Windows does not have the `fork` system call [inherent to Unix systems](https://stackoverflow.com/questions/57535979/concurrent-future-fails-on-windows). Because Windows doesn't have this capability, it resorts to launching a new interpreter with each process that tries to import the main module. If the main module doesn't exist, it reruns your entire program, causing recursive chaos to ensue.

So taking a look at our main function, we use list comprehension to create a list from 1 million to 1 million and 16, we open a ProcessPoolExecutor with concurrent.futures, and we use list comprehension and `ProcessPoolExecutor().submit()` to start executing our processes and throwing them into a list called "futures." 

*We could also use `ThreadPoolExecutor()` if we wanted to use threads instead -- concurrent.futures is versatile.*

And this is where the asynchronicity comes in: The "results" list does not actually contain the results from running our functions. Instead, it contains "futures" which are similar to the JavaScript idea of "promises." In order to allow our program to continue running, we get back these futures that represent a placeholder for a value. If we try to print the future, depending on whether it's finished running or not, we will either get back a state of "pending" or "finished." Once it's finished we can get the return value (assuming there is one) using `var.result()`. In this case, our var will be "result." 

We then iterate through our list of futures, but instead of printing our values, we are simply printing out "okay." This is just because of how massive the resulting calculations come out to be.

Just as before, I built a comparison script that does this synchronously. And, just as before, [you can find it on GitHub](https://github.com/based-jace/concurrency-parallelism-and-asyncio).

Running our control program, which also includes functionality for timing our program, we get:

```bash
Starting...
okay
...
okay
Time to complete: 54.64
```

Wow. 54.64 seconds is quite a long time. Let's see if our version with multiprocessing does any better:

```bash
Starting...
okay
...
okay
Time to complete: 6.24
```

Our time has been *significantly* reduced. We're at about 1/9th of our original time.

*So what would happen if we used threading for this instead?*

I'm sure you can guess -- it wouldn't be much faster. In fact, it might be slower because it still takes a little time and effort to spin up new threads. But don't take my word for it, here's what we get when we replace `ProcessPoolExecutor()` with `ThreadPoolExecutor()`:

```bash
Starting...
okay
...
okay
Time to complete: 53.83
```

As I mentioned earlier, threading allows your applications to focus on new tasks while others are waiting. In this case, we're never sitting idly by. Multiprocessing, on the other hand, spins up totally new services, usually on separate CPU cores, ready to do whatever you ask it completely in tandem with whatever else your script is doing. This is why the multiprocessing version taking roughly 1/9th of the time makes sense -- I have 8 cores in my CPU.

Now that we've talked about concurrency and parallelism in Python, we can finally set the terms straight. If you're have trouble distinguish the terms, you can safely and accurately think of our previous definitions of "parallelism" and "concurrency" as "parallel concurrency" and  "non-parallel concurrency" respectively.

### Further Reading
Real Python has a great article on [concurrency vs parallelism](https://realpython.com/python-concurrency/).

Engineer Man has a good video comparison of [threading vs multiprocessing](https://www.youtube.com/watch?v=ecKWiaHCEKs).

Corey Schafer also has a good [video on multiprocessing](https://www.youtube.com/watch?v=fKl2JW_qrso&t=127s) in the same spirit as his threading video.

*Recap: When to use multiprocessing vs asyncio or threading*

Use multiprocessing when you need to do many heavy calculations and you can split them up. Use asyncio or threading when you're performing I/O operations -- communicating with external resources or reading/writing from/to files.

## Async/Await in Other Languages
`async`/`await` and similar syntax also exist in other languages, and in some of those languages, its implementation can differ drastically.

### .NET: F# to C#
The first programming language (back in 2007) to use the `async` syntax was Microsoft's F#. Whereas it doesn't exactly use `await` to wait on a function call, it uses specific syntax like `let!` and `do!` along with proprietary `Async` functions included in the `System` module.

*You can find more about async programming in F# on [Microsoft's F# docs](https://docs.microsoft.com/en-us/dotnet/fsharp/tutorials/asynchronous-and-concurrent-programming/async)*

Their C# team then built upon this concept, and that's where the `async`/`await` that we are now familiar with were born: 

```c#
using System;

// Allows the "Task" return type
using System.Threading.Tasks;
					
public class Program
{
    // Declare an async function with "async"
	private static async Task<string> ReturnHello()
	{
		return "hello world";
	}
	
    // Main can be async -- no problem
	public static async Task Main()
	{
        // await an async string
		string result = await ReturnHello();
		
        // Print the string we got asynchronously
		Console.WriteLine(result);
	}
}
```

*[Run it on .NETFiddle](https://dotnetfiddle.net/N9rO8Y)*

We ensure that we are `using System.Threading.Tasks` as it includes the `Task` type, and, in general, the `Task` type is needed for an async function to be awaited. The cool thing about C# is that you can make your main function asynchronous just by declaring it with `async`, and you won't have any issues.

If you're interested in learning more about `async`/`await` in C#, [Microsoft's C# docs](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/async/) have a good page on it.

### JavaScript
First introduced in ES6, the `async`/`await` syntax is essentially an abstraction over JavaScript promises (which are similar to Python futures). Unlike Python, however, so long as you're not awaiting, you can call an async function normally without a specific function like Python's `asyncio.start()`:

```javascript
// Declare a function with async
async function returnHello(){
	return "hello world";
}

async function printSomething(){
    // await an async string
	const result = await returnHello();
    
    // print the string we got asynchronously
    console.log(result);
}

// Run our async code
printSomething();
```

*[Run it on JSFiddle](https://jsfiddle.net/kyamcp1o/1/)*

*See MDN for more info on [`async`/`await` in JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await).*

### Rust
Rust now allows the use of the `async`/`await` syntax as well, and it works similarly to Python, C#, and JavaScript:

```rust
// Allows blocking synchronous code to run async code
use futures::executor::block_on;

// Declare an async function with "async"
async fn return_hello() -> String {
    "hello world".to_string()
}

// Code that awaits must also be declared with "async"
async fn print_something(){
    // await an async String
    let result: String = return_hello().await;

    // Print the string we got asynchronously 
    println!("{0}", result); 
}

fn main() {
    // Block the current synchronous execution to run our async code
    block_on(print_something()); 
}
```

*[Run it on Rust Play](https://play.rust-lang.org/?version=stable&mode=debug&edition=2018&code=%2F%2F%20Allows%20blocking%20synchronous%20code%20to%20run%20async%20code%0Ause%20futures%3A%3Aexecutor%3A%3Ablock_on%3B%0A%0A%2F%2F%20Declare%20an%20async%20function%20with%20%22async%22%0Aasync%20fn%20return_hello()%20-%3E%20String%20%7B%0A%20%20%20%20%22hello%20world%22.to_string()%0A%7D%0A%0A%2F%2F%20Code%20that%20awaits%20must%20also%20be%20declared%20with%20%22async%22%0Aasync%20fn%20print_something()%7B%0A%20%20%20%20%2F%2F%20await%20an%20async%20String%0A%20%20%20%20let%20result%3A%20String%20%3D%20return_hello().await%3B%0A%0A%20%20%20%20%2F%2F%20Print%20the%20string%20we%20got%20asynchronously%20%0A%20%20%20%20println!(%22%7B0%7D%22%2C%20result)%3B%20%0A%7D%0A%0Afn%20main()%20%7B%0A%20%20%20%20%2F%2F%20Block%20the%20current%20synchronous%20execution%20to%20run%20our%20async%20code%0A%20%20%20%20block_on(print_something())%3B%20%0A%7D)*

In order to use async functions, we must first add `futures = "0.3"` to our Cargo.toml. We then import the `block_on` function with `use futures::executor::block_on` -- `block_on` is necessary for running our async function from our synchronous `main` function.

*You can find more info on [`async`/`await` in Rust](https://rust-lang.github.io/async-book/01_getting_started/01_chapter.html) in the Rust docs.*

### Go
Rather than the traditional `async`/`await` syntax inherent to all of the previous languages we've covered, Go uses "goroutines" and "channels." You can think of a channel as being similar to a Python future. In Go, you generally send a channel as an argument to a function, then use `go` to run the function concurrently. Whenever you need to ensure the function has finished completing, you use the `<-` syntax, which you can think of as the more common `await` syntax. If your goroutine (the function you're running asynchronously) has a return value, it can be grabbed this way.

```go
package main

import "fmt"

// "chan" makes the return value a string channel instead of a string
func returnHello(result chan string){
	// Gives our channel a value
	result <- "hello world"
}

func main() {
	// Creates a string channel
	result := make(chan string)
	
	// Starts execution of our goroutine
	go returnHello(result)
	
	// Awaits and prints our string
	fmt.Println(<- result)
}
```

*[Run it in the Go Playground](https://play.golang.org/p/4hkgIunl2-E)*

*For more info on concurrency in Go, see [An Introduction to Programming in Go](https://www.golang-book.com/books/intro/10) by Caleb Doxsey.*

### Ruby
Similarly to Python, Ruby also has the Global Interpreter Lock limitation. What it doesn't have is concurrency built-in to the language. However, there is a community-created gem that allows concurrency in Ruby, and you can find its [source on GitHub](https://github.com/ruby-concurrency/concurrent-ruby).

### Java
Like Ruby, Java doesn't have the `async`/`await` syntax built-in, but it does have concurrency capabilities using the `java.util.concurrent` module. However, [Electronic Arts wrote an Async library](https://github.com/electronicarts/ea-async) that allows using `await` as a method. It's not exactly the same as Python/C#/JavaScript/Rust, but it's worth looking into if you're a Java developer and are interested in this sort of functionality.

# C++
Although C++ also doesn't have the `async`/`await` syntax, it does have the ability to use futures to run code concurrently using the `futures` module:

```cpp
#include <iostream>       
#include <string>         

// Necessary for futures
#include <future>     

// No async declaration needed
std::string return_hello() {
    return "hello world";
}

int main ()
{
    // Declares a string future
    std::future<std::string> fut = std::async(return_hello);
    
    // Awaits the result of the future
    std::string result = fut.get();      
    
    // Prints the string we got asynchronously
    std::cout << result << '\n';
}
```

*[Run it on C++ Shell](http://www.cpp.sh/)*

There's no need to declare a function with any keyword to denote whether or not it can and should be run asynchronously. Instead, you declare your initial future whenever you need it with `std::future<{{ function return type }}>` and set it equal to `std::async()`, including the name of the function you want to perform asynchronously along with any arguments it takes, i.e. `std::async(do_something, 1, 2, "string")`. To await the value of the future, use the `.get()` syntax on it.

*You can find documentation for [async in C++](https://www.cplusplus.com/reference/future/async/) on cplusplus.com*

## Summary
Whether you're working with asynchronous network or file operations or you're performing numerous complex calculations, there are a few different ways to maximize your code's efficiency. 

If you're using Python, you can use `asyncio` or `threading` to make the most out of IO operations or the `multiprocessing` module for CPU-intensive code.

*Also remember that the `concurrent.futures` module can be used in place of either `threading` or `multiprocessing`*

If you're using another programming language, chances are there's an implementation of `async`/`await` for it too.
