import pathlib
from sys import argv


def bug_finder(file: str) -> None:
    path = pathlib.Path(file)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    tasks_list = []
    prev_i = 0
    for i in range(len(content) - 1):
        if content[i] + content[i + 1] == "\n\n":
            tasks_list += ["".join(content[prev_i:i])]
            prev_i = i + 2
    tasks_list += ["".join(content[prev_i:])]

    for record in tasks_list:
        entrance = []
        output = []
        record_list = record.split("\n")
        for element in record_list:
            number = element.find("->")
            if number != -1:
                entrance += [element[: number - 1]]
                output += [element[number + 3 :]]
        entrance_repetitions = [
            (i, entrance.index(entrance[i]), entrance[i])
            for i in range(len(entrance))
            if not i == entrance.index(entrance[i])
        ]
        output_repetitions = [
            (i, output.index(output[i]), output[i])
            for i in range(len(output))
            if not i == output.index(output[i])
        ]

        missing_on_entrance = []  # type:ignore
        missing_on_output = []  # type:ignore

        for element in entrance:
            if element not in output:
                missing_on_output += element

        for element in output:
            if element not in entrance:
                missing_on_entrance += element

        if len(missing_on_output) > 0 and len(output_repetitions) > 0:
            if len(missing_on_output) == 1 and len(output_repetitions) == 1:
                if len(output_repetitions[0]) != 3:
                    print("V, V, V...")
            else:
                print("V, V, V...")

        if len(missing_on_entrance) > 0 and len(entrance_repetitions) > 0:
            if len(missing_on_entrance) == 1 and len(entrance_repetitions) == 1:
                if len(entrance_repetitions[0]) != 3:
                    print("V, V, V...")
            else:
                print("V, V, V...")


if __name__ == "__main__":
    file = argv[1]
    bug_finder(file)
