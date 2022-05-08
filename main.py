from Lexer import nfa_definition
from Lexer.lexer import *
from Parser.parser import Parser, Terminals
import os
print(os.getcwd())


def main():

    print("\nWelcome to SQL-- Compiler Front-end!")
    print("\t1. Read the SQL statement from the file\n" \
          "\t2. Input SQL statement from terminal")
    option = input('> ')

    # lexer
    nfa = NFA(nfa_definition.nfa_start, nfa_definition.nfa_accept, nfa_definition.nfa_trans)
    dfa = nfa.nfa2dfa()
    minimized_dfa = dfa.dfa_minimization()
    filepath = os.getcwd() + '\\Test\\Output\\'
    lexer = Lexer(minimized_dfa)

    # parser
    start_symbol = 'root'
    grammar_file = r'Parser\grammar.txt'
    parser = Parser(terminals=Terminals, grammar_file=grammar_file, start_symbol=start_symbol)

    sql_filepath = os.getcwd() + '\\Test\\Input\\'

    if int(option) == 1:
        file_name = input('\nPleas input file name > ')
        sql_filepath += file_name

        with open(sql_filepath) as fp:
            text = fp.read()

        group = file_name.split('.')[0][-1]

        print('\n----------------------  LEXICAL ANALYSIS ----------------------')
        lexer.lexical_analysis(text, filepath + f'47{group}lex.tsv')
        print('---------------------------------------------------------------')

        print('\n\n')
        print('-----------------------  SYNTAX ANALYSIS ----------------------')
        lexer.print_tokens_keyword()
        parser.parse_tokens(lexer.tokens, filepath + f'47{group}gra.tsv')
        print('---------------------------------------------------------------')

    elif int(option) == 2:

        while True:
            text = input('\nsql > ')

            print('\n----------------------  LEXICAL ANALYSIS ----------------------')
            lexer.lexical_analysis(text, filepath + 'lex.tsv')
            print('---------------------------------------------------------------')

            print('\n\n')
            print('-----------------------  SYNTAX ANALYSIS ----------------------')
            lexer.print_tokens_keyword()
            parser.parse_tokens(lexer.tokens, filepath + 'gra.tsv')
            print('---------------------------------------------------------------')


if __name__ == '__main__':
    main()

