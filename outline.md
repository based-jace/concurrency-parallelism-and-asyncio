# Title: Concurrency, Parallelism, and asyncio

### Points
* Why asynchronicity matters
* How concurreny and parallelism differ
* asyncio vs threading vs multiprocessing
    * Python examples of each
* Concurrency, parallelism, and asynchronicity in Python vs other languages
* Global Interpreter Lock

## Outline
1. Intro - Concurrency and Parallelism
    * Why they matter - examples cases that benefit from concurrency and parallelism
        * Examples Cases
            * Communicating with multiple services over the web
            * Running code that writes/reads to/from files multiple times
            * Running a calculation-heavy function multiple times
        * Allows doing multiple things at once, either at the same time, or by doing one directly after another
    * Overview
        * ~ "We'll start with how these concepts fit into Python and introduce the threading, multiprocessing, and asyncio libraries"
        * ~ "Then we'll compare these concepts in Python against their implementations in other languages"
2. Concurrency
    * What it is - switching between tasks while others are waiting
    * threading
    * asyncio
    * When to use threading vs asyncio
3. Parallelism
    * What it is - performing multiple tasks at the same time
    * How it differs from non-parallel concurrency
        * Global Interpreter Lock (GIL)
    * multiprocessing
    * When to use multiprocessing vs threading or asyncio
4. Comparison to other languages
    1. How different languages differ with concurrency and parallelism
    2. How different languages tackle async/await
    * Languages to compare Python with
        * .NET - F# to C#
        * JavaScript
        * Ruby
        * C/C++
        * Java
        * Go
        * Rust
5. Outro
    * Recap

### Resources
<!-- * Asynchronous Python - https://medium.com/@nhumrich/asynchronous-python-45df84b82434 -->
* Threading vs Multiprocessing in Python - https://www.youtube.com/watch?v=ecKWiaHCEKs
* Multiprocessing in Python - https://www.youtube.com/watch?v=fKl2JW_qrso&t=127s
<!-- * Threading in Python - https://www.youtube.com/watch?v=IEEhzQoKtQU -->
* More on Concurrency and Parallelism in Python - https://realpython.com/python-concurrency/
* Python's Global Interpreter Lock (GIL) - https://realpython.com/python-gil/
<!-- * asyncio - https://realpython.com/async-io-python/ -->
