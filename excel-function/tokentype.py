token_types = ['IgnoreTokenType', 'FieldTokenType', 'NumberTokenType']


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
        return None, start_index + i

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
        return query[start_index + 1:start_index + i], start_index + i + 1

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] == FieldTokenType.symbols


class NumberTokenType(TokenType):
    value = "Number"
    symbols = '0123456789.'

    @staticmethod
    def get_token_value(query, start_index):
        i = 1
        while query[start_index + i] in NumberTokenType.symbols:
            i += 1
        value = query[start_index:start_index + i]
        if '.' in value:
            value = float(value)
        else:
            value = int(value)

        return value, start_index + i

    @staticmethod
    def is_this_type(start_of_query):
        return start_of_query[0] in NumberTokenType.symbols


def tokenize(query):
    tokens = []
    start_index = 0

    while start_index < len(query):
        token_type = TokenType.get_token_type(query[start_index:])
        value, start_index = token_type.get_token_value(query, start_index)

        if value != None:
            tokens.append(value)

    return tokens


# query = '455 / 15.2 * "Hello" + 12'
query = '  455  "Hello"  78.24  "Renuka"  "Fernando"'
print(tokenize(query))
