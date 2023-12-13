from string import ascii_letters, digits

VALID_CHARS = ascii_letters + digits + "_"
VALID_CHARS += "абвгдеёжзиийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


class Define:
    """
    A define in c++ program.
    """

    def __init__(self, raw: str):
        raw = raw[8:]

        self.name = ""
        self.arguments = []
        self.body = ""
        self.empty = False

        if all(x in VALID_CHARS for x in raw):
            self.empty = True
            return

        for i in range(len(raw)):
            if raw[i] not in VALID_CHARS:
                self.name = raw[:i]
                name_end = i
                break
        else:
            raise ValueError("Invalid define: " + raw)

        if raw[name_end] == " ":
            self.body = raw[i + 1:]
            return

        args_start = name_end + 1
        args_end = raw.find(")", args_start)
        self.body = raw[args_end + 2:]

        self.arguments = [x.strip() for x in raw[args_start:args_end].split(",")]

    def tune(self, program: str):
        if len(self.arguments) == 0:
            return self.standard_tune(program)
        return self.arg_tune(program)

    def standard_tune(self, program: str):
        min_pos = 0
        while True:
            pos = program.find(self.name, min_pos)
            if pos == -1:
                break
            if program[pos - 1] in VALID_CHARS:
                min_pos = pos + 1
                continue
            if program[pos + len(self.name)] in VALID_CHARS:
                min_pos = pos + 1
                continue
            program = program[:pos] + self.body + program[pos + len(self.name):]
            min_pos = pos + len(self.body)
        return program

    def arg_tune(self, program: str):
        min_pos = 0
        while True:
            pos = program.find(self.name, min_pos)
            if pos == -1:
                break
            if program[pos - 1] in VALID_CHARS:
                min_pos = pos + 1
                continue
            if program[pos + len(self.name)] in VALID_CHARS:
                min_pos = pos + 1
                continue

            args_start = program.find("(", pos)
            brackets = 1
            args = []
            buffer = ""
            for i in range(args_start + 1, len(program)):
                if program[i] == "(":
                    brackets += 1
                elif program[i] == ")":
                    brackets -= 1
                if brackets == 0:
                    if buffer:
                        args.append(buffer)
                    define_end = i
                    break
                buffer += program[i]
                if program[i] == "," and brackets == 1:
                    args.append(buffer)
                    buffer = ""

            else:
                raise ValueError(f"INVALID TUNE AT {pos}\n IN" + program)

            if len(args) != len(self.arguments):
                raise ValueError(f"Argument count mismatch: {len(self.arguments)} needed but {len(args)} found")

            prepared_body = self.body

            for fr, to in zip(self.arguments, args):
                prepared_body = prepared_body.replace(fr, to)

            program = program[:pos] + prepared_body + program[define_end + 1:]
            min_pos = pos + len(self.body)

        return program


def convert(program: str):
    """
    Inlines all defines in given c++ program.

    Args:
        program (str): The c++ program to be converted.

    Returns:
        str: The converted c++ program.
    """
    defines = []
    look_from = 0
    while True:
        pos = program.find("#define", look_from)
        if pos == -1:
            break
        end_pos = program.find("\n", pos)

        define = Define(program[pos:end_pos])
        if not define.empty:
            defines.append(define)
            program = program[:pos] + program[end_pos + 1:]
        else:
            look_from = end_pos

    for define in defines:
        program = define.tune(program)
    return program
