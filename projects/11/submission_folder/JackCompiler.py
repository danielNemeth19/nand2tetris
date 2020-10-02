import sys
import logging
import argparse
from functools import partial
from pathlib import Path

from Tokenizer import Tokenizer
from SymbolTable import SymbolTable
from VmWriter import VmWriter


class Parser:
    STATEMENT_KEYWORDS = ("let", "if", "while", "do", "return")
    OP = ("+", "-", "*", "/", "&", "|", "<", ">", "=")
    UNARY_OP = ("-", "~")
    KEYWORD_CONSTANTS = ("true", "false", "null", "this")

    def __init__(self, source_path, tokenizer, options):
        self.source_p = source_path
        self.class_name = self.source_p.stem
        self.ident_spec, self.verbose, self.write_xml = self._configure_parser(options)
        if self.write_xml:
            self.file = self._construct_xml_outfile()
        self.vm_writer = VmWriter(self.source_p, self.class_name)
        self.tokenizer = tokenizer
        self.class_symbol_table = SymbolTable(is_class=True)
        self.subroutine_symbol_table = SymbolTable()
        self.logger = self._setup_logger()

    @staticmethod
    def _configure_parser(spec):
        write_xml = False if not spec.xml else True
        return spec.ident, spec.verbose, write_xml

    def _construct_xml_outfile(self):
        outfile = Path(self.source_p.parent, f"{self.class_name}").with_suffix(".xml")
        return open(outfile, 'w')

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        log_level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=log_level)
        return logger

    def compile_class(self):
        class_grammar = self._class_grammar()
        self.logger.debug(f"Writing: {self.vm_writer.file.name}")
        for elem in class_grammar["fixpattern"]:
            elem_grammar = class_grammar[elem]
            self.tokenizer.next_token()
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if "non-terminal" in elem_grammar["write"] and self.write_xml:
                    self.file.write(elem_grammar["write"]["non-terminal"])
                elem_grammar["write"]["terminal"]()

        self.tokenizer.next_token()
        while self._if_optional_grammar_applies(class_grammar, optional_grammar_key="optional_1"):
            grammar = self._get_optional_grammar(class_grammar, optional_key="optional_1")
            validator_kwargs = grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                grammar["write"]["terminal"]()

        while self._if_optional_grammar_applies(class_grammar, optional_grammar_key="optional_2"):
            grammar = self._get_optional_grammar(class_grammar, optional_key="optional_2")
            validator_kwargs = grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if self.write_xml:
                    self.file.write(grammar["write"]["non-terminal"])
                grammar["write"]["terminal"]()

        close_grammar = self._get_close_pattern_grammar(class_grammar)
        self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
        validator_kwargs = close_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            close_grammar["write"]["terminal"]()

        self._write_non_terminal_tag("class", open_tag=False)
        if self.write_xml:
            self.file.close()
        return self.vm_writer.close()

    def compile_class_var_dec(self):
        class_var_dec_grammar = self._class_var_dec_grammar()
        self._write_non_terminal_tag("classVarDec")
        token_cache = list()
        for elem in class_var_dec_grammar["fixPattern"]:
            self.logger.debug(f"Matching grammar for:{elem} {self.tokenizer.current_token}")
            elem_grammar = class_var_dec_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                token_cache.append(self.tokenizer.current_token)
                if elem == "varName":
                    self.class_symbol_table.define(cached_data=token_cache)
                elem_grammar["write"]["terminal"]()

        while self._if_optional_group_applies(class_var_dec_grammar):
            for elem in class_var_dec_grammar["optionalGroup"]:
                self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = class_var_dec_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    if elem == "varName":
                        token_cache.append(self.tokenizer.current_token)
                        self.class_symbol_table.define(cached_data=token_cache)
                    elem_grammar["write"]["terminal"]()

        close_grammar = self._get_close_pattern_grammar(class_var_dec_grammar)
        self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
        validator_kwargs = close_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            close_grammar["write"]["terminal"]()
        self._write_non_terminal_tag("classVarDec", open_tag=False)

        if self.block_is_not_done(class_var_dec_grammar):
            return self.compile_class_var_dec()
        return

    def compile_subroutine_dec(self):
        self.logger.debug(f"Compiling subroutine: {self.tokenizer.current_token}")
        self._cleanup_cache()
        self._initialize_counters()
        function_cache = dict(subroutine_kind=None, type=None, name=None)
        subroutine_dec_grammar = self._subroutine_dec_grammar()
        self.subroutine_symbol_table.start_subroutine()
        self._handle_this_for_methods()
        for elem in subroutine_dec_grammar["fixPattern"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = subroutine_dec_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if "non-terminal" in elem_grammar["write"] and self.write_xml:
                    self.file.write(elem_grammar["write"]["non-terminal"])
                if elem == "constructor|function|method":
                    function_cache["subroutine_kind"] = self.tokenizer.current_token
                elif elem == "void|type":
                    function_cache["type"] = self.tokenizer.current_token
                elif elem == "subroutineName":
                    function_cache["name"] = self.tokenizer.current_token
                elem_grammar["write"]["terminal"](function_cache=function_cache)
        self._write_non_terminal_tag("subroutineDec", open_tag=False)

    def _handle_this_for_methods(self):
        if self.tokenizer.current_token == "method":
            cached_data = ["argument", self.class_name, "this"]
            self.subroutine_symbol_table.define(cached_data=cached_data)

    def compile_parameter_list(self, function_cache=None):
        parameter_list_grammar = self._parameter_list_grammar()
        if self._if_optional_group_applies(parameter_list_grammar):
            token_cache = ["argument"]
            for elem in parameter_list_grammar["optionalGroup"]:
                self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = parameter_list_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    token_cache.append(self.tokenizer.current_token)
                    if elem == "varName":
                        self.subroutine_symbol_table.define(cached_data=token_cache)
                    elem_grammar["write"]["terminal"]()

        while self._if_optional_group_applies(parameter_list_grammar, optional_group_key="optionalGroup_2"):
            token_cache = ["argument"]
            for elem in parameter_list_grammar["optionalGroup_2"]:
                self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = parameter_list_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    if self.tokenizer.get_token_type() != "symbol":
                        token_cache.append(self.tokenizer.current_token)
                        if elem == "varName":
                            self.subroutine_symbol_table.define(cached_data=token_cache)
                    elem_grammar["write"]["terminal"]()

    def compile_subroutine_body(self, function_cache=None):
        subroutine_body_grammar = self._subroutine_body_grammar()
        for elem in subroutine_body_grammar["fixPattern"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = subroutine_body_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()

        if self._if_optional_grammar_applies(subroutine_body_grammar):
            optional_grammar = subroutine_body_grammar["optional"]
            elem_grammar = subroutine_body_grammar[optional_grammar]
            self.logger.debug(f"token is: {self.tokenizer.current_token}, matched grammar: {optional_grammar}")
            elem_grammar["write"]["terminal"]()

        for elem in subroutine_body_grammar["fixPattern_2"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = subroutine_body_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"](function_cache=function_cache)
        self._write_non_terminal_tag(elem="subroutineBody", open_tag=False)

    def compile_var_dec(self):
        var_dec_grammar = self._var_dec_grammar()
        self._write_non_terminal_tag("varDec")
        token_cache = list()
        for elem in var_dec_grammar["fixPattern"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = var_dec_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                token_cache.append(self.tokenizer.current_token)
                if elem == "varName":
                    self.subroutine_symbol_table.define(cached_data=token_cache)
                elem_grammar["write"]["terminal"]()

        while self._if_optional_group_applies(var_dec_grammar):
            for elem in var_dec_grammar["optionalGroup"]:
                self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = var_dec_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    if elem == "varName":
                        token_cache.append(self.tokenizer.current_token)
                        self.subroutine_symbol_table.define(cached_data=token_cache)
                    elem_grammar["write"]["terminal"]()

        close_grammar = self._get_close_pattern_grammar(var_dec_grammar)
        self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")

        validator_kwargs = close_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            close_grammar["write"]["terminal"]()
        self._write_non_terminal_tag("varDec", open_tag=False)

        if self.block_is_not_done(var_dec_grammar):
            return self.compile_var_dec()
        return

    def compile_statements(self, function_cache=None):
        if not hasattr(self, "function_cache"):
            self.handle_subroutine_setup(function_cache)
        self._write_non_terminal_tag(elem="statements")
        while self.tokenizer.current_token in self.STATEMENT_KEYWORDS:
            func = getattr(self, f"compile_{self.tokenizer.current_token}_statement")
            func()
        self._write_non_terminal_tag(elem="statements", open_tag=False)

    def handle_subroutine_setup(self, function_cache):
        setattr(self, "function_cache", function_cache)
        number_of_vars = self.subroutine_symbol_table.var_count("var")
        func_name = self.function_cache.get("name")
        self.vm_writer.write_function(name=func_name, n_locals=number_of_vars)
        number_of_fields = self.class_symbol_table.var_count("field")
        # TODO: Let' clarify if we need 'THIS' when there are no fields?
        if self._is_constructor() and number_of_fields:
            self._create_memory_block_for_new_object(number_of_fields)
        elif self._is_method():
            self._anchor_this_segment_to_objects_base_address()
        return

    def _create_memory_block_for_new_object(self, number_of_fields):
        self.vm_writer.write_push("constant", number_of_fields)
        self.vm_writer.write_call("Memory.alloc", 1)
        self.vm_writer.write_pop("pointer", 0)

    def _anchor_this_segment_to_objects_base_address(self):
        self.vm_writer.write_push("argument", 0)
        self.vm_writer.write_pop("pointer", 0)

    def compile_let_statement(self):
        let_grammar = self._let_statement_grammar()
        self._write_non_terminal_tag(elem="letStatement")
        varname = None
        is_lh_array = False
        for elem in let_grammar["fixPattern"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = let_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if elem == "varName":
                    varname = self.tokenizer.current_token
                elem_grammar["write"]["terminal"]()

        if self._if_optional_group_applies(let_grammar):
            is_lh_array = True
            for elem in let_grammar["optionalGroup"]:
                self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = let_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    elem_grammar["write"]["terminal"]()
            self.calc_mem_address_of_array_elem(varname=varname)

        for elem in let_grammar["fixPattern_2"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = let_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()
        if is_lh_array:
            self.assign_result_to_lh()
        else:
            self.write_pop_command_for_let_statement(varname=varname)
        self._write_non_terminal_tag(elem="letStatement", open_tag=False)

    def calc_mem_address_of_array_elem(self, varname, push_that=False):
        kind, index_of = self.get_kind_and_index_of_identifier(varname)
        segment = self._get_segment_for_vm_writer(kind)
        self.logger.debug(f"Push base address of array named: {varname}, segment: {segment}, index: {index_of}")
        self.vm_writer.write_push(segment, index_of)
        self.vm_writer.write_arithmetic("+")
        if push_that:
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("that", 0)

    def assign_result_to_lh(self):
        self.logger.debug("saving result of rh expression")
        self.vm_writer.write_pop("temp", 0)
        self.logger.debug("setting THAT segment to base address of lh[expression]")
        self.vm_writer.write_pop("pointer", 1)
        self.logger.debug("pushing result of rh expression to stack")
        self.vm_writer.write_push("temp", 0)
        self.logger.debug("save result to the mem address of THAT")
        self.vm_writer.write_pop("that", 0)

    def write_pop_command_for_let_statement(self, varname):
        kind, index_of = self.get_kind_and_index_of_identifier(varname)
        segment = self._get_segment_for_vm_writer(kind)
        self.logger.debug(f"Let statement pop, varName: {varname}, segment: {segment}, index: {index_of}")
        self.vm_writer.write_pop(segment, index_of)

    def compile_if_statement(self):
        if_grammar = self._if_statement_grammar()
        self._write_non_terminal_tag(elem="ifStatement")
        label_ix = self._get_if_label_counter()
        true_label, false_label, end_label = "IF_TRUE", "IF_FALSE", "IF_END"
        for elem in if_grammar["fixPattern"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = if_grammar[elem]
            validator_obj = elem_grammar["validator"]
            if isinstance(validator_obj, dict):
                if self._match_grammar(**validator_obj):
                    elem_grammar["write"]["terminal"]()
            else:
                if validator_obj():
                    elem_grammar["write"]["terminal"]()
                    self.vm_writer.write_if(f"{true_label}{label_ix}")
                    self.vm_writer.write_goto(f"{false_label}{label_ix}")
                    self.vm_writer.write_label(f"{true_label}{label_ix}")

        if self._if_optional_group_applies(block_grammar=if_grammar):
            self.vm_writer.write_goto(f"{end_label}{label_ix}")
            self.vm_writer.write_label(f"{false_label}{label_ix}")
            for elem in if_grammar["optionalGroup"]:
                self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = if_grammar[elem]
                validator_obj = elem_grammar["validator"]
                if isinstance(validator_obj, dict):
                    if self._match_grammar(**validator_obj):
                        elem_grammar["write"]["terminal"]()
                else:
                    if validator_obj():
                        elem_grammar["write"]["terminal"]()
            self.vm_writer.write_label(f"{end_label}{label_ix}")
        else:
            self.vm_writer.write_label(f"{false_label}{label_ix}")
        self._write_non_terminal_tag(elem="ifStatement", open_tag=False)

    def _get_if_label_counter(self):
        label_ix = getattr(self, "if_counter") + 1
        setattr(self, "if_counter", label_ix)
        return label_ix

    def compile_while_statement(self):
        while_grammar = self._while_statement_grammar()
        self._write_non_terminal_tag(elem="whileStatement")
        label_ix = self._get_while_label_counter()
        true_label, end_label = "WHILE_EXP", "WHILE_END"
        for elem in while_grammar["fixPattern"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = while_grammar[elem]
            validator_obj = elem_grammar["validator"]
            if isinstance(validator_obj, dict):
                if self._match_grammar(**validator_obj):
                    if elem == "while":
                        self.vm_writer.write_label(f"{true_label}{label_ix}")
                    elem_grammar["write"]["terminal"]()
            else:
                if validator_obj():
                    elem_grammar["write"]["terminal"]()
                    self.vm_writer.write_arithmetic("~")
                    self.vm_writer.write_if(f"{end_label}{label_ix}")

        self.vm_writer.write_goto(f"{true_label}{label_ix}")
        self.vm_writer.write_label(f"{end_label}{label_ix}")
        self._write_non_terminal_tag(elem="whileStatement", open_tag=False)

    def _get_while_label_counter(self):
        label_ix = getattr(self, "while_counter") + 1
        setattr(self, "while_counter", label_ix)
        return label_ix

    def compile_do_statement(self):
        do_grammar = self._do_statement_grammar()
        self._write_non_terminal_tag(elem="doStatement")
        for elem in do_grammar["fixPattern"]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = do_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()
        self.vm_writer.write_pop("temp", 0)
        self._write_non_terminal_tag(elem="doStatement", open_tag=False)

    def compile_return_statement(self):
        return_grammar = self._return_grammar()
        self._write_non_terminal_tag(elem="returnStatement")
        fix_grammar = self._get_fixpattern_grammar(return_grammar)
        validator_kwargs = fix_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            fix_grammar["write"]["terminal"]()

        optional_grammar = self._get_optional_grammar(return_grammar)
        if optional_grammar["validator"]():
            # TODO - constructor case: would be good to validate that constructor needs to return 'this'
            optional_grammar["write"]["terminal"]()

        close_grammar = self._get_close_pattern_grammar(return_grammar)
        self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
        validator_kwargs = close_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            close_grammar["write"]["terminal"]()

        subroutine_type = self.function_cache.get("type")
        if subroutine_type == "void":
            self.vm_writer.write_push("constant", 0)
        self.vm_writer.write_return()
        self._write_non_terminal_tag(elem="returnStatement", open_tag=False)

    def _is_constructor(self):
        subroutine_kind = self.function_cache.get("subroutine_kind", None)
        if subroutine_kind == "constructor":
            return True
        return False

    def _is_method(self):
        subroutine_kind = self.function_cache.get("subroutine_kind", None)
        if subroutine_kind == "method":
            return True
        return False

    def compile_expression(self):
        expression_grammar = self._expression_grammar()
        self._write_non_terminal_tag(elem="expression")
        term_grammar = self._get_fixpattern_grammar(expression_grammar)
        self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")

        def _compile_term(un_op=None):
            current_term = None
            type_of = None
            un_op = un_op if un_op else None
            if self._is_simple_term():
                current_term, type_of = self._handle_simple_term(term_grammar)
            elif self._if_optional_group_applies(expression_grammar, optional_group_key="optionalSubGroup_1"):
                self._write_non_terminal_tag("term")
                for elem in expression_grammar["optionalSubGroup_1"]:
                    elem_grammar = expression_grammar[elem]
                    validator_kwargs = elem_grammar["validator"]
                    if self._match_grammar(**validator_kwargs):
                        elem_grammar["write"]["terminal"]()
                self._write_non_terminal_tag("term", open_tag=False)

            elif self._if_optional_group_applies(expression_grammar, optional_group_key="optionalSubGroup_2"):
                self._write_non_terminal_tag("term")
                for elem in expression_grammar["optionalSubGroup_2"]:
                    elem_grammar = expression_grammar[elem]
                    validator_kwargs = elem_grammar["validator"]
                    if self._match_grammar(**validator_kwargs):
                        is_recursive = elem_grammar.get("recursive", False)
                        if not is_recursive:
                            un_op = self.tokenizer.current_token
                            elem_grammar["write"]["terminal"]()
                        else:
                            current_term, type_of, un_op = _compile_term(un_op=un_op)
                self._write_non_terminal_tag("term", open_tag=False)

            elif self._is_identifier():
                self._write_non_terminal_tag("term")
                cached_token_dict = self._lookahead_for_next_token()
                if self._if_optional_group_applies(
                        expression_grammar, optional_group_key="optionalSubGroup_3", index=1
                ):
                    self._write_terminal_element(advance_token=False, cache=cached_token_dict)
                    for elem in expression_grammar["optionalSubGroup_3"][1:]:
                        elem_grammar = expression_grammar[elem]
                        validator_kwargs = elem_grammar["validator"]
                        if self._match_grammar(**validator_kwargs):
                            elem_grammar["write"]["terminal"]()
                    current_term = cached_token_dict.get("cached_token")
                    self.calc_mem_address_of_array_elem(varname=current_term, push_that=True)

                elif self._if_optional_group_applies(
                        expression_grammar, optional_group_key="optionalSubGroup_4", index=1
                ):
                    self._write_subroutine_call(cached_token_dict)
                else:
                    current_term = cached_token_dict.get("cached_token")
                    type_of = cached_token_dict.get("cached_token_type")
                    self._write_terminal_element(advance_token=False, cache=cached_token_dict)
                self._write_non_terminal_tag("term", open_tag=False)
            return current_term, type_of, un_op

        term, term_type, unary_op = _compile_term()
        self.logger.debug(f"Term is: {term}, term_type is: {term_type} unary op is: {unary_op}")
        if term:
            self.write_push_command_for_term(term, term_type)

        op_to_call = None
        while self._if_optional_group_applies(expression_grammar):
            for optional_elem in expression_grammar["optionalGroup"]:
                optional_grammar = expression_grammar[optional_elem]
                optional_validator_kwargs = optional_grammar["validator"]
                if self._match_grammar(**optional_validator_kwargs):
                    recursive = optional_grammar.get("recursive", False)
                    if not recursive:
                        op_to_call = self.tokenizer.current_token
                        optional_grammar["write"]["terminal"]()
                    else:
                        term, term_type, unary_op = _compile_term()
                        if term:
                            self.write_push_command_for_term(term, term_type)
        if op_to_call:
            self.vm_writer.write_arithmetic(op_to_call)
        elif unary_op:
            unary_op = "unary-" if unary_op == "-" else unary_op
            self.vm_writer.write_arithmetic(unary_op)

        self._write_non_terminal_tag(elem="expression", open_tag=False)

    def write_push_command_for_term(self, token, token_type):
        if token_type == self.tokenizer.INT_CONST:
            self.vm_writer.write_push("constant", token)
        elif token_type == self.tokenizer.IDENTIFIER:
            kind, index_of = self.get_kind_and_index_of_identifier(token_value=token)
            segment = self._get_segment_for_vm_writer(kind)
            self.vm_writer.write_push(segment, index_of)
        elif token_type == self.tokenizer.STR_CONST:
            self.generate_code_for_string(token)
        elif token_type == self.tokenizer.KEYWORD:
            if token in ("null", "false"):
                self.vm_writer.write_push("constant", 0)
            elif token == "true":
                self.vm_writer.write_push("constant", 0)
                self.vm_writer.write_arithmetic("~")
            else:
                self.logger.debug(f"Term must be 'this': {token}")
                self.vm_writer.write_push("pointer", 0)
        else:
            self.logger.debug(f"Term is not handled yet: {token}")

    def generate_code_for_string(self, token):
        self.logger.debug(f"String constant to handle: {token}")
        self.vm_writer.write_push("constant", len(token))
        self.vm_writer.write_call("String.new", 1)
        for char in token:
            if char.isascii():
                self.vm_writer.write_push("constant", ord(char))
                self.vm_writer.write_call("String.appendChar", 2)
            else:
                self.logger.error(f"Char is not in ASCII range: {char}")
                sys.exit(3)

    def compile_expression_list(self):
        expr_counter = 0
        expression_list_grammar = self._expression_list_grammar()
        self._write_non_terminal_tag(elem="expressionList")
        optional_grammar = self._get_optional_grammar(expression_list_grammar)
        if optional_grammar["validator"]():
            expr_counter += 1
            optional_grammar["write"]["terminal"]()
            while self._if_optional_group_applies(expression_list_grammar, optional_group_key="optionalGroup_2"):
                for elem in expression_list_grammar["optionalGroup_2"]:
                    self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
                    elem_grammar = expression_list_grammar[elem]
                    validator_obj = elem_grammar["validator"]
                    if isinstance(validator_obj, dict):
                        if self._match_grammar(**validator_obj):
                            elem_grammar["write"]["terminal"]()
                    else:
                        if validator_obj():
                            expr_counter += 1
                            elem_grammar["write"]["terminal"]()
        self.logger.debug(f"Number of expressions in list: {expr_counter}")
        self._write_non_terminal_tag(elem="expressionList", open_tag=False)
        return expr_counter

    def _handle_simple_term(self, grammar):
        term_type, term = self._get_token_and_token_type(cache=None)
        if self.write_xml:
            self.file.write(grammar["write"]['non-terminal'])
        grammar["write"]["terminal"]()
        if self.write_xml:
            self.file.write(grammar["write"]['non-terminal-close'])
        return term, term_type

    def _write_subroutine_call(self, cached_token_dict=None):
        subroutine_grammar = self._subroutine_call_grammar()
        if cached_token_dict:
            applicable = True if self.tokenizer.current_token == "." else False
        else:
            applicable, cached_token_dict = self.look_ahead_for_optional_grammar(subroutine_grammar)
        cached_token = cached_token_dict.get("cached_token")
        self._write_terminal_element(advance_token=False, cache=cached_token_dict)
        if applicable:
            elem = subroutine_grammar["optionalGroup"][1]
            elem_grammar = subroutine_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()

        needs_this, name = self._get_call_elements(applicable, cached_token)
        if needs_this:
            self.push_object_for_method_call(cached_token)

        fix_pattern_index = 0 if applicable else 1
        for elem in subroutine_grammar["fixPattern"][fix_pattern_index:]:
            self.logger.debug(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = subroutine_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if elem == "expressionList":
                    n_expressions = elem_grammar["write"]["terminal"]()
                    n_args = n_expressions + 1 if needs_this else n_expressions
                else:
                    elem_grammar["write"]["terminal"]()
        self.vm_writer.write_call(name, n_args)

    def _get_call_elements(self, applicable, cached_token):
        needs_this = True
        if not applicable:
            klass_obj = self.class_name
            subroutine = cached_token
            name = f"{klass_obj}.{subroutine}"
        else:
            registered_var_type = self.get_type_of_identifier(token_value=cached_token)
            subroutine = self.tokenizer.current_token
            if registered_var_type:
                klass_instance = registered_var_type
                name = f"{klass_instance}.{subroutine}"
            else:
                needs_this = False
                klass_obj = cached_token
                name = f"{klass_obj}.{subroutine}"
        return needs_this, name

    def push_object_for_method_call(self, cached_token):
        kind, index_of = self.get_kind_and_index_of_identifier(cached_token)
        if kind:
            segment = self._get_segment_for_vm_writer(kind)
        else:
            self.logger.debug(f"Must be a call on class's own method: {cached_token}")
            self._check_validity_of_method_call()
            segment, index_of = "pointer", 0
        self.vm_writer.write_push(segment, index_of)

    def _check_validity_of_method_call(self):
        if self.function_cache.get("subroutine_kind") == "function":
            self.logger.error("Subroutine call in the form of 'do fun()' is only "
                              "valid from a constructor or a method")
            sys.exit(3)

    def _write_terminal_element(self, advance_token=True, cache=None, defined=False, **kwargs):
        token_type, token_value = self._get_token_and_token_type(cache)
        if self.write_xml:
            self.file.write(f"<{token_type}>{token_value}</{token_type}>\n")
        if token_type == self.tokenizer.IDENTIFIER and self.ident_spec:
            kind, index_of = self.get_kind_and_index_of_identifier(token_value)
            self._write_identifier_spec(token_value, defined, kind, index_of)
        if advance_token:
            self.tokenizer.next_token()

    def _get_token_and_token_type(self, cache):
        cache = cache or {}
        if cache:
            token_type, token_value = cache.get("cached_token_type"), cache.get("cached_token")
            return token_type, token_value
        token_type = self.tokenizer.get_token_type()
        token_value = getattr(self.tokenizer, token_type)()
        return token_type, token_value

    def get_kind_and_index_of_identifier(self, token_value):
        kind = self.subroutine_symbol_table.kind_of(token_value)
        if not kind:
            kind = self.class_symbol_table.kind_of(token_value)
        symbol_table = self._get_symbol_table(kind)
        if symbol_table:
            index_of = symbol_table.index_of(token_value)
        if not symbol_table:
            return None, None
        return kind, index_of

    def get_type_of_identifier(self, token_value):
        type_of = self.subroutine_symbol_table.type_of(token_value)
        if not type_of:
            type_of = self.class_symbol_table.type_of(token_value)
        if not type_of:
            return None
        else:
            return type_of

    def _write_identifier_spec(self, token_value, defined, kind, index_of):
        self.file.write("\t<identifier_spec>\n")
        if not kind:
            self.logger.debug(f"{token_value} is either a subroutine name or a class name")
        else:
            status = "defined" if defined else "used"
            spec = f"\t\t<kind>{kind}</kind>\n\t\t<index>{index_of}</index>\n\t\t<status>{status}</status>\n"
            self.file.write(spec)
            self.logger.debug(f"{token_value}--{kind}--{index_of}--{status}")
        self.file.write("\t</identifier_spec>\n")

    def _get_symbol_table(self, kind):
        if not kind:
            return None
        elif kind in ("argument", "var"):
            return self.subroutine_symbol_table
        return self.class_symbol_table

    def _write_non_terminal_tag(self, elem, open_tag=True):
        if self.write_xml:
            tag_to_write = f"<{elem}>\n" if open_tag else f"</{elem}>\n"
            self.file.write(tag_to_write)

    @staticmethod
    def _get_fixpattern_grammar(grammar):
        key = grammar["fixPattern"]
        return grammar[key]

    @staticmethod
    def _get_optional_grammar(grammar, optional_key="optional"):
        key = grammar[optional_key]
        return grammar[key]

    @staticmethod
    def _get_close_pattern_grammar(grammar):
        key = grammar["closePattern"]
        return grammar[key]

    @staticmethod
    def _get_segment_for_vm_writer(kind):
        segment_map = dict(
            field="this",
            static="static",
            var="local",
            argument="argument"
        )
        return segment_map.get(kind)

    def _cleanup_cache(self):
        for attr in ("function_cache", "if_counter", "while_counter"):
            if hasattr(self, attr):
                delattr(self, attr)

    def _initialize_counters(self):
        for attr in ("if_counter", "while_counter"):
            setattr(self, attr, -1)

    def _match_grammar(self, expected_token=None, expected_token_type=None, optional=None, force_pass=False):
        if force_pass:
            return True
        token = self.tokenizer.current_token
        token_type = self.tokenizer.get_token_type()
        if isinstance(expected_token, tuple):
            if token in expected_token:
                return True
            elif (self.tokenizer.IDENTIFIER in expected_token and
                    token_type == self.tokenizer.IDENTIFIER):
                return True
            elif optional:
                return False
        elif expected_token and token == expected_token:
            return True
        elif expected_token_type and not expected_token:
            if expected_token_type == token_type:
                return True
        elif optional:
            return False
        self.logger.error(f"Expected: type: '{expected_token_type}', token: '{expected_token}'."
                          f"Got: type: '{token_type}', token: '{token}'")
        self.file.close()
        sys.exit(3)

    def _match_expression_grammar(self):
        token = self.tokenizer.current_token
        token_type = self.tokenizer.get_token_type()
        if token in self.KEYWORD_CONSTANTS:
            return True
        elif token_type in (
                self.tokenizer.INT_CONST, self.tokenizer.STR_CONST, self.tokenizer.IDENTIFIER
        ):
            return True
        elif token in (*self.UNARY_OP, "("):
            return True
        return False

    def _is_simple_term(self):
        token = self.tokenizer.current_token
        token_type = self.tokenizer.get_token_type()
        if token in self.KEYWORD_CONSTANTS:
            return True
        elif token_type in (self.tokenizer.INT_CONST, self.tokenizer.STR_CONST):
            return True
        return False

    def _is_identifier(self):
        token_type = self.tokenizer.get_token_type()
        if token_type == self.tokenizer.IDENTIFIER:
            return True
        return False

    def _if_optional_group_applies(self, block_grammar, optional_group_key=None, index=0):
        optional_group_key = optional_group_key if optional_group_key else "optionalGroup"
        elem_index_to_match = index if index else 0
        elem = block_grammar[optional_group_key][elem_index_to_match]
        grammar = block_grammar[elem]
        validator_kwargs = grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            return True
        return False

    def _if_optional_grammar_applies(self, block_grammar, optional_grammar_key=None):
        optional_grammar_key = optional_grammar_key if optional_grammar_key else "optional"
        elem_key = block_grammar[optional_grammar_key]
        grammar = block_grammar[elem_key]
        validator_kwargs = grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            return True
        return False

    def _lookahead_for_next_token(self):
        cached_token_dict = dict(
            cached_token=self.tokenizer.current_token,
            cached_token_type=self.tokenizer.get_token_type(),
        )
        self.tokenizer.next_token()
        return cached_token_dict

    def look_ahead_for_optional_grammar(self, block_grammar):
        first_elem, second_elem = block_grammar["optionalGroup"][0], block_grammar["optionalGroup"][1]
        grammar = block_grammar[first_elem]
        if self._check_if_grammar_is_valid(grammar=grammar):
            cached_token_dict = self._lookahead_for_next_token()
        grammar = block_grammar[second_elem]
        if self._check_if_grammar_is_valid(grammar=grammar):
            return True, cached_token_dict
        return False, cached_token_dict

    def _check_if_grammar_is_valid(self, grammar):
        validator_kwargs = grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            return True
        return False

    def block_is_not_done(self, block_grammar):
        first_elem = block_grammar["fixPattern"][0]
        grammar = block_grammar[first_elem]
        validator_kwargs = grammar["validator"]
        if self._match_grammar(**validator_kwargs, optional=True):
            return True
        return False

    def _class_grammar(self):
        grammar_map = {
            "fixpattern": ("class", "ClassName", "{",),
            "optional_1": "classVarDec",
            "optional_2": "subRoutineDec",
            "closePattern": "}",
            "class": {
                "validator": {
                    "expected_token": "class"
                },
                "write": {
                    "non-terminal": "<class>\n",
                    "terminal": partial(self._write_terminal_element, False)
                }
            },
            "ClassName": {
                "validator": {
                    "expected_token": self.class_name,
                },
                "write": {
                    "terminal": partial(self._write_terminal_element, False)
                }
            },
            "{": {
                "validator": {
                    "expected_token": "{",
                },
                "write": {
                    "terminal": partial(self._write_terminal_element, False)
                }
            },
            "classVarDec": {
                "validator": {
                    "expected_token": ("static", "field"),
                    "optional": True
                },
                "write": {
                    "terminal": self.compile_class_var_dec
                }
            },
            "subRoutineDec": {
                "validator": {
                    "expected_token": ("constructor", "function", "method"),
                    "optional": True
                },
                "write": {
                    "non-terminal": "<subroutineDec>\n",
                    "terminal": self.compile_subroutine_dec
                }
            },
            "}": {
                "validator": {
                    "expected_token": "}",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            }
        }
        return grammar_map

    def _class_var_dec_grammar(self):
        grammar_map = {
            "fixPattern": ("static|field", "type", "varName"),
            "optionalGroup": (",", "varName"),
            "closePattern": ";",
            "static|field": {
                "validator": {
                    "expected_token": ("static", "field")
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "type": {
                "validator": {
                    "expected_token": ('int', 'char', 'boolean', self.tokenizer.IDENTIFIER),
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "varName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER
                },
                "write": {
                    "terminal": partial(self._write_terminal_element, True, None, True)
                }
            },
            ",": {
                "validator": {
                    "expected_token": ",",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            ";": {
                "validator": {
                    "expected_token": ";",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            }
        }
        return grammar_map

    def _subroutine_dec_grammar(self):
        grammar_map = {
            "fixPattern": (
                "constructor|function|method", "void|type", "subroutineName",
                "(", "parameterList",  ")", "subroutineBody"
            ),
            "constructor|function|method": {
                "validator": {
                    "expected_token": ("constructor", "function", "method")
                },
                "write": {
                    "terminal": self._write_terminal_element
                },
            },
            "void|type": {
                "validator": {
                    "expected_token": ('int', 'char', 'boolean', 'void', self.tokenizer.IDENTIFIER),
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "subroutineName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "(": {
                "validator": {
                    "expected_token": "(",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "parameterList": {
                "validator": {
                    "force_pass": True
                },
                "write": {
                    "non-terminal": "<parameterList>\n",
                    "terminal": self.compile_parameter_list
                }
            },
            ")": {
                "validator": {
                    "expected_token": ")",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                    "non-terminal": "</parameterList>\n",
                }
            },
            "subroutineBody": {
                "validator": {
                    "expected_token": "{",
                },
                "write": {
                    "non-terminal": "<subroutineBody>\n",
                    "terminal": self.compile_subroutine_body
                }
            }

        }
        return grammar_map

    def _parameter_list_grammar(self):
        grammar_map = {
            "optionalGroup": ("type", "varName"),
            "optionalGroup_2": (",", "type", "varName"),
            "type": {
                "validator": {
                    "expected_token": ('int', 'char', 'boolean', self.tokenizer.IDENTIFIER),
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "varName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER
                },
                "write": {
                    "terminal": partial(self._write_terminal_element, True, None, True)
                }
            },
            ",": {
                "validator": {
                    "expected_token": ",",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
        }
        return grammar_map

    def _subroutine_body_grammar(self):
        grammar_map = {
            "fixPattern": "{",
            "optional": "varDec",
            "fixPattern_2": ("statements", "}"),
            "{": {
                "validator": {
                    "expected_token": "{",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "varDec": {
                "validator": {
                    "expected_token": "var",
                    "optional": True
                },
                "write": {
                    "terminal": self.compile_var_dec
                }
            },
            "statements": {
                "validator": {
                    "expected_token": ("let", "if", "while", "do", "return"),
                },
                "write": {
                    "terminal": self.compile_statements
                }
            },
            "}": {
                "validator": {
                    "expected_token": "}",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            }
        }
        return grammar_map

    def _var_dec_grammar(self):
        grammar_map = {
            "fixPattern": ("var", "type", "varName"),
            "optionalGroup": (",", "varName"),
            "closePattern": ";",
            "var": {
                "validator": {
                    "expected_token": "var"
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "type": {
                "validator": {
                    "expected_token": ('int', 'char', 'boolean', self.tokenizer.IDENTIFIER),
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "varName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER
                },
                "write": {
                    "terminal": partial(self._write_terminal_element, True, None, True)
                }
            },
            ",": {
                "validator": {
                    "expected_token": ",",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            ";": {
                "validator": {
                    "expected_token": ";",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            }
        }
        return grammar_map

    def _let_statement_grammar(self):
        grammar_map = {
            "fixPattern": ("let", "varName"),
            "optionalGroup": ("[", "expression", "]"),
            "fixPattern_2": ("=", "expression", ";"),
            "let": {
                "validator": {
                    "expected_token": "let",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "varName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "[": {
                "validator": {
                    "expected_token": "[",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "expression": {
                "validator": {
                    "force_pass": True
                },
                "write": {
                    "terminal": self.compile_expression
                }
            },
            "]": {
                "validator": {
                    "expected_token": "]"
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "=": {
                "validator": {
                    "expected_token": "=",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            ";": {
                "validator": {
                    "expected_token": ";",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            }
        }
        return grammar_map

    def _do_statement_grammar(self):
        grammar_map = {
            "fixPattern": ("do", "subroutineCall", ";"),
            "do": {
                "validator": {
                    "expected_token": "do",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "subroutineCall": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER,
                },
                "write": {
                    "terminal": self._write_subroutine_call
                }
            },
            ";": {
                "validator": {
                    "expected_token": ";",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            }
        }
        return grammar_map

    def _expression_grammar(self):
        grammar_map = {
            "fixPattern": "term",
            "optionalSubGroup_1": ("(", "expression", ")"),
            "optionalSubGroup_2": ("unary_op", "term"),
            "optionalSubGroup_3": ("varName", "[", "expression", "]"),
            "optionalSubGroup_4": ("subroutineName|className|varName", ".|("),
            "optionalGroup": ("op", "term"),
            "term": {
                "validator": {
                    "force_pass": True
                },
                "write": {
                    "non-terminal": "<term>\n",
                    "terminal": self._write_terminal_element,
                    "non-terminal-close": "</term>\n",
                    "recursive": True
                },
                "recursive": True,
            },
            "(": {
                "validator": {
                    "expected_token": "(",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "expression": {
                "validator": {
                    "force_pass": True
                },
                "write": {
                    "terminal": self.compile_expression
                }
            },
            ")": {
                "validator": {
                    "expected_token": ")",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "unary_op": {
                "validator": {
                    "expected_token": ("-", "~"),
                    "optional": True
                },
                "write": {
                    "non-terminal": "<term>\n",
                    "terminal": self._write_terminal_element,
                    "non-terminal-close": "</term>\n"
                }
            },
            "varName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER,
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "[": {
                "validator": {
                    "expected_token": "[",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "]": {
                "validator": {
                    "expected_token": "]",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "subroutineName|className|varName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER,
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            ".|(": {
                "validator": {
                    "expected_token": (".", "("),
                    "optional": True
                },
                "write": self._write_subroutine_call
            },
            "op": {
                "validator": {
                    "expected_token": self.OP,
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            }
        }
        return grammar_map

    def _subroutine_call_grammar(self):
        grammar_map = {
            "optionalGroup": ("className|varName", "."),
            "fixPattern": ("subroutineName", "(", "expressionList", ")"),
            "className|varName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER,
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            ".": {
                "validator": {
                    "expected_token": ".",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "subroutineName": {
                "validator": {
                    "expected_token_type": self.tokenizer.IDENTIFIER,
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "(": {
                "validator": {
                    "expected_token": "(",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "expressionList": {
                "validator": {
                    "force_pass": True
                },
                "write": {
                    "terminal": self.compile_expression_list
                }
            },
            ")": {
                "validator": {
                    "expected_token": ")",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
        }
        return grammar_map

    def _expression_list_grammar(self):
        grammar_map = {
            "optional": "expression",
            "optionalGroup_2": (",", "expression"),
            "expression": {
                "validator": self._match_expression_grammar,
                "write": {
                    "terminal": self.compile_expression
                }
            },
            ",": {
                "validator": {
                    "expected_token": ",",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
        }
        return grammar_map

    def _return_grammar(self):
        grammar_map = {
            "fixPattern": "return",
            "optional": "expression",
            "closePattern": ";",
            "return": {
                "validator": {
                    "expected_token": "return",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "expression": {
                "validator": self._match_expression_grammar,
                "write": {
                    "terminal": self.compile_expression
                }
            },
            ";": {
                "validator": {
                    "expected_token": ";",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            }
        }
        return grammar_map

    def _if_statement_grammar(self):
        grammar_map = {
            "fixPattern": ("if", "(", "expression", ")", "{", "statements", "}"),
            "optionalGroup": ("else", "{", "statements", "}"),
            "if": {
                "validator": {
                    "expected_token": "if",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "(": {
                "validator": {
                    "expected_token": "(",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "expression": {
                "validator": self._match_expression_grammar,
                "write": {
                    "terminal": self.compile_expression
                }
            },
            ")": {
                "validator": {
                    "expected_token": ")",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "{": {
                "validator": {
                    "expected_token": "{",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "statements": {
                "validator": {
                    "expected_token": self.STATEMENT_KEYWORDS,
                },
                "write": {
                    "terminal": self.compile_statements,
                }
            },
            "}": {
                "validator": {
                    "expected_token": "}",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "else": {
                "validator": {
                    "expected_token": "else",
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            }
        }
        return grammar_map

    def _while_statement_grammar(self):
        grammar_map = {
            "fixPattern": ("while", "(", "expression", ")", "{", "statements", "}"),
            "while": {
                "validator": {
                    "expected_token": "while",
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "(": {
                "validator": {
                    "expected_token": "(",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "expression": {
                "validator": self._match_expression_grammar,
                "write": {
                    "terminal": self.compile_expression
                }
            },
            ")": {
                "validator": {
                    "expected_token": ")",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "{": {
                "validator": {
                    "expected_token": "{",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            },
            "statements": {
                "validator": {
                    "expected_token": self.STATEMENT_KEYWORDS,
                },
                "write": {
                    "terminal": self.compile_statements,
                }
            },
            "}": {
                "validator": {
                    "expected_token": "}",
                },
                "write": {
                    "terminal": self._write_terminal_element,
                }
            }
        }
        return grammar_map


def _file_translation(source_path, options):
    tokenizer = Tokenizer(source_path)
    token_writer = Parser(source_path=source_path, tokenizer=tokenizer, options=options)
    return token_writer.compile_class()


def _dir_translation(source_path, options):
    for file in source_path.iterdir():
        if file.suffix == ".jack":
            tokenizer = Tokenizer(infile=file)
            token_writer = Parser(source_path=file, tokenizer=tokenizer, options=options)
            token_writer.compile_class()
    return


def main(arguments):
    source_path = Path(arguments.path)
    translate_method = _file_translation if source_path.is_file() else _dir_translation
    return partial(translate_method, source_path, arguments)()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to source code to be compiled")
    parser.add_argument("--xml", help="If specified, parser writes xml", action="store_true")
    parser.add_argument("--ident", help="If specified, parser writes identifier spec to xml", action="store_true")
    parser.add_argument("--verbose", help="If specified, all modules logs in debug mode", action="store_true")

    args = parser.parse_args()
    if args.ident and not args.xml:
        parser.error('--xml is required when --ident is set.')
    main(arguments=args)
