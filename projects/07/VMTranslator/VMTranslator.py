import os
import sys
import logging
from functools import partial
from pathlib import Path

ROOT_PATH = Path(os.environ.get("USERPROFILE"), "Workspace", "nand2tetris", "projects", "07", "VMTranslator")
__logger__ = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Reader:
    def __init__(self, infile, outfile):
        self.source = Path(ROOT_PATH, infile)
        self.output = outfile
        self.read()

    def read(self):
        with open(self.source, "r") as infile:
            source_code = list()
            for line in infile:
                line_part = line.strip().split("//")[0].strip()
                if line_part:
                    parsed_vm_code = self.parse_code_line(line_part)
                    source_code.append(parsed_vm_code)
        CodeWriter(source_code, self.output)

    @staticmethod
    def parse_code_line(line_part):
        vm_code_spec = dict(command=None, arg1=None, arg2=None)
        code_segments = line_part.split()
        for key, code_segment in zip(vm_code_spec.keys(), code_segments):
            vm_code_spec[key] = code_segment
        vm_code_spec["comment"] = f"// {line_part}"
        __logger__.debug(f"VM code dict: {vm_code_spec}")
        return vm_code_spec


class CodeWriter:
    C_ARITHMETIC = ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")

    def __init__(self, vm_code, outfile):
        self.vm_code = vm_code
        self.output_path = outfile
        self.cmd_function_map = self._setup_map()
        self.labels = dict()
        self.assembly_codes = list()
        self.translate()

    def translate(self):
        for code_line in self.vm_code:
            func, arg1, arg2, comment = self.parse_params(code_line)
            partial(func, arg1, arg2, comment)()

        self.write_out()
        for line in self.assembly_codes:
            print(line)

    def parse_params(self, code_line):
        command = code_line.get("command")
        comment = code_line.get("comment")
        if command in self.C_ARITHMETIC:
            func = self.cmd_function_map["arithmetic"]
            arg1 = command
            return func, arg1, None, comment
        else:
            func = self.cmd_function_map[command]
            arg1 = code_line.get("arg1")
            arg2 = code_line.get("arg2")
        return func, arg1, arg2, comment

    def push_to_stack(self, arg1, arg2, comment):
        __logger__.debug(f"push: {arg1}, {arg2}")
        self.assembly_codes.append(comment)
        if arg1 == "constant":
            self.save_constant_to_d_register(arg2)
            self.copy_d_to_sp_loc()
            self.increase_stack_pointer()

    def arithmetic(self, arg1, _, comment):
        __logger__.debug(f"add: {arg1}, {_}")
        self.assembly_codes.append(comment)
        self.decrease_stack_pointer(get_sp_loc_value=True)
        if arg1 in ("neg", "not"):
            self.write_arithmetic_function(arg1)
        if arg1 in ("add", "sub", "and", "or"):
            self.decrease_stack_pointer()
            self.write_arithmetic_function(arg1)
        if arg1 in ("eq", "lt", "gt"):
            self.decrease_stack_pointer()
            self.write_arithmetic_function(arg1)
            self.write_conditional_jump(arg1)
            self.write_not_true_branch(arg1)
            self.write_true_branch(arg1)
            self.generate_label_for_done(arg1)
        self.increase_stack_pointer()
        return

    def increase_stack_pointer(self):
        self.assembly_codes.append("@SP")
        self.assembly_codes.append("M = M + 1")
        return

    def decrease_stack_pointer(self, get_sp_loc_value=False):
        self.assembly_codes.append("@SP")
        self.assembly_codes.append("AM = M - 1")
        if get_sp_loc_value:
            self.assembly_codes.append("D = M")
        return

    def write_not_true_branch(self, cond):
        if cond in ("eq", "lt", "gt"):
            self.assembly_codes.extend(["@SP", "A = M", "M = 0"])
            self.write_conditional_jump(cond, done=True)
        return

    def write_true_branch(self, cond):
        if cond in ("eq", "lt", "gt"):
            count = self.labels[cond]
            label = f"({cond}_{count})"
            self.assembly_codes.append(label)
            self.assembly_codes.extend(["@SP", "A = M", "M = -1"])
        return

    def generate_label_for_done(self, cond):
        count = self.labels.get(cond)
        close_label = f"(done.{cond}_{count})"
        self.assembly_codes.append(close_label)

    def write_arithmetic_function(self, arg1):
        func_map = {
            "add": "M = M + D",
            "sub": "M = M - D",
            "eq": "D = M - D",
            "lt": "D = M - D",
            "gt": "D =  M - D",
            "neg": ["M = M - D", "M = M - D"],
            "and": "M = D & M",
            "or": "M = D | M",
            "not": ["M = M - D", "M = M - D", "M = M - 1"]
        }
        func = func_map[arg1]
        if isinstance(func, str):
            return self.assembly_codes.append(func)
        return self.assembly_codes.extend(func)

    def write_conditional_jump(self, cond, done=False):
        jmp_map = {
            "eq": "JEQ",
            "lt": "JLT",
            "gt": "JGT",
            "unc": "JMP"
        }
        if done:
            count = self.labels.get(cond)
            symbol = f"@done.{cond}_{count}"
            self.assembly_codes.extend([symbol, f"0; {jmp_map['unc']}"])
        else:
            count = self.labels.get(cond, 0) + 1
            self.labels[cond] = count
            symbol = f"@{cond}_{count}"
            self.assembly_codes.append(symbol)
            self.assembly_codes.append(f"D;{jmp_map[cond]}")
        return

    def save_constant_to_d_register(self, value):
        self.assembly_codes.extend([f"@{value}", "D = A"])

    def copy_d_to_sp_loc(self):
        self.assembly_codes.append("@SP")
        self.assembly_codes.append("A = M")
        self.assembly_codes.append("M = D")
        return

    def _setup_map(self):
        cmd_map = {
            "push": self.push_to_stack,
            "arithmetic": self.arithmetic
        }
        return cmd_map

    def write_out(self):
        with open(self.output_path, "w") as outfile:
            for assembly_code in self.assembly_codes:
                outfile.write(assembly_code)
                outfile.write("\n")


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    Reader(input_path, output_path)