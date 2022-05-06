from lexer import *
import nfa_definition

nfa = NFA(nfa_definition.nfa_start, nfa_definition.nfa_accept, nfa_definition.nfa_trans)
dfa = nfa.nfa2dfa()
# lexer = Lexer(dfa)
mini_dfa = dfa.dfa_minimization()
lexer = Lexer(dfa)
text = 'SELECT * \nFROM T07 \nWHERE 0.0 T07.A != "BLA BLA"'
text = text.replace('\n', ' ')
lexer.lexical_analysis(text)


fun = {1: {'a': [4, 5], '$': [2]},
       2: {'a': [3]},
       3: {'$': [8]},
       4: {'$': [7]},
       5: {'$': [6]},
       6: {'$': [2]}
       }

fun = {0: {'a': [0], '$': [1, 2]},
       1: {'b': [1, 3]},
       2: {'c': [2], '$': [3]},
       }

fun = {0: {'a': [0, 1], 'b': [0]},
       1: {'b': [2]},
       2: {'b': [3]},
       }

fun = {0: {'$': [1, 7]},
       1: {'$': [2, 4]},
       2: {'a': [3]},
       3: {'$': [6]},
       4: {'b': [5]},
       5: {'$': [6]},
       6: {'$': [1, 7]},
       7: {'a': [8]},
       8: {'b': [9]},
       9: {'b': [10]},
       }


fun = {0: {'$': [1, 3, 7, 9]},
       1: {'a': [2]},
       3: {'a': [4]},
       4: {'b': [5]},
       5: {'b': [6]},
       7: {'a': [7], 'b': [8]},
       8: {'b': [8]},
       9: {' ': [9]}
       }

acc = {2: ['KW', 1],
       6: ['KW', 2],
       8: ['IDN'],
       }



