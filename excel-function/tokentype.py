token_types = ['FieldTokenType', 'NumberTokenType']


class TokenType:
    value = None

    @staticmethod
    def get_type():
        return 1

    @staticmethod
    def get_token_type(start_of_query):
        for token_type in token_types:
            if eval('%s.is_this_type(start_of_query)' % token_type):
                return NumberTokenType

    @staticmethod
    def get_token_value(query, start_index):
        return NotImplementedError()

    @staticmethod
    def is_this_type(start_of_query):
        return NotImplementedError()


class FieldTokenType(TokenType):
    value = "Field"

    @staticmethod
    def get_token_value(query, start_index):
        i = 1
        while query[start_index + i] != '"':
            i += 1
        return query[start_index + 1:start_index + i], start_index + i + 1

    @staticmethod
    def is_this_type(start_of_query):
        return False


class NumberTokenType(TokenType):
    value = "Number"

    @staticmethod
    def get_token_value(query, start_index):
        i = 1
        while query[start_index + i] in '0123456789.':
            i += 1
        return query[start_index:start_index + i], start_index + i

    @staticmethod
    def is_this_type(start_of_query):
        return True


print(TokenType.get_token_type('').get_token_value('455 / 15.2 * "Hello" + 12', 6))
