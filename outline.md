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
            * Running multiple functions with different parameters
        * Allows doing multiple things at once, either at the same time, or by doing one directly after another
    * Overview
        * ~ "We'll start with how these concepts fit into Python and introduce the threading, multiprocessing, and asyncio libraries"
        * ~ "Then we'll compare these concepts in Python against their implementations in other languages"
2. Concurrency
    * What it is - switching between tasks while others are waiting
    * threading
    * asyncio
3. Parallelism - performing multiple tasks at the same time
    * What it is
    * How it differs from concurrency
        * Global Interpreter Lock (GIL)
    * multiprocessing
4. Comparison to other languages
    1. How different languages differ with concurrency and parallelism
    2. How different languages tackle async
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
*  Asynchronous Python - https://medium.com/@nhumrich/asynchronous-python-45df84b82434
*  Threading vs Multiprocessing in Python - https://www.youtube.com/watch?v=ecKWiaHCEKs