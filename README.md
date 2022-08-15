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
def methode1():
    for i in tqdm(range(100)):
        with open("stream.txt", "wb", buffering=0) as f:
            for x in range(100000):
                f.write(str(x).encode())

# up to 48-52 seconds 
def methode2():
    for i in tqdm(range(100)):
        with open("stream.txt", "w") as f:
            for x in range(100000):
                f.write(str(x))
                f.flush()

# up to 1 hours 
def methode3():
    for i in tqdm(range(100)):
        for x in range(100000):
            open("stream.txt", "w").write(str(x))

# up to 1 hours & 3 minutes
def methode4():
    for i in tqdm(range(100)):
        for x in range(100000):
            f = open("stream.txt", "w")
            f.write(str(x))
            f.close()
```