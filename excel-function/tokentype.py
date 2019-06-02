token_types = ['IgnoreTokenType', 'FieldTokenType', 'NumberTokenType', 'BinaryOperatorTokenType',
               'GroupSymbolTokenType', 'FunctionTokenType']

GROUP_SYMBOL = {
    'open': '[',
    'close': ']'
}

FUNCTION_SYMBOL = {
    'open': '(',
    'close': ')',
    'arg_separator': ','
}

FUNCTIONS = {
    'sum': lambda args: sum(args),
    'if': lambda args: args[1] if args[0] else args[2]
}


def query_executor(query_tokens):
    operands = []
    operators = []
    for token in query_tokens:
        if token.token_type == GroupSymbolTokenType.value:
            token = Token(query_executor(token.value), NumberTokenType.value)
        elif token.token_type == FieldTokenType.value:
            token = Token(extract_field_value(token.value), NumberTokenType.value)
        elif token.token_type == FunctionTokenType.value:
            func = FUNCTIONS[token.value['function_name']]
            args = token.value['arguments']
            token = Token(func(args), NumberTokenType.value)

        if token.token_type == NumberTokenType.value:
            if len(operators) == 0:
                operands.append(token)
            else:
                operands.append(Token(operators.pop().value(operands.pop().value, token.value), NumberTokenType.value))
        elif token.token_type == BinaryOperatorTokenType.value:
            operators.append(token)

    return operands[0].value


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
    def get_token_and_start_index(query, start_index):
        return NotImplementedError()

    @staticmethod
    def is_this_type(start_of_query):
        return NotImplementedError()


class IgnoreTokenType(TokenType):
    value = "Ignore"
    symbols = ' '

    @staticmethod
    def get_token_and_start_index(query, start_index):
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
    def get_token_and_start_index(query, start_index):
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
    def get_token_and_start_index(query, start_index):
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
    symbols = '+-*/><'
    binary_operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y
    }

    @staticmethod
    def get_token_and_start_index(query, start_index):
        operator = query[start_index]
        return Token(BinaryOperatorTokenType.binary_operations[operator],
                     BinaryOperatorTokenType.value), start_index + 1

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] in BinaryOperatorTokenType.symbols


class FunctionTokenType(TokenType):
    value = "FUNCTION"
    symbols = 'abcdefghijklmnopqrstuvwxyz'

    @staticmethod
    def get_token_and_start_index(query, start_index):
        i = 1
        while start_index + i < len(query) and query[start_index + i] != FUNCTION_SYMBOL['open']:
            i += 1
        function_name = query[start_index: start_index + i]
        j = i + 1
        arg_start = j
        open_count = 1
        arguments = []
        while start_index + j < len(query) and open_count > 0:
            if query[start_index + j] == FUNCTION_SYMBOL['open']:
                open_count += 1
            if query[start_index + j] == FUNCTION_SYMBOL['close']:
                open_count -= 1
            if query[start_index + j] == FUNCTION_SYMBOL['arg_separator'] and open_count == 1:
                arguments.append(query[start_index + arg_start: start_index + j])
                arg_start = j + 1

            j += 1
        arguments.append(query[start_index + arg_start: start_index + j - 1])
        executed_arguments = [query_executor(tokenize(arg)) for arg in arguments]

        return Token({'function_name': function_name, 'arguments': executed_arguments},
                     FunctionTokenType.value), start_index + j + 1

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] in FunctionTokenType.symbols


class GroupSymbolTokenType(TokenType):
    value = "QUERY"
    symbols = GROUP_SYMBOL.values()

    @staticmethod
    def get_token_and_start_index(query, start_index):
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
        token, start_index = token_type.get_token_and_start_index(query, start_index)

        if token.token_type != IgnoreTokenType.value:
            tokens.append(token)

    return tokens


def extract_field_value(field_name):
    return 10


# query = '455 / 15.2 * "Hello" + 12'
query = '10 + if( 30 > 12 * 2, 2, 100)'
print(query_executor(tokenize(query)))
