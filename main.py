from Lexer import nfa_definition
from Lexer.lexer import *
from Parser.parser import Parser, Terminals


def main():

    # lexer
    text = 'SELECT * 07M.11 FROM T07 WHERE T07.A != "BLA BLA" '
    text = 'SELECT from_._1_,SUM(from_._2_) FROM from_ JOIN _1A ON from_._1_=_1A.cr7 WHERE from_._2_>1 AND from_._3_' \
           '<3.1415926 OR 1.25 IS NOT NULL GROUP BY from_._2_ HAVING from_._3_="ORDER BY #><=="'

    # lexical analysis
    nfa = NFA(nfa_definition.nfa_start, nfa_definition.nfa_accept, nfa_definition.nfa_trans)
    dfa = nfa.nfa2dfa()
    minimized_dfa = dfa.dfa_minimization()
    lexer = Lexer(minimized_dfa)
    lexer.lexical_analysis(text)


    # parsing
    start_symbol = 'root'
    grammar_file = 'Parser\grammar.txt'
    parser = Parser(terminals=Terminals, grammar_file=grammar_file, start_symbol=start_symbol)


    print('\n\n')
    lexer.print_tokens_keyword()
    parser.parse_tokens(lexer.tokens)

    # while True:
    #     text = input('sql > ')
    #
    #     lexer.lexical_analysis(text)
    #
    #     print('\n\n')
    #     lexer.print_tokens_keyword()
    #     parser.parse_tokens(lexer.tokens)


if __name__ == '__main__':
    main()
