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


class Writer:
    def __init__(self, source_path, tokenizer):
        self.source_p = source_path
        self.outfile = self._construct_outfile_path()
        self.tokenizer = tokenizer

    def _construct_outfile_path(self):
        return Path(self.source_p.parent, f"{self.source_p.stem}TTT").with_suffix(".xml")

    def write(self):
        __logger__.info(f"Writing: {self.outfile}")
        with open(self.outfile, "w") as outfile:
            outfile.write("<tokens>\n")
            token = self.tokenizer.next_token()
            while self.tokenizer.has_more_token:
                if token:
                    token_type = self.tokenizer.get_token_type()
                    get_value = getattr(self.tokenizer, token_type)
                    outfile.write(f"<{token_type}>{get_value()}</{token_type}>\n")
                    token = self.tokenizer.next_token()
            outfile.write("</tokens>\n")


def _file_translation(source_path):
    tokenizer = Tokenizer(source_path)
    token_writer = Writer(source_path, tokenizer)
    return token_writer.write()


def _dir_translation(source_path):
    for file in source_path.iterdir():
        if file.suffix == ".jack":
            tokenizer = Tokenizer(infile=file)
            token_writer = Writer(source_path=file, tokenizer=tokenizer)
            token_writer.write()
    return


def main(source):
    source_path = Path(source)
    translate_method = _file_translation if source_path.is_file() else _dir_translation
    return partial(translate_method, source_path)()


if __name__ == '__main__':
    input_path = sys.argv[1]
    main(source=input_path)