import logging


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
        self.logger = self._setup_logger()

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
                self.logger.debug(f"Current line to process: {code_snippet}")
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

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger(__name__)
        return logger
