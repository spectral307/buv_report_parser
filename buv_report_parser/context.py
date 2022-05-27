from dataclasses import dataclass


class Context:
    @dataclass
    class Position:
        line: int = 0
        char: int = 0

    def __init__(self, lines):
        self.lines = lines
        self.pos = Context.Position()

    @ classmethod
    def create_from_file(cls, file):
        text = file.read().splitlines()
        return Context(text)

    @ classmethod
    def create_from_path(cls, path):
        with open(path, "r") as file:
            return cls.create_from_file(file)
