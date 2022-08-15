import os
import requests

from collections.abc import Iterator
from tqdm import tqdm
from git import Repo

PATH_OF_GIT_REPO = r"./race-pi-maxio-1/.git"
FILE_MAX_SIZE = 100000000


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
    current_file: "str" = sorted(filter(lambda x: ".txt" in x, os.listdir(path)), key=lambda x: int(x.split(".")[1]))[-1]
    to_push: int = int(input(f"> "))
    file_changed: bool = True
    check: int = 0
    commited: int = 0
    with tqdm(total=to_push) as pbar:
        while commited < to_push:
            if file_changed:
                check = check_file(path, current_file)
                file_changed = False
                if check == FILE_MAX_SIZE:
                    repo.remote(name="origin").push()
                    print(f"{current_file} is full")
                    current_file = f"pi.{int(current_file.split('.')[1]) + 1}.txt"
                    print(f"{current_file} is now the current file")
                    file_changed = True
                    continue
            check = FILE_MAX_SIZE - check
            while check != 0 and commited < to_push:
                char: str = str(next(getter_pi))
                open(f"./{path}/{current_file}", "a").write(char)
                check -= 1
                commited += 1
                pbar.update(1)
                repo.git.add(update=True)
                repo.index.commit(f"decimal: {start + commited} ({char})")
            file_changed = True
        repo.remote(name="origin").push()


def main() -> None:
    current_start = count_nb_files("./race-pi-maxio-1")
    print(f"start at {current_start} decimal.")
    process("./race-pi-maxio-1", current_start)


if __name__ == "__main__":
    main()
