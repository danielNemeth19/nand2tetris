import sys
import logging
from functools import partial
from pathlib import Path

__logger__ = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Reader:
    def __init__(self, infile):
        self.source = Path(infile)

    def read(self):
        with open(self.source, "r") as infile:
            source_code = list()
            for line in infile:
                line_part = line.strip().split("//")[0].strip()
                if line_part:
                    parsed_vm_code = self.parse_code_line(line_part)
                    source_code.append(parsed_vm_code)
        return source_code

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
    ENDFRAME_OFFSET = 5
    CALL_POINTERS = 5
    ENDFRAME_REGISTER = "R13"
    RETURN_ADDR_REGISTER = "R14"

    def __init__(self, vm_code, file_name, bootstrap_needed):
        self.vm_code = vm_code
        self.file_name = file_name
        self._is_bootstrap_needed = bootstrap_needed
        self.cmd_function_map = self._setup_map()
        self.labels = dict()
        self.current_function = None
        self.function_call_counter = dict()
        self.assembly_codes = list()

    def translate(self):
        if self._is_bootstrap_needed:
            self.write_bootstrap_code()
        self.assembly_codes.append(f"// Translating file: {self.file_name}")
        for code_line in self.vm_code:
            func, arg1, arg2, comment = self.parse_params(code_line)
            partial(func, arg1, arg2, comment)()

        for line in self.assembly_codes:
            print(line)
        return self.assembly_codes

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
            self.push_constant_to_stack(value)
        elif arg1 in ("temp", "static"):
            self.push_static_temp_segment(segment, value)
        elif arg1 == "pointer":
            pointer_of = segment[value]
            self.push_pointer_to_stack(pointer_of)
        elif value in (0, 1):
            self.push_segment_with_0_1(segment, value)
        else:
            self.push_segment_with_offset(segment, offset=value)
        self.increase_stack_pointer()

    def pop_to_segment(self, arg1, arg2, comment):
        __logger__.debug(f"pop: {arg1}, {arg2}")
        self.assembly_codes.append(comment)
        segment, mem_seg_offset = self._parse_segment_and_value(arg1, arg2, func="pop")
        if arg1 in ("temp", "static"):
            self.pop_static_temp_segment(segment, mem_seg_offset)
        elif arg1 == "pointer":
            pointer_for = segment[mem_seg_offset]
            self.set_base_address_of_segment(pointer_for=pointer_for)
        elif mem_seg_offset in (0, 1):
            self.pop_to_segment_with_0_1(segment, mem_seg_offset)
        else:
            self.pop_to_segment_with_offset(segment, mem_seg_offset)

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

    def push_constant_to_stack(self, value):
        if value in (0, 1):
            self.copy_value_to_sp_loc(value=value)
        else:
            self.save_constant_to_d_register(value)
            self.copy_value_to_sp_loc()

    def push_segment_with_0_1(self, segment, value):
        offset = "M + 1" if value else "M"
        self.save_segment_addr_value_to_d(segment, offset)
        self.copy_value_to_sp_loc()

    def push_segment_with_offset(self, segment, offset):
        register_d = self.save_constant_to_d_register(value=offset)
        offset = f"{register_d} + M"
        self.save_segment_addr_value_to_d(segment, offset)
        self.copy_value_to_sp_loc()

    def push_static_temp_segment(self, segment, value):
        self.save_temp_static_to_d_register(segment, value)
        self.copy_value_to_sp_loc()

    def push_pointer_to_stack(self, pointer_of):
        self.save_pointer_to_d(pointer_of=pointer_of)
        self.copy_value_to_sp_loc()

    def save_temp_static_to_d_register(self, segment, value):
        if segment == self.file_name:
            register_var = f"{segment}.{value}"
        else:
            register_var = f"{segment}{self.TEMP_OFFSET + value}"
        self.assembly_codes.extend([f"@{register_var}", "D = M"])

    def pop_static_temp_segment(self, segment, value):
        self.decrease_stack_pointer(get_sp_loc_value=True)
        if segment == self.file_name:
            register_var = f"{segment}.{value}"
        else:
            register_var = f"{segment}{self.TEMP_OFFSET + value}"
        self.assembly_codes.extend([f"@{register_var}", "M = D"])

    def pop_to_segment_with_0_1(self, segment, offset):
        self.decrease_stack_pointer(get_sp_loc_value=True)
        self.copy_d_to_segment_loc(segment, loc_modifier=offset)

    def pop_to_segment_with_offset(self, segment, offset):
        self.save_constant_to_d_register(offset)
        self.increase_segment_base_addr_with_d(segment)
        segment_addr_var = "pop_to"
        self.store_addr_to_variable(segment_addr_var)
        self.decrease_stack_pointer(get_sp_loc_value=True)
        self.copy_d_to_segment_loc(segment_addr_var)

    def set_base_address_of_segment(self, pointer_for):
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
        if arg1 in ("neg", "not"):
            self.write_neg_not(arg1)
        elif arg1 in ("add", "sub", "and", "or"):
            self.write_add_sub_and_or(arg1)
        else:
            self.write_eq_lt_gt(arg1)
        return

    def increase_stack_pointer(self, increase_from_d=False):
        self.assembly_codes.append("@SP")
        base_register = "D" if increase_from_d else "M"
        self.assembly_codes.append(f"M = {base_register} + 1")
        return

    def decrease_stack_pointer(self, get_sp_loc_value=False):
        self.assembly_codes.append("@SP")
        self.assembly_codes.append("AM = M - 1")
        if get_sp_loc_value:
            self.assembly_codes.append("D = M")
        return

    def activate_register_behind_stack_pointer(self):
        self.assembly_codes.append("@SP")
        self.assembly_codes.append("A = M - 1")

    def write_neg_not(self, arg1):
        self.activate_register_behind_stack_pointer()
        self.write_arithmetic_function(arg1)

    def write_add_sub_and_or(self, arg1):
        self.decrease_stack_pointer(get_sp_loc_value=True)
        self.activate_register_behind_stack_pointer()
        self.write_arithmetic_function(arg1)

    def write_eq_lt_gt(self, arg1):
        cond_var, done_var = self._get_vars(func=arg1)
        self.decrease_stack_pointer(get_sp_loc_value=True)
        self.activate_register_behind_stack_pointer()
        self.write_arithmetic_function(arg1)
        self.write_jump(
            func=arg1, symbol=self._as_symbol(cond_var)
        )
        self.write_not_true_branch()
        self.write_jump(
            func="unc", symbol=self._as_symbol(done_var)
        )
        self.write_true_branch_with_labels(
            label=self._as_label(cond_var),
            done_label=self._as_label(done_var)
        )

    def _get_vars(self, func):
        count = self.labels.get(func, 0) + 1
        self.labels[func] = count
        cond_var = f"{func}_{self.file_name}_{count}"
        done_var = f"done.{cond_var}"
        return cond_var, done_var

    @staticmethod
    def _as_label(var):
        return f"({var})"

    @staticmethod
    def _as_symbol(var):
        return f"@{var}"

    def write_not_true_branch(self):
        self.activate_register_behind_stack_pointer()
        self.assembly_codes.append("M = 0")
        return

    def write_true_branch_with_labels(self, label, done_label):
        self.assembly_codes.append(label)
        self.activate_register_behind_stack_pointer()
        self.assembly_codes.append("M = -1")
        self.assembly_codes.append(done_label)
        return

    def write_jump(self, func, symbol):
        jmp_map = {
            "eq": "JEQ",
            "lt": "JLT",
            "gt": "JGT",
            "unc": "JMP"
        }
        self.assembly_codes.append(symbol)
        self.assembly_codes.append(f"D;{jmp_map[func]}")
        return

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

    def save_pointer_to_d(self, pointer_of):
        self.assembly_codes.extend([f"@{pointer_of}", "D = M"])

    def save_constant_to_d_register(self, value):
        self.assembly_codes.extend([f"@{value}", "D = A"])
        return "D"

    def save_segment_addr_value_to_d(self, segment, offset_from_pointer):
        self.assembly_codes.append(f"@{segment}")
        self.assembly_codes.append(f"A = {offset_from_pointer}")
        self.assembly_codes.append("D = M")

    def increase_segment_base_addr_with_d(self, segment):
        self.assembly_codes.extend([f"@{segment}", "D = D + M"])

    def store_addr_to_variable(self, segment_address):
        self.assembly_codes.extend([f"@{segment_address}", "M = D"])

    def copy_value_to_sp_loc(self, value="D"):
        self.assembly_codes.append("@SP")
        self.assembly_codes.append("A = M")
        self.assembly_codes.append(f"M = {value}")
        return

    def copy_d_to_segment_loc(self, segment, loc_modifier=False):
        self.assembly_codes.append(f"@{segment}")
        addr = "A = M" if not loc_modifier else "A = M + 1"
        self.assembly_codes.append(addr)
        self.assembly_codes.append("M = D")
        return

    def write_label(self, arg1, arg2, comment):
        __logger__.debug(f"write label: {arg1}, {arg2}")
        self.assembly_codes.append(comment)
        label_prefix = self.current_function if self.current_function else "null"
        self.assembly_codes.append(f"({label_prefix}${arg1})")
        return

    def write_if_goto(self, arg1, arg2, comment):
        __logger__.debug(f"write if-goto: {arg1}, {arg2}")
        self.assembly_codes.append(comment)
        self.decrease_stack_pointer(get_sp_loc_value=True)
        label_prefix = self.current_function if self.current_function else "null"
        self.assembly_codes.extend([f"@{label_prefix}${arg1}", "D; JNE"])
        return

    def write_goto(self, arg1, arg2, comment):
        __logger__.debug(f"write goto: {arg1}, {arg2}")
        self.assembly_codes.append(comment)
        label_prefix = self.current_function if self.current_function else "null"
        self.assembly_codes.append(f"@{label_prefix}${arg1}")
        self.assembly_codes.append("0; JMP")
        return

    def goto_return_address_in_callers_code(self):
        self.assembly_codes.append("// -->goto to return address")
        self.assembly_codes.append(f"@{self.RETURN_ADDR_REGISTER}")
        self.assembly_codes.append("A = M")
        self.assembly_codes.append("0; JMP")

    def write_function(self, arg1, arg2, comment):
        __logger__.debug(f"write function: {arg1}, {arg2}")
        __logger__.debug(f"Current running function name saved: {arg1}")
        self.current_function = arg1
        self.assembly_codes.append(comment)
        self.assembly_codes.append(f"({arg1})")
        try:
            num_of_locals = int(arg2)
        except ValueError:
            __logger__.debug(f"Function def incorrect: {arg2} should be an int")
            sys.exit(3)
        for i in range(num_of_locals):
            __logger__.debug(f"setting up locals, local var numb: {i}")
            self.push_to_stack(arg1="constant", arg2=0, comment=f"// func setup: push constant 0 for local var {i}")
            self.pop_to_segment(arg1="local", arg2=i, comment=f"// func setup: pop local {i}")
            self.push_to_stack(arg1="local", arg2=i, comment=f"// func setup: push local {i} to stack")
        pass

    def save_endframe(self):
        self.assembly_codes.append("// -->Saving endframe")
        self.save_pointer_to_d("LCL")
        self.store_addr_to_variable(self.ENDFRAME_REGISTER)

    def save_retr_addr(self):
        self.assembly_codes.append("// -->Saving return address")
        self.assembly_codes.extend([f"@{self.ENDFRAME_OFFSET}", "A = D - A", "D = M"])
        self.store_addr_to_variable(self.RETURN_ADDR_REGISTER)

    def reposition_sp(self):
        self.assembly_codes.append("// -->Reposition SP of the caller")
        self.save_pointer_to_d("ARG")
        self.increase_stack_pointer(increase_from_d=True)

    def restore_segment_pointer(self, segment, offset):
        self.assembly_codes.append(f"// -->Restore {segment} of the caller")
        if offset != 1:
            offset = self.save_constant_to_d_register(offset)
        self.assembly_codes.extend([f"@{self.ENDFRAME_REGISTER}", f"A = M - {offset}", "D = M"])
        self.store_addr_to_variable(segment_address=segment)

    def write_return(self, _, __, comment):
        __logger__.debug(f"Returning from function call")
        self.assembly_codes.append(comment)
        self.save_endframe()
        self.save_retr_addr()
        self.pop_to_segment(arg1="argument", arg2=0, comment="// -->Reposition return value for the caller")
        self.reposition_sp()
        for segment, i in zip(("THAT", "THIS", "ARG", "LCL"), range(1, 5)):
            self.restore_segment_pointer(segment, i)
        self.goto_return_address_in_callers_code()

    def push_return_address(self, func_name, call_count):
        self.assembly_codes.append("// -->Saving return address and pushing to stack")
        retr_var = f"{func_name}.{self.file_name}$ret.{call_count}"
        self.assembly_codes.append(f"@{retr_var}")
        self.assembly_codes.append("D = A")
        self.copy_value_to_sp_loc()
        self.increase_stack_pointer()
        return retr_var

    def push_segment_pointers(self):
        for segment in ("LCL", "ARG", "THIS", "THAT"):
            self.assembly_codes.append(f"// -->Push {segment} of the caller")
            self.assembly_codes.append(f"@{segment}")
            self.assembly_codes.append("D = M")
            self.copy_value_to_sp_loc()
            self.increase_stack_pointer()

    def reposition_arg(self, number_of_args):
        self.assembly_codes.append(f"// -->Reposition of arg")
        try:
            num_of_args = int(number_of_args)
        except ValueError:
            __logger__.debug(f"Function def incorrect: {number_of_args} should be an int")
            sys.exit(3)
        self.save_constant_to_d_register(num_of_args + self.CALL_POINTERS)
        self.assembly_codes.extend([f"@SP", "D = M - D"])
        self.store_addr_to_variable(segment_address="ARG")

    def reposition_lcl(self):
        self.assembly_codes.append(f"// -->Reposition LCL")
        self.save_pointer_to_d(pointer_of="SP")
        self.store_addr_to_variable(segment_address="LCL")

    def goto_function(self, func_name):
        self.assembly_codes.append(f"// -->goto function now")
        self.assembly_codes.append(f"@{func_name}")
        self.assembly_codes.append("0; JMP")

    def write_return_label(self, r_label):
        self.assembly_codes.append(f"// -->return label")
        self.assembly_codes.append(f"({r_label})")

    def write_call(self, arg1, arg2, comment):
        __logger__.debug(f"write call: {arg1}, {arg2}")
        self.assembly_codes.append(comment)
        call_count = self.function_call_counter.get(arg1, 0) + 1
        self.function_call_counter[arg1] = call_count
        retr_var = self.push_return_address(func_name=arg1, call_count=call_count)
        self.push_segment_pointers()
        self.reposition_arg(number_of_args=arg2)
        self.reposition_lcl()
        self.goto_function(func_name=arg1)
        self.write_return_label(r_label=retr_var)

    def write_bootstrap_code(self):
        self.assembly_codes.append("// Bootstrap code")
        self.save_constant_to_d_register(256)
        self.store_addr_to_variable("SP")
        self.write_call(arg1="Sys.init", arg2=0, comment="// Boostrap: calling Sys.init")

    def _setup_map(self):
        cmd_map = {
            "push": self.push_to_stack,
            "arithmetic": self.arithmetic,
            "pop": self.pop_to_segment,
            "label": self.write_label,
            "if-goto": self.write_if_goto,
            "goto": self.write_goto,
            "function": self.write_function,
            "return": self.write_return,
            "call": self.write_call
        }
        return cmd_map


