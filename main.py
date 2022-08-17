import os
import requests

from collections.abc import Iterator
from tqdm import tqdm
from git import Repo

PATH = "race-pi-maxio-1"
PATH_OF_GIT_REPO = f"./{PATH}/.git"
FILE_MAX_SIZE = 100000000
PUSH_OVER = 10000


def get_digit(start: int) -> Iterator[int]:
    pi: list = []
    start_next: int = start + 1000
    while True:
        if len(pi) == 0:
            req = requests.get("https://api.pi.delivery/v1/pi", params=[("start", start + 1), ("numberOfDigits", 1000)])
            pi = list(req.json()["content"])
            start, start_next = start_next, start_next + 1000
        yield pi.pop(0)


def check_file(path: str, filename: str) -> int:
    with open(f"./{path}/{filename}", "r") as f:
        return len(f.read())


def count_nb_files(path: str) -> int:
    lenght: int = 0
    for file in os.listdir(path):
        if ".txt" in file:
            lenght += check_file(path, file)
    return lenght


def process(path: str, start: int) -> None:
    getter_pi: Iterator[int] = get_digit(start)
    repo = Repo(PATH_OF_GIT_REPO)
    current_file: str = sorted(filter(lambda x: ".txt" in x, os.listdir(path)), key=lambda x: int(x.split(".")[1]))[-1]
    to_push: int = int(input(f"nb of push (commit: choice * {PUSH_OVER})> ")) * PUSH_OVER
    file_changed: bool = True
    check: int = 0
    commited: int = 0
    with tqdm(total=to_push // PUSH_OVER) as pbarPush:
        with tqdm(total=min(PUSH_OVER, to_push - commited), leave=False) as pbarCommit:
            while commited < to_push:
                if file_changed:
                    check = check_file(path, current_file)
                    file_changed = False
                    if check == FILE_MAX_SIZE:
                        print(f"{current_file} is full")
                        current_file = f"pi.{int(current_file.split('.')[1]) + 1}.txt"
                        print(f"{current_file} is now the current file")
                        file_changed = True
                        continue
                check = FILE_MAX_SIZE - check
                with open(f"./{path}/{current_file}", "ba", buffering=0) as f:
                    while check != 0 and commited < to_push:
                        char: str = str(next(getter_pi))
                        f.write(char.encode())
                        check -= 1
                        commited += 1
                        pbarCommit.update(1)
                        repo.git.add(["pi.1.txt"])
                        repo.index.commit(f"decimal: {start + commited} ({char})")
                        if commited % PUSH_OVER == 0:
                            repo.remote(name="origin").push()
                            pbarPush.update(1)
                            pbarCommit.reset()
                    file_changed = True
            repo.remote(name="origin").push()


def main() -> None:
    current_start = count_nb_files(f"./{PATH}")
    print(f"start at {current_start} decimal.")
    process(f"./{PATH}", current_start)


if __name__ == "__main__":
    main()
