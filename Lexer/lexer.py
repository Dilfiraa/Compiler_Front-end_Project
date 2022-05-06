class Token:
    def __init__(self, lexeme, category, seq, keyword, pos):
        self.lexeme = lexeme
        self.category = category
        self.seq = seq
        self.keyword = keyword
        self.pos = pos

        if self.lexeme is not None:
            print("%-10s<%s,%s>" % (self.lexeme, self.category, self.seq))


class NFA:
    def __init__(self, start_state, accept_states, trans_function):
        self.start_state = start_state
        self.accept_states = accept_states
        self.trans_function = trans_function
        self.non_accept_states = self.get_non_accept_states()

    def get_non_accept_states(self):
        result = {}

        for s1 in self.trans_function:
            if s1 not in self.accept_states:
                result[s1] = None
            for t in self.trans_function[s1]:
                for s2 in self.trans_function[s1][t]:
                    if s2 not in self.accept_states:
                        result[s2] = None
        return result

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

        # use to run dfa
        self.cur_state = tuple(self.start_state)
        self.pre_state = None

        # use to minimize dfa
        self.non_accept_states = self.get_non_accept_states()
        self.state_sets = None
        self.sets_max_sqe = {'NON': 0, 'IDN': 0, 'INT': 0}

        self.state_num = len(self.accept_states) + len(self.non_accept_states)

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
        print()

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

    def print_state_sets(self):
        for state_name in self.state_sets:
            print(state_name, end='\t')
            for s in self.state_sets[state_name]:
                print(s, end=' ')
            print()
        print()

    def run_on_dfa(self, char):
        self.pre_state = self.cur_state
        try:
            self.cur_state = tuple(self.trans_function[self.cur_state][char])
        except KeyError:
            self.cur_state = tuple(self.start_state)
            return self.pre_state, None

        return self.pre_state, self.cur_state

    def sets(self, category):
        states_set = {}

        for state in self.accept_states:
            if self.accept_states[state][0] == category:
                states_set[state] = None

        return states_set

    def split_set(self, set_key):

        # 根据到达的结点分为集合名称
        for state in self.state_sets[set_key]:

            for set_name in self.state_sets:
                if self.state_sets[set_key][state] in self.state_sets[set_name]:
                    self.state_sets[set_key][state] = set_name
                    break

                elif self.state_sets[set_key][state] in self.accept_states:
                    if self.accept_states[self.state_sets[set_key][state]][0] not in ['IDN', 'INT']:
                        self.state_sets[set_key][state] = tuple(self.accept_states[self.state_sets[set_key][state]])

        # 根据集合名称 进行分类 生成新的集合
        new_set = {}
        for state in self.state_sets[set_key]:
            if self.state_sets[set_key][state] not in new_set:
                new_set[self.state_sets[set_key][state]] = {state: None}
            else:
                new_set[self.state_sets[set_key][state]][state] = None

        if len(new_set) > 1:
            del self.state_sets[set_key]
            for new_state in new_set:
                self.sets_max_sqe[set_key[0]] += 1
                self.state_sets[(set_key[0], self.sets_max_sqe[set_key[0]])] = new_set[new_state]
            return True

        return False

    def dfa_minimization(self):

        # IDN states dict
        idn_set = self.sets('IDN')

        # INT states dict
        int_set = self.sets('INT')

        # Initial division of the state set
        self.state_sets = {('INT', self.sets_max_sqe['INT']): int_set,
                           ('NON', self.sets_max_sqe['NON']): self.non_accept_states,
                           ('IDN', self.sets_max_sqe['IDN']): idn_set}

        # store the previous set number and current set number
        pre_state_sets_num = 0
        cur_state_sets_num = len(self.state_sets)

        # Operate on each set until the set is no longer split
        while cur_state_sets_num != pre_state_sets_num:

            have_split = False

            # Operate on each set
            for set_key in self.state_sets:

                # If the set contains only one state skip the set
                if len(self.state_sets[set_key]) == 1:
                    continue

                # Save non-terminals that all nodes of the set can read in
                terminal_set = []
                for state in self.state_sets[set_key]:
                    for ter in self.trans_function[state]:
                        if ter not in terminal_set:
                            terminal_set.append(ter)

                # For each node in the set record the node reached after reading in the non-terminal
                for ter in terminal_set:
                    for state in self.state_sets[set_key]:
                        try:
                            self.state_sets[set_key][state] = tuple(self.trans_function[state][ter])
                        except KeyError:
                            continue

                    # split the current set
                    have_split = self.split_set(set_key)

                    # If the set is split, start over from the beginning
                    if have_split:
                        break

                # If the set is split, start over from the beginning
                if have_split:
                    break

            # calculate the new pre_state_sets_num and cur_state_sets_num
            pre_state_sets_num = cur_state_sets_num
            cur_state_sets_num = len(self.state_sets)

        # Add the rest of the accepting state that contain only one state to the state_sets
        for state in self.accept_states:
            if self.accept_states[state][0] not in ['IDN', 'INT']:
                self.state_sets[tuple(self.accept_states[state])] = {state: None}

        # Generate minimized DFA based on self.state_sets
        return self.generate_minimize_dfa()

    def generate_minimize_dfa(self):

        # Preserve the mapping relationship of states between the original DFA and the minimized DFA
        state_mapping = {}
        for state_name in self.state_sets:
            for state in self.state_sets[state_name]:
                state_mapping[state] = state_name

        # The start state of minimized-DFA
        start_state = state_mapping[tuple(self.start_state)]

        # The accept state of minimized-DFA
        accept_states = {}
        for state in self.accept_states:
            accept_states[state_mapping[state]] = self.accept_states[state]

        # The transfer function of minimized-DFA
        trans_function = {}
        for state in self.trans_function:
            trans_function[state_mapping[state]] = {}
            for ter in self.trans_function[state]:
                trans_function[state_mapping[state]][ter] = state_mapping[tuple(self.trans_function[state][ter])]

        # Return minimized-DFA
        return DFA(start_state, accept_states, trans_function)


