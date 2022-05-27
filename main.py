from Lexer import nfa_definition
from Lexer.lexer import *
from Parser.parser import *
import os


def main():
    # symbol table
    symbol_table= SymbolTable()

    # lexer
    nfa = NFA(nfa_definition.nfa_start, nfa_definition.nfa_accept, nfa_definition.nfa_trans)
    dfa = nfa.nfa2dfa()
    minimized_dfa = dfa.dfa_minimization()
    filepath = os.getcwd() + '\\Test\\Output\\'
    lexer = Lexer(minimized_dfa, symbol_table)

    # parser
    start_symbol = 'root'
    grammar_file = r'Parser\grammar.txt'
    parser = Parser(Terminals, grammar_file, start_symbol, symbol_table)

    sql_filepath = os.getcwd() + '\\Test\\Input\\'

    print("\n+---------------------------------------------------+")
    print("|\tWelcome to SQL-- Compiler Front-end!\t\t\t|")
    print("|\t\t1. Read the SQL statement from the file\t\t|\n"
          "|\t\t2. Input SQL statement from terminal\t\t|")
    print("+---------------------------------------------------+")

    while True:

        print("\nPlease input 1 or 2 to parse sql statement or input exit to exit.")
        option = input('> ')

        try:
            option = int(option)
        except ValueError:
            pass

        if option == 1:
            file_name = input('\nPleas input file name > ')
            sql_filepath += file_name

            try:
                with open(sql_filepath) as fp:
                    text = fp.read()
            except FileNotFoundError:
                print("Error: Please check if the file name is correct or if the file is in the Test/input folder.")
                continue

            group = file_name.split('.')[0][-1]

            print('\n----------------------  LEXICAL ANALYSIS ----------------------')
            lexer.lexical_analysis(text, filepath + f'47{group}lex.tsv')
            print('---------------------------------------------------------------')

            print('\n\n')
            print('-----------------------  SYNTAX ANALYSIS ----------------------')
            lexer.print_tokens_keyword()
            parser.parse_tokens(lexer.tokens, filepath + f'47{group}gra.tsv')
            print('---------------------------------------------------------------')

        elif option == 2:

            text = input('\nsql > ')

            print('\n----------------------  LEXICAL ANALYSIS ----------------------')
            lexer.lexical_analysis(text, filepath + 'lex.tsv')
            print('---------------------------------------------------------------')

            print('\n\n')
            print('-----------------------  SYNTAX ANALYSIS ----------------------')
            lexer.print_tokens_keyword()
            parser.parse_tokens(lexer.tokens, filepath + 'gra.tsv')
            print('---------------------------------------------------------------')

            symbol_table.print_table()

        elif option == 'exit':
            break

        else:
            print("Error: Pleas input 1 ,2 or exit.\n")


if __name__ == '__main__':
    main()

