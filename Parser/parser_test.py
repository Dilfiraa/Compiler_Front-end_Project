from Lexer.lexer import Token
from Parser.parser import Parser, Terminals


def keyword_list_to_token(token_keyword_list):
    token_list = []
    for keyword in token_keyword_list:
        token_list.append(Token(None, None, None, keyword, None))
    return token_list

def print_keyword(token_list):
    for token in token_list:
        print(token.keyword, end=' ')
    print()


start_symbol = 'root'
grammar_file = 'grammar.txt'

token_keywords = ['SELECT', 'IDN', '.', 'IDN', 'FROM', 'IDN', 'WHERE', 'IDN', '.', 'IDN', '>', 'INT']
tokens = keyword_list_to_token(token_keywords)


parser = Parser(terminals=Terminals, grammar_file=grammar_file, start_symbol=start_symbol)
parser.parse_tokens(tokens)