class Lexer:
    def __init__(self, dfa):
        self.dfa = dfa
        self.input_buffer = ''
        self.output_buffer = ''
        self.tokens = []

    def print_tokens(self):
        for token in self.tokens:
            print(f'{token.lexeme}\t<{token.category},{token.seq}>')

    def get_token_keyword(self, key, seq):

        keyword_table = {'KW': [None, 'SELECT', 'FROM', 'WHERE', 'AS', '*', 'INSERT', 'INTO', 'VALUES', 'VALUE',
                                'DEFAULT', 'UPDATE', 'SET', 'DELETE', 'JOIN', 'LEFT', 'RIGHT', 'ON',
                                'MIN', 'MAX', 'AVG', 'SUM', 'UNION', 'ALL', 'GROUP BY', 'HAVING', 'DISTINCT',
                                'ORDER BY', 'TRUE', 'FALSE', 'UNKNOWN', 'IS', 'NULL'],
                         'OP': [None, '=', '>', '<', '>=', '<=', '!=', '<=>', 'AND', '&&', '||', 'OR', 'XOR', 'NOT',
                                '!', '-', '.'],
                         'SE': [None, '(', ')', ',']}

        if key in keyword_table:
            return keyword_table[key][seq]
        else:
            return key

    def lexical_analysis(self, text):

        self.input_buffer = text
        sql_text = text
        pos = 1

        while self.input_buffer:
            self.output_buffer = ''
            del_cur_char_num = 0
            pre_char = ''

            for cur_char in self.input_buffer:
                pos += 1
                del_cur_char_num += 1
                pre_state, cur_state = self.dfa.run_on_dfa(cur_char)
                if cur_state is None:
                    break
                self.output_buffer += cur_char
                pre_char = cur_char

            if cur_state is None:

                if pre_state in self.dfa.accept_states:
                    if self.dfa.accept_states[pre_state][0] in ['IDN', 'STRING', 'INT', 'FLOAT']:
                        try:
                            self.dfa.accept_states[pre_state][1] = self.output_buffer
                        except IndexError:
                            self.dfa.accept_states[pre_state].append(self.output_buffer)

                    boundary_ter = [' ', '.', '*', '>', '<', '=', '&', '(', ')', ',', '|']
                    if cur_char in boundary_ter or pre_char in boundary_ter:
                        self.input_buffer = self.input_buffer[del_cur_char_num - 1:]
                        pos -= 1
                        self.tokens.append(Token(self.output_buffer, self.dfa.accept_states[pre_state][0],
                                                 self.dfa.accept_states[pre_state][1],
                                                 self.get_token_keyword(self.dfa.accept_states[pre_state][0],
                                                                        self.dfa.accept_states[pre_state][1]),
                                                 pos-len(self.output_buffer)))

                    else:
                        print('Error!')
                        return

                elif pre_char == ' ':
                    pos -= 1
                    self.input_buffer = self.input_buffer[del_cur_char_num - 1:]

                else:
                    print(sql_text)
                    print(' ' * (pos-len(self.output_buffer)-2) + '^')
                    print('Error: invalid syntax!')
                    return

            elif cur_state in self.dfa.accept_states:
                if self.dfa.accept_states[cur_state][0] in ['IDN', 'STRING', 'INT', 'FLOAT']:
                    try:
                        self.dfa.accept_states[cur_state][1] = self.output_buffer
                    except IndexError:
                        self.dfa.accept_states[cur_state].append(self.output_buffer)

                self.input_buffer = self.input_buffer[del_cur_char_num:]
                self.tokens.append(Token(self.output_buffer, self.dfa.accept_states[cur_state][0],
                                         self.dfa.accept_states[cur_state][1],
                                         self.get_token_keyword(self.dfa.accept_states[cur_state][0],
                                                                self.dfa.accept_states[cur_state][1]),
                                         pos-len(self.output_buffer)))

            elif cur_state == self.dfa.start_state:
                self.input_buffer = self.input_buffer[del_cur_char_num:]

            else:
                print('Error!')
                return

        with open('Test/Output/49lex.tsv', 'w') as f:
            text = ''
            for token in self.tokens:
                text += "%-10s<%s,%s>\n" % (token.lexeme, token.category, token.seq)
            f.write(text)

    def print_tokens_keyword(self):
        for token in self.tokens:
            print(token.keyword, end=' ')
        print()

