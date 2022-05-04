import copy


class Token:
    def __init__(self, name):
        self.name = name


class Parser:
    def __init__(self, terminals, grammar_file, start_symbol, tokens):
        self.first_set = {}
        self.follow_set = {}

        self.rules_table = []
        self.pre_first_dict = {}
        self.pre_follow_dict = {}

        self.parsing_table = {}

        self.terminals = terminals

        self.tokens_queue = tokens
        self.symbol_stack = ['#']

        self.grammar_file = grammar_file
        self.start_symbol = start_symbol

    def generate_rules_table(self):

        with open(self.grammar_file, "r") as f:
            for line in f:
                if line == '\n':
                    continue

                cur_line = line.split()

                if 'GROUP' in cur_line:
                    cur_line[cur_line.index('GROUP')] = 'GROUP BY'
                    cur_line.remove('BY')

                if 'ORDER' in cur_line:
                    cur_line[cur_line.index('ORDER')] = 'ORDER BY'
                    cur_line.remove('BY')

                self.rules_table.append([cur_line[0], cur_line[2:]])

    def generate_pre_first_dict(self):
        seq = 0
        for rule in self.rules_table:
            if rule[0] in self.pre_first_dict:
                self.pre_first_dict[rule[0]].append(seq)
            else:
                self.pre_first_dict[rule[0]] = [seq]
            seq += 1

    def print_pre_first_dict(self):
        # for line in self.pre_first_dict:
        #     print(f'{line}  {self.pre_first_dict[line]}')
        for line in self.pre_first_dict:
            print(line)
            for rule_num in self.pre_first_dict[line]:
                print(self.rules_table[rule_num][1])
            print()

    def first(self, lhs):

        for rule_num in self.pre_first_dict[lhs]:
            if self.rules_table[rule_num][1][0] in self.terminals:
                if lhs not in self.first_set:
                    self.first_set[lhs] = copy.copy([self.rules_table[rule_num][1][0]])
                else:
                    self.first_set[lhs].append(self.rules_table[rule_num][1][0])

            else:
                for nt in self.rules_table[rule_num][1]:
                    if nt == lhs:
                        continue

                    if nt in self.terminals:
                        self.first_set[lhs].append(nt)
                        break

                    if nt not in self.first_set:
                        self.first(nt)

                    if '$' not in self.first_set[nt] or self.rules_table[rule_num][1].index(nt) == len(
                            self.rules_table[rule_num][1]) - 1:
                        if lhs not in self.first_set:
                            self.first_set[lhs] = copy.copy(self.first_set[nt])
                        else:
                            self.add_lists(self.first_set[lhs], self.first_set[nt], False)
                        break
                    else:
                        if lhs not in self.first_set:
                            self.first_set[lhs] = copy.copy(self.first_set[nt])
                            self.first_set[lhs].remove('$')
                        else:
                            self.add_lists(self.first_set[lhs], self.first_set[nt], True)

    def generate_first_set(self):
        for lhs in self.pre_first_dict:
            if lhs in self.first_set:
                continue
            else:
                self.first(lhs)

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

    def generate_pre_follow_dict(self):
        for rule in self.rules_table:
            self.pre_follow_dict[rule[0]] = []

        seq = 0
        for line in self.rules_table:
            for rule in line[1]:
                if rule in self.terminals:
                    continue
                self.pre_follow_dict[rule].append(seq)
            seq += 1

    def print_pre_follow_dict(self):
        for line in self.pre_follow_dict:
            print(line)
            for rule_num in self.pre_follow_dict[line]:
                print(f'{self.rules_table[rule_num][0]} -> {self.rules_table[rule_num][1]}')
            print()


    def first_of_rhs(self, rhs_list):

        index = 0
        result = []
        for v in rhs_list:
            if v in self.terminals:
                self.add_lists(result, [v], False)
                break
            elif '$' not in self.first_set[v]:
                self.add_lists(result, self.first_set[v], False)
                break
            elif index < len(rhs_list) - 1:
                self.add_lists(result, self.first_set[v], True)
            else:
                self.add_lists(result, self.first_set[v], False)
            index += 1

        return result

    def generate_follow_set(self):

        temp = {}
        self.symbol_stack.append(self.start_symbol)

        for rule in self.rules_table:
            self.follow_set[rule[0]] = []
        self.follow_set[self.start_symbol].append('#')

        for lhs in self.pre_follow_dict:
            for seq_num in self.pre_follow_dict[lhs]:
                start = self.rules_table[seq_num][1].index(lhs) + 1
                first_of_r = self.first_of_rhs(self.rules_table[seq_num][1][start:])
                # print(self.rules_table[seq_num][1][start:], '   ', first_of_r)
                if '$' not in first_of_r and len(first_of_r):
                    self.add_lists(self.follow_set[lhs], first_of_r, False)
                else:
                    self.add_lists(self.follow_set[lhs], first_of_r, True)
                    if lhs in temp:
                        temp[lhs].append(self.rules_table[seq_num][0])
                    else:
                        temp[lhs] = [self.rules_table[seq_num][0]]

        # need to be optimize!!!
        for item in temp:
            for nt in temp[item]:
                self.add_lists(self.follow_set[item], self.follow_set[nt], False)

        for item in temp:
            for nt in temp[item]:
                self.add_lists(self.follow_set[item], self.follow_set[nt], False)

    def print_follow_set(self):
        print('\n\n')
        print('+--------------------------------------------------------------------+')
        print('|---------------------------- Follow Set ----------------------------|')
        print('+--------------------------------------------------------------------+')
        for non_ter in self.follow_set:
            print(f'{non_ter}=[', end='')
            for i in range(len(self.follow_set[non_ter]) - 1):
                print(self.follow_set[non_ter][i], end=', ')
            print(self.follow_set[non_ter][-1], end='],\n')
        print('\n\n')

    def generate_parsing_table(self):

        seq_num = 0
        for rule in self.rules_table:
            for first_ter in self.first_of_rhs(rule[1]):
                if '$' == first_ter:
                    for follow_ter in self.follow_set[rule[0]]:
                        self.parsing_table[(rule[0], follow_ter)] = seq_num
                else:
                    self.parsing_table[(rule[0], first_ter)] = seq_num
            seq_num += 1


    def parse_tokens(self):
        seq_num = 1
        self.tokens_queue.append(Token('#'))

        while len(self.tokens_queue):
            if self.symbol_stack[-1] == self.tokens_queue[0].name:
                print(f'{seq_num}\t/\t{self.symbol_stack[-1]}#{self.tokens_queue[0].name}\tmove')
                self.symbol_stack.pop()
                self.tokens_queue.pop(0)
            elif (self.symbol_stack[-1], self.tokens_queue[0].name) in self.parsing_table:
                rule_num = self.parsing_table[(self.symbol_stack[-1], self.tokens_queue[0].name)]
                if self.rules_table[rule_num][1] == ['$']:
                    print(f'{seq_num}\t{rule_num+1}\t{self.symbol_stack[-1]}#{self.tokens_queue[0].name}\treduction')
                    self.symbol_stack.pop()
                else:
                    print(f'{seq_num}\t{rule_num+1}\t{self.symbol_stack[-1]}#{self.tokens_queue[0].name}\treduction')
                    self.symbol_stack.pop()
                    for i in range(len(self.rules_table[rule_num][1]) - 1, -1, -1):
                        self.symbol_stack.append(self.rules_table[rule_num][1][i])
            else:
                print('Error!')
                return

            seq_num += 1

        print('accept!')

    def print_tokens_queue(self):
        print('token_queue :', end='\t')
        for tok in self.tokens_queue:
            print(tok.name, end=' ')
        print()

    def print_symbol_stack(self):
        print('symbol_stack:', end='\t')
        for index in range(len(self.symbol_stack) - 1, -1, -1):
            print(self.symbol_stack[index], end=' ')
        print()

    def print_first_or_follow(self, Non_Terminal, option):

        if option == 'follow':
            if Non_Terminal in self.follow_set:
                print(f'\nfollow( {Non_Terminal} )\t= {self.follow_set[Non_Terminal]}')
            else:
                print(f"Error : '{Non_Terminal}' is not an non-terminal")

        elif option == 'first':
            if Non_Terminal in self.first_set:
                print(f'\nfirst( {Non_Terminal} ) \t= {self.first_set[Non_Terminal]}')
            else:
                print(f"Error : '{Non_Terminal}' is not an non-terminal")

        else:
            print("Error : Option should be 'first' or 'follow'.")




