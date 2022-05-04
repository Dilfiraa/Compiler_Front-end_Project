class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_to_table(self, lexeme, category):
        self.table[lexeme] = category


class Token:
    def __init__(self, lexeme, category, seq, line, pos):
        self.lexeme = lexeme
        self.category = category
        self.seq = seq
        self.line = line
        self.pos = pos
        print(f'{self.lexeme}\t<{self.category},{self.seq}>')


symbol_table = SymbolTable()


class NFA:
    def __init__(self, start_state, accept_states, trans_function):
        self.start_state = start_state
        self.accept_states = accept_states
        self.trans_function = trans_function

    def closure(self, states):
        queue = []
        result = states
        for state in states:
            try:
                result.extend(self.trans_function[state]['$'])
                queue.extend(self.trans_function[state]['$'])
            except KeyError:
                continue

        while len(queue):
            state = queue[0]
            if state in result:
                queue.pop(0)
            else:
                try:
                    result.extend(self.trans_function[state]['$'])
                    queue.extend(self.trans_function[state]['$'])
                except KeyError:
                    queue.pop(0)

        return result

    def nfa2dfa(self):
        dfa_start_state = self.closure([self.start_state])
        # add the start state to queue
        queue = [tuple(dfa_start_state)]

        # add the start state to visited state set
        visited_states = set()
        visited_states.add(tuple(dfa_start_state))

        # create dict to store transfer function and accept states of DFA
        dfa_trans_func = {}
        dfa_accept_state = {}
        dfa_all_states = {}

        # execute till the queue is empty
        while len(queue):

            # get state from queue
            states = queue[0]
            # Store all terminals that can cause the nodes in the set to transfer
            terminal_set = set()

            # Find all terminals that can cause the nodes in the set to transfer
            for state in states:
                try:
                    for ter in self.trans_function[state]:
                        if ter == '$':
                            continue
                        terminal_set.add(ter)
                except KeyError:
                    continue

            # Save all transfer functions for a single node
            single_state_trans = {}

            # Constructing all transfer functions for a single node
            for ter in terminal_set:
                trans_state = []
                for state in states:
                    try:
                        trans_state.extend(self.trans_function[state][ter])
                    except KeyError:
                        continue
                trans_state = self.closure(trans_state)

                # add the single trans to dict
                single_state_trans[ter] = trans_state

                # chek if the state has been created before
                if tuple(trans_state) not in visited_states:
                    # add the new state to the queue and hash table
                    queue.append(tuple(trans_state))
                    visited_states.add(tuple(trans_state))

                    # check if the new state is accept state
                    for s in trans_state:
                        if s in self.accept_states:
                            dfa_accept_state[tuple(trans_state)] = self.accept_states[s]
                            if self.accept_states[s][0] != 'IDN':
                                break

            dfa_trans_func[tuple(states)] = single_state_trans
            queue.pop(0)

        return DFA(dfa_start_state, dfa_accept_state, dfa_trans_func)


class DFA:
    def __init__(self, start_state, accept_states, trans_function):

        self.start_state = start_state
        self.accept_states = accept_states

        self.trans_function = trans_function
        self.non_accept_states = self.get_non_accept_states()

        # use to run dfa
        self.cur_state = tuple(self.start_state)
        self.pre_state = None

    def get_non_accept_states(self):
        result = {}

        for s1 in self.trans_function:
            if s1 not in self.accept_states:
                result[tuple(s1)] = None
            for t in self.trans_function[s1]:
                if tuple(self.trans_function[s1][t]) not in self.accept_states:
                    result[tuple(self.trans_function[s1][t])] = None

        return result

    def print_non_accept_states(self):
        for s in self.non_accept_states:
            print(s)

    def print_trans_function(self):
        print("DFA transfer function")
        for state in self.trans_function:
            print(f'{state}\t{self.trans_function[state]}')
        print()

    def print_accept_states(self):
        print("DFA accept states")
        for state in self.accept_states:
            print(f'{state}\t{self.accept_states[state]}')
        print()

    def run_on_dfa(self, char):
        self.pre_state = self.cur_state
        try:
            self.cur_state = tuple(self.trans_function[self.cur_state][char])
        except KeyError:
            self.cur_state = tuple(self.start_state)
            return self.pre_state, None

        return self.pre_state, self.cur_state

    def dfa_minimization(self):
        pass


