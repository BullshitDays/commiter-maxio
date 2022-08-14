import os


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
    # filename: pi.1.txt, pi.2.txt
    current_file: "str" = sorted(filter(lambda x: ".txt" in x, os.listdir(path)), key=lambda x: int(x.split(".")[1]))[-1]
    to_push: int = int(input(f"> "))
    file_changed: bool = True
    check: int = 0
    commited: int = 0
    with open(f"./pi_dec_1m.txt", "a") as pi_all:
        pi_all.seek(start)
        while commited < to_push:
            if file_changed:
                check = check_file(path, current_file)
                file_changed = False
                if check == 100000000:
                    os.system(f"cd {path} && git push")
                    print(f"{current_file} is full")
                    current_file = f"pi.{int(current_file.split('.')[1]) + 1}.txt"
                    print(f"{current_file} is now the current file")
                    file_changed = True
                    continue
            check = 100000000 - check
            with open(f"./{path}/{current_file}", "r") as f:
                while check != 0:
                    f.write(pi_all.read(1))
                    check -= 1
                    commited += 1
                    os.system(f"cd {path} && git add {current_file} && git commit -m 'decimal: {start + commited}'")
                if commited == to_push:
                    break
                file_changed = True
    os.system(f"cd {path} && git push")


def main() -> None:
    current_start = count_nb_files("./race-pi-maxio-1")
    print(f"start at {current_start} decimal.")
    process("./race-pi-maxio-1", current_start)


if __name__ == "__main__":
    main()
