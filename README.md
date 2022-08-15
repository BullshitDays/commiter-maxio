# commiter-maxio

For Profiler:
```bash
python -m profile -o profile_commit.prof main.py
python -m snakeviz profile_commit.prof 
```


after comparing the best method is `with ... open` without buffering.
Method test:
```python
# up to 32-39 seconds
# most time used by write
def methode1():
    for i in tqdm(range(100)):
        with open("stream.txt", "wb", buffering=0) as f:
            for x in range(100000):
                f.write(str(x).encode())

# up to 48-52 seconds
# most time used by flush
def methode2():
    for i in tqdm(range(100)):
        with open("stream.txt", "w") as f:
            for x in range(100000):
                f.write(str(x))
                f.flush()

# up to 1 hours & 20 minutes
# most time used by open
def methode3():
    for i in tqdm(range(100)):
        for x in range(100000):
            open("stream.txt", "w").write(str(x))

# up to 1 hours & 3 minutes
# most time used by open
def methode4():
    for i in tqdm(range(100)):
        for x in range(100000):
            f = open("stream.txt", "w")
            f.write(str(x))
            f.close()
```