class Lexer:
    def __init__(self, dfa):
        self.dfa = dfa
        self.input_buffer = ''
        self.output_buffer = ''
        self.tokens = []

    def print_tokens(self):
        for token in self.tokens:
            print(f'{token.lexeme}\t<{token.category},{token.seq}>')

    def lexical_analysis(self, text):

        self.input_buffer = text
        line = 1
        pos = 1
        while self.input_buffer:
            print(f'input_buf:{self.input_buffer}')
            self.output_buffer = ''
            del_cur_char_num = 0
            pre_char = ''

            for cur_char in self.input_buffer:
                # print(f'line{line}:{cur_char}')
                # if cur_char == '\n':
                #     line += 1
                #     self.input_buffer = self.input_buffer[1:]
                #     break
                del_cur_char_num += 1
                pre_state, cur_state = dfa.run_on_dfa(cur_char)
                if cur_state is None:
                    break
                self.output_buffer += cur_char
                pre_char = cur_char


            # print(f'pre_char:{pre_char}.')

            if cur_state is None:

                if pre_state in self.dfa.accept_states:
                    if self.dfa.accept_states[pre_state][0] in ['IDN', 'STRING', 'INT', 'FLOAT']:
                        self.dfa.accept_states[pre_state].append(1)

                    if cur_char in [' ', '.', '*', '>', '<', '=', '&', '(', ')', ',', '|']:
                        self.input_buffer = self.input_buffer[del_cur_char_num - 1:]
                        self.tokens.append(Token(self.output_buffer, self.dfa.accept_states[pre_state][0],
                                                 self.dfa.accept_states[pre_state][1], line, pos))
                    elif pre_char in [' ', '.', '*', '>', '<', '=', '&', '(', ')', ',', '|']:
                        self.input_buffer = self.input_buffer[del_cur_char_num - 1:]
                        self.tokens.append(Token(self.output_buffer, self.dfa.accept_states[pre_state][0],
                                                 self.dfa.accept_states[pre_state][1], line, pos))
                    else:
                        print('Error1')
                        break
                elif pre_char == ' ':
                    self.input_buffer = self.input_buffer[del_cur_char_num - 1:]
                else:
                    print('Error2')
                    break

            elif cur_state in self.dfa.accept_states:
                if self.dfa.accept_states[cur_state][0] in ['IDN', 'STRING', 'INT', 'FLOAT']:
                    self.dfa.accept_states[cur_state].append(1)

                self.input_buffer = self.input_buffer[del_cur_char_num:]
                self.tokens.append(Token(self.output_buffer, self.dfa.accept_states[cur_state][0],
                                         self.dfa.accept_states[cur_state][1], line, pos))

            elif cur_state == self.dfa.start_state:
                self.input_buffer = self.input_buffer[del_cur_char_num:]

            else:
                print('Error3')
                break

        print(line)


import NFA_TRANS
import test

nfa = NFA(NFA_TRANS.nfa_start, NFA_TRANS.nfa_accept, NFA_TRANS.nfa_trans)
# nfa = NFA(0, test.acc,test.fun)
dfa = nfa.nfa2dfa()
dfa.print_accept_states()
dfa.print_trans_function()
dfa.print_non_accept_states()
lexer = Lexer(dfa)
# text = 'SELECT *\nFROM T07\nWHERE 0.0 T07.A != "BLA BLA"'
# text = text.replace('\n', ' ')
# # print(text)
# lexer.lexical_analysis(text)
print()
#
# for s in dfa.accept_states:
#     if dfa.accept_states[s][0] == 'INT':
#         print(f'{s}\t{dfa.accept_states[s]}')


