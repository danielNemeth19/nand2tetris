import sys
import logging
from functools import partial
from pathlib import Path

__logger__ = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Tokenizer:
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STR_CONST = "stringConstant"

    KEYWORDS = (
        "class", "constructor", "function", "method", "field", "static",
        "var", "int", "char", "boolean", "void", "true", "false", "null",
        "this", "let", "do", "if", "else", "while", "return"
    )
    SYMBOLS = (
        "{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"
    )

    def __init__(self, infile):
        self._source = open(infile, "r").readlines()
        self._code = iter(self._source)
        self.current_line = None
        self.current_token = True
        self.tokens = None
        self.has_more_token = True

    def _token_builder(self, token=None, tokens=None, str_const=False):
        tokens = tokens if tokens else list()
        token = token if token else ""
        try:
            char = next(self.current_line)
        except StopIteration:
            if token:
                tokens.append(token)
            return tokens
        if char == "\"":
            str_const = False if token else True
            if token:
                tokens.append(f"\"{token}\"")
            return self._token_builder(tokens=tokens, str_const=str_const)
        elif char in self.SYMBOLS and not str_const:
            if token:
                tokens.append(token)
            tokens.append(char)
            return self._token_builder(tokens=tokens)
        elif char != " " or str_const:
            token += char
            return self._token_builder(token, tokens, str_const)
        elif char == " ":
            if token:
                tokens.append(token)
            return self._token_builder(tokens=tokens)
        return tokens

    def get_next_code_snippet(self):
        item = next(self._code).strip()
        if item.startswith("//") or not item:
            return self.get_next_code_snippet()
        elif item.startswith("/**"):
            while not item.endswith("*/"):
                item = self.get_next_code_snippet()
            return self.get_next_code_snippet()
        code_snippet = item.strip().split("//")[0].strip()
        return code_snippet

    def next_token(self):
        try:
            self.current_token = next(self.tokens)
        except (TypeError, StopIteration):
            try:
                code_snippet = self.get_next_code_snippet()
                __logger__.debug(f"Current line to process: {code_snippet}")
                self.current_line = iter(code_snippet)
                tokens = self._token_builder()
                self.tokens = iter(tokens)
                return self.next_token()
            except StopIteration:
                self.has_more_token = False
                self.current_token = False
        return self.current_token

    def get_token_type(self):
        if self.current_token.startswith("\"") and self.current_token.endswith("\""):
            return self.STR_CONST
        if self.current_token in self.KEYWORDS:
            return self.KEYWORD
        elif self.current_token in self.SYMBOLS:
            return self.SYMBOL
        try:
            int(self.current_token)
        except ValueError:
            return self.IDENTIFIER
        return self.INT_CONST

    def keyword(self):
        return self.current_token

    def symbol(self):
        special_chars_map = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;"
        }
        self.current_token = special_chars_map.get(
            self.current_token, self.current_token
        )
        return self.current_token

    def identifier(self):
        return self.current_token

    def integerConstant(self):
        return self.current_token

    def stringConstant(self):
        return self.current_token[1:-1]


