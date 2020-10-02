import logging
from pathlib import Path


class VmWriter:
    def __init__(self, source_path, class_name):
        self.source_p = source_path
        self.class_name = class_name
        self.file = self._construct_outfile()
        self.logger = self._setup_logger()

    def _construct_outfile(self):
        outfile = Path(self.source_p.parent, f"{self.class_name}").with_suffix(".vm")
        return open(outfile, 'w')

    def close(self):
        return self.file.close()

    def write_function(self, name, n_locals):
        function_declaration = f"function {self.class_name}.{name} {n_locals}\n"
        self.file.write(function_declaration)

    def write_call(self, name, n_args):
        function_call = f"call {name} {n_args}\n"
        self.file.write(function_call)

    def write_push(self, segment, index):
        push_command = f"push {segment} {index}\n"
        self.file.write(push_command)

    def write_pop(self, segment, index):
        pop_command = f"pop {segment} {index}\n"
        self.file.write(pop_command)

    def write_arithmetic(self, command):
        command_map = {
            "+": "add",
            "=": "eq",
            "-": "sub",
            "*": "call Math.multiply 2",
            "/": "call Math.divide 2",
            ">": "gt",
            "<": "lt",
            "unary-": "neg",
            "|": "or",
            "~": "not",
            "&": "and"
        }
        command = f"{command_map.get(command)}\n"
        self.file.write(command)

    def write_label(self, label):
        label_command = f"label {label}\n"
        self.file.write(label_command)

    def write_goto(self, label):
        goto_command = f"goto {label}\n"
        self.file.write(goto_command)

    def write_if(self, label):
        if_goto_command = f"if-goto {label}\n"
        self.file.write(if_goto_command)

    def write_return(self):
        return_command = "return\n"
        self.file.write(return_command)

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger(__name__)
        return logger
