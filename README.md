# Concurrency, Parallelism, and asyncio

Blog post for [testdriven.io](https://testdriven.io/). If you want to follow along and create the projects yourself, you can find the post [here](https://testdriven.io/blog/concurrency-parallelism-asyncio/).


## Code Examples

Create and activate a new virtual environment:

*Windows Powershell, assuming the Python version in your PATH is 3.9+:*

```powershell
PS X:> python -m venv venv
PS X:> .\venv\Scripts\Activate.ps1
(venv) PS X:>

(venv) PS X:> pip install -r requirements.txt
```

*Mac/Linux:*

```sh
$ python3.9 -m venv venv
$ source venv/bin/activate
(venv)$

(venv)$ pip install -r requirements.txt
```

### Concurrency

```sh
(venv)$ python code_examples/concurrency/sync.py
(venv)$ python code_examples/concurrency/threads.py
(venv)$ python code_examples/concurrency/async.py
```

### Parallelism

```sh
(venv)$ python code_examples/parallelism/sync.py
(venv)$ python code_examples/parallelism/threads.py
(venv)$ python code_examples/parallelism/multi.py
```

### pytest async

```sh
(venv)$ python -m pytest code_examples/pytest_asyncio/test_hello_asyncio.py
(venv)$ python -m pytest code_examples/pytest_asyncio/test_hello_asyncio2.py
```

### asyncio and multiprocessing

```sh
(venv)$ python code_examples/asyncio_and_multiprocessing/sync.py
(venv)$ python code_examples/asyncio_and_multiprocessing/multiprocessing_only.py
(venv)$ python code_examples/asyncio_and_multiprocessing/asyncio_only.py
(venv)$ python code_examples/asyncio_and_multiprocessing/asyncio_with_multiprocessing.py
```
