token_types = ['IgnoreTokenType', 'FieldTokenType', 'NumberTokenType', 'BinaryOperatorTokenType',
               'GroupSymbolTokenType']

GROUP_SYMBOL = {
    'open': '[',
    'close': ']'
}


class TokenType:
    value = None
    symbols = None

    @staticmethod
    def get_type():
        return 1

    @staticmethod
    def get_token_type(start_of_query):
        for token_type in token_types:
            if eval('%s.is_this_type(start_of_query)' % token_type):
                return eval(token_type)

    @staticmethod
    def get_token_value(query, start_index):
        return NotImplementedError()

    @staticmethod
    def is_this_type(start_of_query):
        return NotImplementedError()


class IgnoreTokenType(TokenType):
    value = "Ignore"
    symbols = ' '

    @staticmethod
    def get_token_value(query, start_index):
        i = 1
        while query[start_index + i] in IgnoreTokenType.symbols:
            i += 1
        return Token(None, IgnoreTokenType.value), start_index + i

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] in IgnoreTokenType.symbols


class FieldTokenType(TokenType):
    value = "Field"
    symbols = '"'

    @staticmethod
    def get_token_value(query, start_index):
        i = 1
        while query[start_index + i] != FieldTokenType.symbols:
            i += 1
        return Token(query[start_index + 1:start_index + i], FieldTokenType.value), start_index + i + 1

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] == FieldTokenType.symbols


class NumberTokenType(TokenType):
    value = "OPERAND"
    symbols = '0123456789.'

    @staticmethod
    def get_token_value(query, start_index):
        i = 1
        while start_index + i < len(query) and query[start_index + i] in NumberTokenType.symbols:
            i += 1
        value = query[start_index:start_index + i]
        if '.' in value:
            value = float(value)
        else:
            value = int(value)

        return Token(value, NumberTokenType.value), start_index + i

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] in NumberTokenType.symbols


class BinaryOperatorTokenType(TokenType):
    value = "BinaryOperator"
    symbols = '+-*/'
    binary_operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }

    @staticmethod
    def get_token_value(query, start_index):
        operator = query[start_index]
        return Token(BinaryOperatorTokenType.binary_operations[operator],
                     BinaryOperatorTokenType.value), start_index + 1

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] in BinaryOperatorTokenType.symbols


class GroupSymbolTokenType(TokenType):
    value = "QUERY"
    symbols = GROUP_SYMBOL.values()

    @staticmethod
    def get_token_value(query, start_index):
        i = 1
        open_count = 1
        while start_index + i < len(query) and open_count > 0:
            if query[start_index + i] == GROUP_SYMBOL['open']:
                open_count += 1
            elif query[start_index + i] == GROUP_SYMBOL['close']:
                open_count -= 1
            i += 1

        return Token(tokenize(query[start_index + 1: start_index + i - 1]), GroupSymbolTokenType.value), start_index + i

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] in GroupSymbolTokenType.symbols


class Token:

    def __init__(self, value, token_type):
        self.value = value
        self.token_type = token_type


def tokenize(query):
    tokens = []
    start_index = 0

    while start_index < len(query):
        token_type = TokenType.get_token_type(query[start_index:])
        token, start_index = token_type.get_token_value(query, start_index)

        if token.token_type != IgnoreTokenType.value:
            tokens.append(token)

    return tokens


def binary_executor(query_tokens):
    operands = []
    operators = []
    for token in query_tokens:
        if token.token_type == GroupSymbolTokenType.value:
            token = Token(binary_executor(token.value), NumberTokenType.value)

        if token.token_type == NumberTokenType.value:
            if len(operators) == 0:
                operands.append(token)
            else:
                operands.append(Token(operators.pop().value(operands.pop().value, token.value), NumberTokenType.value))
        elif token.token_type == BinaryOperatorTokenType.value:
            operators.append(token)

    return operands[0].value


# query = '455 / 15.2 * "Hello" + 12'
query = '1 + [[[15 / 2] + [5 * 2]] * 2]'
print(binary_executor(tokenize(query)))
