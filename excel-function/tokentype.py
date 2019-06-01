class TokenType:
    value = None

    @staticmethod
    def get_type():
        return 1

    def get_token_value(self, query, start_index):
        return NotImplementedError()


class FieldTokenType(TokenType):
    value = "Field"

    def get_token_value(self, query, start_index):
        i = 1
        while query[start_index + i] != '"':
            i += 1
        return (query[start_index + 1:start_index + i], start_index + i + 1)


print(FieldTokenType().get_token_value('15 * "Hello" + 12', 5))
