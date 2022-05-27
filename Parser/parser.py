import copy
from Lexer.lexer import Token


class Parser:
    def __init__(self, terminals, grammar_file, start_symbol):

        # store first and follow set for every non-terminal
        self.first_set = {}
        self.follow_set = {}

        # store LL(1) grammar
        self.grammar_file = grammar_file
        self.start_symbol = start_symbol
        self.rules_table = []

        # data structure ues to construct first set
        self.pre_first_dict = {}

        # data structure ues to construct follow set
        self.pre_follow_dict = {}

        # store the parsing table
        self.parsing_table = {}

        # store the terminals of the LL(1) grammar
        self.terminals = terminals

        # use to parse tokens
        self.tokens_queue = None
        self.symbol_stack = ['#']

        # initialize parser
        self.generate_rules_table()
        self.generate_pre_first_dict()
        self.generate_first_set()
        self.generate_pre_follow_dict()
        self.generate_follow_set()
        self.generate_parsing_table()

    # read grammar from file and store to list
    def generate_rules_table(self):

        # read grammar from file
        with open(self.grammar_file, "r") as f:
            for line in f:
                # If it is a blank line, skip it
                if line == '\n':
                    continue

                # split the line with blank space
                cur_line = line.split()

                # Special processing of 'GROUP BY' and 'ORDER BY'
                if 'GROUP' in cur_line:
                    cur_line[cur_line.index('GROUP')] = 'GROUP BY'
                    cur_line.remove('BY')

                if 'ORDER' in cur_line:
                    cur_line[cur_line.index('ORDER')] = 'ORDER BY'
                    cur_line.remove('BY')

                # store the grammar to rules_table, example:
                # querySpecification -> SELECT unionType selectElements selectClause
                # [querySpecification, SELECT, unionType, selectElements, selectClause]
                self.rules_table.append([cur_line[0], cur_line[2:]])

    # generate new data structure for construct first set
    def generate_pre_first_dict(self):
        # For each non-terminal save all generators of that
        # non-terminal at the left hand side of the grammar
        seq = 0
        for rule in self.rules_table:
            try:
                self.pre_first_dict[rule[0]].append(seq)
            except KeyError:
                self.pre_first_dict[rule[0]] = [seq]
            seq += 1

    # use to debug : print pre_first_dict
    def print_pre_first_dict(self):
        for line in self.pre_first_dict:
            print(line)
            for rule_num in self.pre_first_dict[line]:
                print(self.rules_table[rule_num][1])
            print()

    # construct first set for one terminal
    def first(self, non_terminal):

        # Consider all grammar with this non-terminal on the left-hand side
        for rule_num in self.pre_first_dict[non_terminal]:

            # if the right hand side of the grammar is started with terminal
            # add the terminal to the first set
            if self.rules_table[rule_num][1][0] in self.terminals:
                try:
                    self.first_set[non_terminal].append(self.rules_table[rule_num][1][0])
                except KeyError:
                    self.first_set[non_terminal] = copy.copy([self.rules_table[rule_num][1][0]])

            # if the grammar doesn't start with terminal
            else:
                for nt in self.rules_table[rule_num][1]:
                    # if the non-terminal is left-hand side non-terminal, skip it
                    if nt == non_terminal:
                        continue

                    # if there is a terminal at the right-hand side, add it to first
                    # set and return
                    if nt in self.terminals:
                        self.first_set[non_terminal].append(nt)
                        break

                    # If a non-terminal is encountered and the first-set of this
                    # non-terminal is not yet computed, then computed the first-set of
                    # this non-terminal first
                    if nt not in self.first_set:
                        self.first(nt)

                    # If a non-terminator is encountered and the first-set for that non-terminal has been calculated
                    # if ε not in the first-set(nt) or non-terminal at the end of the grammar
                    if '$' not in self.first_set[nt] or nt == self.rules_table[rule_num][1][-1]:
                        # just add all the terminal in the first-set(nt) to the first-set of non_terminal
                        try:
                            # False : don't delete ε
                            self.add_lists(self.first_set[non_terminal], self.first_set[nt], False)
                        except KeyError:
                            self.first_set[non_terminal] = copy.copy(self.first_set[nt])
                        break

                    # if ε in the first-set(nt) and non-terminal nt not at the end of the grammar
                    else:
                        # just add the terminal in the first-set(nt) to the first-set of non_terminal (except ε !)
                        try:
                            # False : don't delete ε
                            self.add_lists(self.first_set[non_terminal], self.first_set[nt], True)
                        except KeyError:
                            self.first_set[non_terminal] = copy.copy(self.first_set[nt])
                            self.first_set[non_terminal].remove('$')

        return

    # generate first set for every non-terminal
    def generate_first_set(self):
        # for every non-terminal call first
        for nt in self.pre_first_dict:
            if nt in self.first_set:
                continue
            else:
                self.first(nt)

    # use to debug : print rules table
    def print_rules_table(self):
        seq = 1
        for line in self.rules_table:
            print(f'{seq}\t{line[0]}\t{line[1]}')
            seq += 1

    @staticmethod
    def add_lists(list1, list2, option):
        # TRUE : delete $   False : don't delete $
        for item in list2:
            if item in list1 or (option and item == '$'):
                continue
            list1.append(item)

    # print first set
    def print_first_set(self):
        print('\n\n')
        print('+-------------------------------------------------------------------+')
        print('|---------------------------- First Set ----------------------------|')
        print('+-------------------------------------------------------------------+')
        for non_ter in self.first_set:
            print(f'{non_ter}=[', end='')
            for i in range(len(self.first_set[non_ter]) - 1):
                print(self.first_set[non_ter][i], end=', ')
            print(self.first_set[non_ter][-1], end='],\n')
        print('\n\n')

    # create new data structure for follow-set generation
    def generate_pre_follow_dict(self):
        # create new dictionary, key value is non-terminal
        for rule in self.rules_table:
            self.pre_follow_dict[rule[0]] = []

        # for each terminal store all the rule numbers that this terminal has
        # appeared on the right-hand side of the rule
        seq = 0
        for line in self.rules_table:
            for nt in line[1]:
                if nt in self.terminals:
                    continue
                self.pre_follow_dict[nt].append(seq)
            seq += 1

    # use to debug : print pre_follow_dict
    def print_pre_follow_dict(self):
        for line in self.pre_follow_dict:
            print(line)
            for rule_num in self.pre_follow_dict[line]:
                print(f'{rule_num}\t{self.rules_table[rule_num][0]} -> {self.rules_table[rule_num][1]}')
            print()

    def first_of_symbols(self, rhs_list):

        index = 0
        result = []

        # for every symbol in the right-hand side
        for s in rhs_list:
            # is s is terminal
            if s in self.terminals:
                self.add_lists(result, [s], False)
                break

            # if s is non-terminal and first-set(s) dose not contain ε
            elif '$' not in self.first_set[s]:
                self.add_lists(result, self.first_set[s], False)
                break

            # if s is non-terminal and it's not the last symbol
            elif index < len(rhs_list) - 1:
                self.add_lists(result, self.first_set[s], True)

            # if s is non-terminal and it is the last symbol
            else:
                self.add_lists(result, self.first_set[s], False)

            index += 1

        return result

    # generate follow set for all the non-terminals
    def generate_follow_set(self):

        temp = {}

        # create empty follow set for every terminal
        for rule in self.rules_table:
            self.follow_set[rule[0]] = []
            
        # start symbol doesn't appear at right-hand side of the grammar
        # so the follow-set of start-symbol is #
        self.follow_set[self.start_symbol].append('#')
        
        # for every non-terminal
        for symbol in self.pre_follow_dict:
            
            # for every rule that the current non-terminal appear at the right-hand side
            for seq_num in self.pre_follow_dict[symbol]:      
                
                start = self.rules_table[seq_num][1].index(symbol) + 1
                first_of_rhs = self.first_of_symbols(self.rules_table[seq_num][1][start:])
                
                # if the first of right-hand side does not contain ε and
                # first of right-hand side is empty (non-terminal does not at the end of the rule)
                if '$' not in first_of_rhs and len(first_of_rhs):
                    self.add_lists(self.follow_set[symbol], first_of_rhs, False)

                # if the first of right-hand side contain ε and
                # non-terminal is at the end of the rule
                else:
                    self.add_lists(self.follow_set[symbol], first_of_rhs, True)
                    # add symbol to temp
                    try:
                        temp[symbol].append(self.rules_table[seq_num][0])
                    except KeyError:
                        temp[symbol] = [self.rules_table[seq_num][0]]

        # need to be optimize!!!
        for symbol in temp:
            for nt in temp[symbol]:
                self.add_lists(self.follow_set[symbol], self.follow_set[nt], False)

        for symbol in temp:
            for nt in temp[symbol]:
                self.add_lists(self.follow_set[symbol], self.follow_set[nt], False)

    def print_follow_set(self):
        print('\n\n')
        print('+--------------------------------------------------------------------+')
        print('|---------------------------- Follow Set ----------------------------|')
        print('+--------------------------------------------------------------------+')
        for non_ter in self.follow_set:
            if len(self.follow_set[non_ter]) == 0:
                print(f'{non_ter}=[]')
                continue
            print(f'{non_ter}=[', end='')
            for i in range(len(self.follow_set[non_ter]) - 1):
                print(self.follow_set[non_ter][i], end=', ')
            print(self.follow_set[non_ter][-1], end='],\n')
        print('\n\n')

    def generate_parsing_table(self):

        seq_num = 0
        for rule in self.rules_table:
            for first_ter in self.first_of_symbols(rule[1]):
                if '$' == first_ter:
                    for follow_ter in self.follow_set[rule[0]]:
                        self.parsing_table[(rule[0], follow_ter)] = seq_num
                else:
                    self.parsing_table[(rule[0], first_ter)] = seq_num
            seq_num += 1

    def print_parsing_table(self):
        for key in self.parsing_table:
            rule = self.rules_table[self.parsing_table[key]]
            rhs = ''
            for symbol in rule[1]:
                rhs += symbol + ' '
            print(f'{key}\t{self.parsing_table[key]} {rule[0]} -> {rhs}')

    def parse_tokens(self, tokens, file_path):
        self.symbol_stack = ['#']
        self.tokens_queue = tokens
        self.tokens_queue.append(Token(None, None, None, '#', None))

        self.symbol_stack.append(self.start_symbol)
        seq_num = 1

        # store the output result
        text = ''

        while len(self.tokens_queue):
            if self.symbol_stack[-1] == self.tokens_queue[0].keyword:
                print(f'{seq_num}\t/\t{self.symbol_stack[-1]}#{self.tokens_queue[0].keyword}\tmove')
                text += f'{seq_num}\t/\t{self.symbol_stack[-1]}#{self.tokens_queue[0].keyword}\tmove\n'
                self.symbol_stack.pop()
                self.tokens_queue.pop(0)

            elif (self.symbol_stack[-1], self.tokens_queue[0].keyword) in self.parsing_table:
                rule_num = self.parsing_table[(self.symbol_stack[-1], self.tokens_queue[0].keyword)]
                if self.rules_table[rule_num][1] == ['$']:
                    print(f'{seq_num}\t{rule_num+1}\t{self.symbol_stack[-1]}#{self.tokens_queue[0].keyword}\treduction')
                    text += f'{seq_num}\t{rule_num+1}\t{self.symbol_stack[-1]}#{self.tokens_queue[0].keyword}\treduction\n'
                    self.symbol_stack.pop()
                else:
                    print(f'{seq_num}\t{rule_num+1}\t{self.symbol_stack[-1]}#{self.tokens_queue[0].keyword}\treduction')
                    text += f'{seq_num}\t{rule_num+1}\t{self.symbol_stack[-1]}#{self.tokens_queue[0].keyword}\treduction\n'
                    self.symbol_stack.pop()
                    for i in range(len(self.rules_table[rule_num][1]) - 1, -1, -1):
                        self.symbol_stack.append(self.rules_table[rule_num][1][i])
            else:
                print('Error!')
                return

            seq_num += 1

        print('Accept!')

        # write the result to file
        with open(file_path, 'w') as f:
            f.write(text)

    # use to debug : print parsing token queue
    def print_tokens_queue(self):
        print('token_queue :', end='\t')
        for tok in self.tokens_queue:
            print(tok.keyword, end=' ')
        print()

    # use to debug : print parsing symbol stack
    def print_symbol_stack(self):
        print('symbol_stack:', end='\t')
        for index in range(len(self.symbol_stack) - 1, -1, -1):
            print(self.symbol_stack[index], end=' ')
        print()
    
    # print first or follow set for non-terminal
    def print_first_or_follow(self, non_terminal, option):

        if option == 'follow':
            if non_terminal in self.follow_set:
                print(f'\nfollow( {non_terminal} )\t= {self.follow_set[non_terminal]}')
            else:
                print(f"Error : '{non_terminal}' is not an non-terminal")

        elif option == 'first':
            if non_terminal in self.first_set:
                print(f'\nfirst( {non_terminal} ) \t= {self.first_set[non_terminal]}')
            else:
                print(f"Error : '{non_terminal}' is not an non-terminal")

        else:
            print("Error : Option should be 'first' or 'follow'.")


Terminals = {'SELECT', 'FROM', 'WHERE', 'AS', '*',
             'INSERT', 'INTO', 'VALUES', 'VALUE', 'DEFAULT',
             'UPDATE', 'SET',
             'DELETE',
             'JOIN', 'LEFT', 'RIGHT', 'ON',
             'MIN', 'MAX', 'AVG', 'SUM',
             'UNION', 'ALL',
             'GROUP BY', 'HAVING', 'DISTINCT', 'ORDER BY',
             'TRUE', 'FALSE', 'UNKNOWN', 'IS', 'NULL',
             '=', '>', '<', '>=', '<=', '!=', '<=>',
             'AND', '&&', '||', 'OR', 'XOR', 'NOT', '!',
             '-',
             '.',
             '(', ')', ',',
             'IDN', 'INT', 'FLOAT', 'STRING', '$'}