class Parser:
    STATEMENT_KEYWORDS = ("let", "if", "while", "do", "return")
    OP = ("+", "-", "*", "/", "&", "|", "<", ">", "=")
    UNARY_OP = ("-", "~")
    KEYWORD_CONSTANTS = ("true", "false", "null", "this")

    def __init__(self, source_path, tokenizer):
        self.source_p = source_path
        self.outfile = self._construct_outfile_path()
        self.tokenizer = tokenizer
        self.file = open(self.outfile, 'w')

    def _construct_outfile_path(self):
        return Path(self.source_p.parent, f"{self.source_p.stem}").with_suffix(".xml")

    def compile_class(self):
        class_grammar = self._class_grammar()
        __logger__.info(f"Writing: {self.outfile}")
        for elem in class_grammar["fixpattern"]:
            elem_grammar = class_grammar[elem]
            self.tokenizer.next_token()
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if "non-terminal" in elem_grammar["write"]:
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
                self.file.write(grammar["write"]["non-terminal"])
                grammar["write"]["terminal"]()

        close_grammar = self._get_close_pattern_grammar(class_grammar)
        __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
        validator_kwargs = close_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            close_grammar["write"]["terminal"]()

        self._write_non_terminal_tag("class", open_tag=False)
        return self.file.close()

    def compile_class_var_dec(self):
        class_var_dec_grammar = self._class_var_dec_grammar()
        self._write_non_terminal_tag("classVarDec")
        for elem in class_var_dec_grammar["fixPattern"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = class_var_dec_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if "non-terminal" in elem_grammar["write"]:
                    self.file.write(elem_grammar["write"]["non-terminal"])
                elem_grammar["write"]["terminal"]()

        while self._if_optional_group_applies(class_var_dec_grammar):
            for elem in class_var_dec_grammar["optionalGroup"]:
                __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = class_var_dec_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    elem_grammar["write"]["terminal"]()

        close_grammar = self._get_close_pattern_grammar(class_var_dec_grammar)
        __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
        validator_kwargs = close_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            close_grammar["write"]["terminal"]()
        self._write_non_terminal_tag("classVarDec", open_tag=False)

        if self.block_is_not_done(class_var_dec_grammar):
            return self.compile_class_var_dec()
        return

    def compile_subroutine_dec(self):
        subroutine_dec_grammar = self._subroutine_dec_grammar()
        for elem in subroutine_dec_grammar["fixPattern"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = subroutine_dec_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if "non-terminal" in elem_grammar["write"]:
                    self.file.write(elem_grammar["write"]["non-terminal"])
                elem_grammar["write"]["terminal"]()
        self._write_non_terminal_tag("subroutineDec", open_tag=False)

    def compile_parameter_list(self):
        parameter_list_grammar = self._parameter_list_grammar()
        if self._if_optional_group_applies(parameter_list_grammar):
            for elem in parameter_list_grammar["optionalGroup"]:
                __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = parameter_list_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    elem_grammar["write"]["terminal"]()

        while self._if_optional_group_applies(parameter_list_grammar, optional_group_key="optionalGroup_2"):
            for elem in parameter_list_grammar["optionalGroup_2"]:
                __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = parameter_list_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    elem_grammar["write"]["terminal"]()

    def compile_subroutine_body(self):
        subroutine_body_grammar = self._subroutine_body_grammar()
        for elem in subroutine_body_grammar["fixPattern"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = subroutine_body_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if "non-terminal" in elem_grammar["write"]:
                    self.file.write(elem_grammar["write"]["non-terminal"])
                elem_grammar["write"]["terminal"]()

        if self._if_optional_grammar_applies(subroutine_body_grammar):
            optional_grammar = subroutine_body_grammar["optional"]
            elem_grammar = subroutine_body_grammar[optional_grammar]
            __logger__.info(f"token is: {self.tokenizer.current_token}, matched grammar: {optional_grammar}")
            elem_grammar["write"]["terminal"]()

        for elem in subroutine_body_grammar["fixPattern_2"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = subroutine_body_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()
        self._write_non_terminal_tag(elem="subroutineBody", open_tag=False)

    def compile_var_dec(self):
        var_dec_grammar = self._var_dec_grammar()
        self._write_non_terminal_tag("varDec")
        for elem in var_dec_grammar["fixPattern"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = var_dec_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                if "non-terminal" in elem_grammar["write"]:
                    self.file.write(elem_grammar["write"]["non-terminal"])
                elem_grammar["write"]["terminal"]()

        while self._if_optional_group_applies(var_dec_grammar):
            for elem in var_dec_grammar["optionalGroup"]:
                __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = var_dec_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    elem_grammar["write"]["terminal"]()

        close_grammar = self._get_close_pattern_grammar(var_dec_grammar)
        __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")

        validator_kwargs = close_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            close_grammar["write"]["terminal"]()
        self._write_non_terminal_tag("varDec", open_tag=False)

        if self.block_is_not_done(var_dec_grammar):
            return self.compile_var_dec()
        return

    def compile_statements(self):
        self._write_non_terminal_tag(elem="statements")
        while self.tokenizer.current_token in self.STATEMENT_KEYWORDS:
            func = getattr(self, f"compile_{self.tokenizer.current_token}_statement")
            func()
        self._write_non_terminal_tag(elem="statements", open_tag=False)

    def compile_let_statement(self):
        let_grammar = self._let_statement_grammar()
        self._write_non_terminal_tag(elem="letStatement")
        for elem in let_grammar["fixPattern"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = let_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()

        if self._if_optional_group_applies(let_grammar):
            for elem in let_grammar["optionalGroup"]:
                __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = let_grammar[elem]
                validator_kwargs = elem_grammar["validator"]
                if self._match_grammar(**validator_kwargs):
                    elem_grammar["write"]["terminal"]()

        for elem in let_grammar["fixPattern_2"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = let_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()
        self._write_non_terminal_tag(elem="letStatement", open_tag=False)

    def compile_if_statement(self):
        if_grammar = self._if_statement_grammar()
        self._write_non_terminal_tag(elem="ifStatement")
        for elem in if_grammar["fixPattern"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = if_grammar[elem]
            validator_obj = elem_grammar["validator"]
            if isinstance(validator_obj, dict):
                if self._match_grammar(**validator_obj):
                    elem_grammar["write"]["terminal"]()
            else:
                if validator_obj():
                    elem_grammar["write"]["terminal"]()

        if self._if_optional_group_applies(block_grammar=if_grammar):
            for elem in if_grammar["optionalGroup"]:
                __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
                elem_grammar = if_grammar[elem]
                validator_obj = elem_grammar["validator"]
                if isinstance(validator_obj, dict):
                    if self._match_grammar(**validator_obj):
                        elem_grammar["write"]["terminal"]()
                else:
                    if validator_obj():
                        elem_grammar["write"]["terminal"]()

        self._write_non_terminal_tag(elem="ifStatement", open_tag=False)

    def compile_while_statement(self):
        while_grammar = self._while_statement_grammar()
        self._write_non_terminal_tag(elem="whileStatement")
        for elem in while_grammar["fixPattern"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = while_grammar[elem]
            validator_obj = elem_grammar["validator"]
            if isinstance(validator_obj, dict):
                if self._match_grammar(**validator_obj):
                    elem_grammar["write"]["terminal"]()
            else:
                if validator_obj():
                    elem_grammar["write"]["terminal"]()
        self._write_non_terminal_tag(elem="whileStatement", open_tag=False)

    def compile_do_statement(self):
        do_grammar = self._do_statement_grammar()
        self._write_non_terminal_tag(elem="doStatement")
        for elem in do_grammar["fixPattern"]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = do_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()
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
            optional_grammar["write"]["terminal"]()

        close_grammar = self._get_close_pattern_grammar(return_grammar)
        __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
        validator_kwargs = close_grammar["validator"]
        if self._match_grammar(**validator_kwargs):
            close_grammar["write"]["terminal"]()
        self._write_non_terminal_tag(elem="returnStatement", open_tag=False)

    def compile_expression(self):
        expression_grammar = self._expression_grammar()
        self._write_non_terminal_tag(elem="expression")
        term_grammar = self._get_fixpattern_grammar(expression_grammar)
        __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")

        def _compile_term():
            if self.is_simple_term():
                self._handle_simple_term(term_grammar)
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
                            elem_grammar["write"]["terminal"]()
                        else:
                            _compile_term()
                self._write_non_terminal_tag("term", open_tag=False)

            elif self._is_identifier():
                self._write_non_terminal_tag("term")
                cached_token_dict = self._lookahead_for_next_token()
                if self._if_optional_group_applies(
                        expression_grammar, optional_group_key="optionalSubGroup_3", index=1
                ):
                    self._write_terminal_element_from_cache(cached_token_dict)
                    for elem in expression_grammar["optionalSubGroup_3"][1:]:
                        elem_grammar = expression_grammar[elem]
                        validator_kwargs = elem_grammar["validator"]
                        if self._match_grammar(**validator_kwargs):
                            elem_grammar["write"]["terminal"]()

                elif self._if_optional_group_applies(
                        expression_grammar, optional_group_key="optionalSubGroup_4", index=1
                ):
                    self._write_subroutine_call(cached_token_dict)
                else:
                    self._write_terminal_element_from_cache(cached_token_dict)
                self._write_non_terminal_tag("term", open_tag=False)

        _compile_term()
        while self._if_optional_group_applies(expression_grammar):
            for optional_elem in expression_grammar["optionalGroup"]:
                optional_grammar = expression_grammar[optional_elem]
                optional_validator_kwargs = optional_grammar["validator"]
                if self._match_grammar(**optional_validator_kwargs):
                    recursive = optional_grammar.get("recursive", False)
                    if not recursive:
                        optional_grammar["write"]["terminal"]()
                    else:
                        _compile_term()

        self._write_non_terminal_tag(elem="expression", open_tag=False)

    def _handle_simple_term(self, grammar):
        self.file.write(grammar["write"]['non-terminal'])
        grammar["write"]["terminal"]()
        self.file.write(grammar["write"]['non-terminal-close'])

    def _write_subroutine_call(self, cached_token_dict=None):
        subroutine_grammar = self._subroutine_call_grammar()
        if cached_token_dict:
            applicable = True if self.tokenizer.current_token == "." else False
        else:
            applicable, cached_token_dict = self.look_ahead_for_optional_grammar(subroutine_grammar)
        self._write_terminal_element_from_cache(cached_token_dict)
        if applicable:
            elem = subroutine_grammar["optionalGroup"][1]
            elem_grammar = subroutine_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()

        fix_pattern_index = 0 if applicable else 1
        for elem in subroutine_grammar["fixPattern"][fix_pattern_index:]:
            __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
            elem_grammar = subroutine_grammar[elem]
            validator_kwargs = elem_grammar["validator"]
            if self._match_grammar(**validator_kwargs):
                elem_grammar["write"]["terminal"]()

    def compile_expression_list(self):
        expression_list_grammar = self._expression_list_grammar()
        self._write_non_terminal_tag(elem="expressionList")
        optional_grammar = self._get_optional_grammar(expression_list_grammar)
        if optional_grammar["validator"]():
            optional_grammar["write"]["terminal"]()
            while self._if_optional_group_applies(expression_list_grammar, optional_group_key="optionalGroup_2"):
                for elem in expression_list_grammar["optionalGroup_2"]:
                    __logger__.info(f"Matching grammar for: {self.tokenizer.current_token}")
                    elem_grammar = expression_list_grammar[elem]
                    validator_obj = elem_grammar["validator"]
                    if isinstance(validator_obj, dict):
                        if self._match_grammar(**validator_obj):
                            elem_grammar["write"]["terminal"]()
                    else:
                        if validator_obj():
                            elem_grammar["write"]["terminal"]()
        self._write_non_terminal_tag(elem="expressionList", open_tag=False)

    def _write_terminal_element(self, advance_token=True):
        token_type = self.tokenizer.get_token_type()
        get_value = getattr(self.tokenizer, token_type)
        self.file.write(f"<{token_type}>{get_value()}</{token_type}>\n")
        if advance_token:
            self.tokenizer.next_token()

    def _write_terminal_element_from_cache(self, cached_token_dict):
        token_type = cached_token_dict.get("cached_token_type")
        token_value = cached_token_dict.get("cached_token")
        self.file.write(f"<{token_type}>{token_value}</{token_type}>\n")

    def write_non_terminal_close_tag(self, block_grammar):
        closing_elem = block_grammar["closePattern"]
        close_tag = block_grammar[closing_elem]["write"]["non-terminal"]
        self.file.write(close_tag)

    def _write_non_terminal_tag(self, elem, open_tag=True):
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
        __logger__.error(f"Expected: type: '{expected_token_type}', token: '{expected_token}'."
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

    def is_simple_term(self):
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
                    "expected_token": self.source_p.stem,
                    "expected_token_type": self.tokenizer.IDENTIFIER
                },
                "write": {
                    "terminal": partial(self._write_terminal_element, False)
                }
            },
            "{": {
                "validator": {
                    "expected_token": "{",
                    "expected_token_type": self.tokenizer.SYMBOL
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
                    "terminal": self._write_terminal_element
                }
            },
            ",": {
                "validator": {
                    "expected_token": ",",
                    "expected_token_type": self.tokenizer.SYMBOL,
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
                    "expected_token_type": self.tokenizer.SYMBOL
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
                    "expected_token_type": self.tokenizer.SYMBOL
                },
                "write": {
                    "terminal": self._write_terminal_element,
                    "non-terminal": "</parameterList>\n",
                }
            },
            "subroutineBody": {
                "validator": {
                    "expected_token": "{",
                    "expected_token_type": self.tokenizer.SYMBOL
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
                    "terminal": self._write_terminal_element
                }
            },
            ",": {
                "validator": {
                    "expected_token": ",",
                    "expected_token_type": self.tokenizer.SYMBOL,
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
                    "expected_token_type": self.tokenizer.SYMBOL
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            "varDec": {
                "validator": {
                    "expected_token": "var",
                    "expected_token_type": self.tokenizer.KEYWORD,
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
                    "terminal": self._write_terminal_element
                }
            },
            ",": {
                "validator": {
                    "expected_token": ",",
                    "expected_token_type": self.tokenizer.SYMBOL,
                    "optional": True
                },
                "write": {
                    "terminal": self._write_terminal_element
                }
            },
            ";": {
                "validator": {
                    "expected_token": ";",
                    "expected_token_type": self.tokenizer.SYMBOL
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
                    "expected_token_type": self.tokenizer.SYMBOL
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
                    "expected_token_type": self.tokenizer.SYMBOL
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


def _file_translation(source_path):
    tokenizer = Tokenizer(source_path)
    token_writer = Parser(source_path, tokenizer)
    return token_writer.compile_class()


def _dir_translation(source_path):
    for file in source_path.iterdir():
        if file.suffix == ".jack":
            tokenizer = Tokenizer(infile=file)
            token_writer = Parser(source_path=file, tokenizer=tokenizer)
            token_writer.compile_class()
    return


def main(source):
    source_path = Path(source)
    translate_method = _file_translation if source_path.is_file() else _dir_translation
    return partial(translate_method, source_path)()


if __name__ == '__main__':
    input_path = sys.argv[1]
    main(source=input_path)