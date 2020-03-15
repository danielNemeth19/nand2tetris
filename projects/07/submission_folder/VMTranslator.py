import os
import sys
import logging
from functools import partial
from pathlib import Path

__logger__ = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Reader:
    def __init__(self, infile):
        self.source = Path(infile)
        self.file_name = self.source.stem
        self.output = self.source.with_suffix(".asm")
        self.read()

    def read(self):
        with open(self.source, "r") as infile:
            source_code = list()
            for line in infile:
                line_part = line.strip().split("//")[0].strip()
                if line_part:
                    parsed_vm_code = self.parse_code_line(line_part)
                    source_code.append(parsed_vm_code)
        CodeWriter(source_code, self.file_name, self.output)

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
    TEMP_OFFSET = 5

    def __init__(self, vm_code, file_name, outfile):
        self.vm_code = vm_code
        self.file_name = file_name
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
        segment, value = self._parse_segment_and_value(arg1, arg2, func="push")
        if not segment:
            self.save_constant_to_d_register(value)
            self.copy_d_to_sp_loc()
            self.increase_stack_pointer()
        if arg1 in ("local", "argument", "this", "that"):
            self.save_constant_to_d_register(value)
            self.save_segment_addr_value_to_d(segment)
            self.copy_d_to_sp_loc()
            self.increase_stack_pointer()
        elif arg1 in ("temp", "static"):
            self.save_temp_static_to_d_register(segment, value)
            self.copy_d_to_sp_loc()
            self.increase_stack_pointer()
        elif arg1 == "pointer":
            pointer_of = segment[value]
            self.save_pointer_to_d(pointer_of=pointer_of)
            self.copy_d_to_sp_loc()
            self.increase_stack_pointer()

    def pop_to_segment(self, arg1, arg2, comment):
        __logger__.debug(f"pop: {arg1}, {arg2}")
        self.assembly_codes.append(comment)
        segment, mem_seg_offset = self._parse_segment_and_value(arg1, arg2, func="pop")
        print(segment, mem_seg_offset)
        if arg1 in ("temp", "static"):
            self._pop_static_temp_segment(segment, mem_seg_offset)
        elif arg1 == "pointer":
            pointer_for = segment[mem_seg_offset]
            self._set_base_address_of_segment(pointer_for=pointer_for)
        elif mem_seg_offset in (0, 1):
            self._pop_to_segment_with_0_1(segment, mem_seg_offset)
        else:
            self._pop_to_segment_with_offset(segment, mem_seg_offset)

    def _parse_segment_and_value(self, arg1, arg2, func):
        try:
            segment = self._get_segment(arg1)
            value = int(arg2)
        except KeyError:
            __logger__.debug(f"Invalid segment for {func} command: {arg1}")
            sys.exit(3)
        except ValueError:
            __logger__.debug(f"Invalid value for {func} command: {arg2}")
            sys.exit(3)
        return segment, value

    def _pop_static_temp_segment(self, segment, value):
        self.decrease_stack_pointer(get_sp_loc_value=True)
        if segment == self.file_name:
            register_var =  f"{segment}.{value}"
        else:
            register_var = f"{segment}{self.TEMP_OFFSET + value}"
        self.assembly_codes.extend([f"@{register_var}", "M = D"])

    def _pop_to_segment_with_0_1(self, segment, offset):
        self.decrease_stack_pointer(get_sp_loc_value=True)
        self.copy_d_to_segment_loc(segment, loc_modifier=offset)

    def _pop_to_segment_with_offset(self, segment, offset):
        self.save_constant_to_d_register(offset)
        self.increase_segment_base_addr_with_d(segment)
        segment_addr_var = "pop_to"
        self.store_addr_to_variable(segment_addr_var)
        self.decrease_stack_pointer(get_sp_loc_value=True)
        self.copy_d_to_segment_loc(segment_addr_var)

    def _set_base_address_of_segment(self, pointer_for):
        self.decrease_stack_pointer(get_sp_loc_value=True)
        self.store_addr_to_variable(pointer_for)

    def _get_segment(self, arg1):
        segments_map = {
            "constant": False,
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "temp": "R",
            "pointer": {
                0: "THIS",
                1: "THAT"
            },
            "static": self.file_name
        }
        return segments_map[arg1]

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
            "neg": "M = -M",
            "and": "M = D & M",
            "or": "M = D | M",
            "not": "M = !M"
        }
        func = func_map[arg1]
        return self.assembly_codes.append(func)

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

    def save_temp_static_to_d_register(self, segment, value):
        if segment == self.file_name:
            register_var = f"{segment}.{value}"
        else:
            register_var = f"{segment}{self.TEMP_OFFSET + value}"
        self.assembly_codes.extend([f"@{register_var}", "D = M"])

    def save_pointer_to_d(self, pointer_of):
        self.assembly_codes.extend([f"@{pointer_of}", "D = M"])

    def save_constant_to_d_register(self, value):
        self.assembly_codes.extend([f"@{value}", "D = A"])

    def save_segment_addr_value_to_d(self, segment):
        self.assembly_codes.extend([f"@{segment}", "A = D + M", "D = M"])

    def increase_segment_base_addr_with_d(self, segment):
        self.assembly_codes.extend([f"@{segment}", "D = D + M"])

    def store_addr_to_variable(self, segment_address):
        self.assembly_codes.extend([f"@{segment_address}", "M = D"])

    def copy_d_to_sp_loc(self):
        self.assembly_codes.append("@SP")
        self.assembly_codes.append("A = M")
        self.assembly_codes.append("M = D")
        return

    def copy_d_to_segment_loc(self, segment, loc_modifier=False):
        self.assembly_codes.append(f"@{segment}")
        addr = "A = M" if not loc_modifier else "A = M + 1"
        self.assembly_codes.append(addr)
        self.assembly_codes.append("M = D")
        return

    def _setup_map(self):
        cmd_map = {
            "push": self.push_to_stack,
            "arithmetic": self.arithmetic,
            "pop": self.pop_to_segment,
        }
        return cmd_map

    def write_out(self):
        with open(self.output_path, "w") as outfile:
            for assembly_code in self.assembly_codes:
                outfile.write(assembly_code)
                outfile.write("\n")


if __name__ == '__main__':
    input_path = sys.argv[1]
    Reader(input_path)
