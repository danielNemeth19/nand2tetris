import logging


class SymbolTable:
    def __init__(self, is_class=False):
        self.is_class = is_class
        self.table = dict()
        self.var_counter = self._setup_counter()
        self.logger = self._setup_logger()

    def _setup_counter(self):
        if self.is_class:
            return dict(field=-1, static=-1)
        return dict(argument=-1, var=-1)

    def start_subroutine(self):
        if self.is_class:
            raise NotImplementedError
        self.table = dict()
        self.var_counter = dict(argument=-1, var=-1)

    def define(self, cached_data):
        name = cached_data.pop()
        ident_spec = dict(type=None, kind=None)

        for key, token in zip(ident_spec, reversed(cached_data)):
            ident_spec[key] = token

        index = self.var_counter.get(ident_spec["kind"]) + 1
        ident_spec["index"] = index
        self.table[name] = ident_spec
        self.var_counter[ident_spec["kind"]] = index
        self.logger.debug(f"Current table: {self.table}")
        return

    def var_count(self, kind):
        count = 0
        for name, spec in self.table.items():
            if "kind" in spec:
                if spec["kind"] == kind:
                    count += 1
        return count

    def kind_of(self, token):
        try:
            kind = self.table[token].get("kind", None)
            return kind
        except KeyError:
            self.logger.debug(f"Unknown token: {token}")
            return None

    def type_of(self, token):
        try:
            token_type = self.table[token].get("type", None)
            return token_type
        except KeyError:
            self.logger.debug(f"Unknown token: {token}")
            return None

    def index_of(self, token):
        try:
            index_of = self.table[token].get("index", None)
            return index_of
        except KeyError:
            self.logger.debug(f"Unknown token: {token}")
            return None

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger(__name__)
        return logger