def write_out(outfile_path, assembly_code):
    with open(outfile_path, "w") as outfile:
        for line in assembly_code:
            outfile.write(line)
            outfile.write("\n")
    return True


def _file_translation(source_path):
    bootstrap_needed = False
    outfile = source_path.with_suffix(".asm")
    source_code = Reader(infile=source_path).read()
    file_name = source_path.stem
    translated_code = CodeWriter(source_code, file_name, bootstrap_needed).translate()
    return outfile, translated_code


def _dir_translation(source_path):
    translated_code = list()
    outfile = Path(source_path, source_path.stem).with_suffix(".asm")
    bootstrap_needed = True
    for file in source_path.iterdir():
        if file.suffix == ".vm":
            file_name = file.stem
            source_code = Reader(infile=file).read()
            assembly_code = CodeWriter(source_code, file_name, bootstrap_needed).translate()
            bootstrap_needed = False
            translated_code.extend(assembly_code)
    return outfile, translated_code


def main(source):
    source_path = Path(source)
    translate_method = _file_translation if source_path.is_file() else _dir_translation
    outfile, translated_code = partial(translate_method, source_path)()
    write_out(outfile_path=outfile, assembly_code=translated_code)
    return


if __name__ == '__main__':
    input_path = sys.argv[1]
    main(source=input_path)
