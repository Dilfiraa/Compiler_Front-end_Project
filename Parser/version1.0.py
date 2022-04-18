import copy


class RHS:
    def __init__(self, rule, id):
        self.rule = rule
        self.id = id


def grammar_to_dict(file_name):
    rules = {}
    seq = 1

    with open(file_name, "r") as f:
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

            rhs = RHS(cur_line[2:], seq)

            if cur_line[0] not in rules:
                rules[cur_line[0]] = [rhs]
            else:
                rules[cur_line[0]].append(rhs)

            seq += 1

    return rules


TERMINAL = {'a', 'b', 'c', 'd', 'g', 'h', '$'}
TERMINAL = {'SELECT', 'FROM', 'WHERE', 'AS', '*',
            'INSERT', 'INTO', 'VALUES', 'VALUE', 'DEFAULT',
            'UPDATE', 'SET',
            'DELETE',
            'JOIN', 'LEFT', 'RIGHT', 'ON',
            'MIN', 'MIN', 'MAX', 'AVG', 'SUM',
            'UNION', 'ALL',
            'GROUP BY', 'HAVING', 'DISTINCT', 'ORDER BY',
            'TRUE', 'FALSE', 'UNKNOWN', 'IS', 'NULL',
            '=', '>', '<', '>=', '<=', '!=', '<=>',
            'AND', '&&', '||', 'OR', 'XOR', 'NOT', '!',
            '-',
            '.',
            '(', ')', ',',
            'IDN', 'INT', 'FLOAT', 'STRING', '$'}
# TERMINAL = {'*', '+', '(', ')', 'i', '$'}


class Parser:
    def __init__(self, rules):
        self.rules = rules
        self.first_set = {}
        self.follow_set = {}

    def first(self, lhs):

        for rhs in self.rules[lhs]:

            if rhs.rule[0] in TERMINAL:
                if lhs not in self.first_set:
                    self.first_set[lhs] = copy.copy([rhs.rule[0]])
                else:
                    self.first_set[lhs].append(rhs.rule[0])

            else:
                for nt in rhs.rule:
                    if nt == lhs:
                        continue

                    if nt in TERMINAL:
                        self.first_set[lhs].append(nt)
                        break

                    if nt not in self.first_set:
                        self.first(nt)

                    if '$' not in self.first_set[nt] or rhs.rule.index(nt) == len(rhs.rule) - 1:
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
        for lhs in self.rules:

            if lhs in self.first_set:
                continue
            else:
                self.first(lhs)

    def print_rules(self):
        for item in self.rules:
            print(item)
            for i in self.rules[item]:
                print(f'{i.id}  {i.rule}')
            print()

    @staticmethod
    def add_lists(list1, list2, option):
        # TRUE : delete $   False : don't delete $
        for item in list2:
            if item in list1 or (option and item == '$'):
                continue
            list1.append(item)

    def print_first_set(self):
        for lhs in self.first_set:
            print(f'{lhs}={self.first_set[lhs]},')

    def generate_follow_set(self):
        pass


parser = Parser(grammar_to_dict('grammar.txt'))
parser.print_rules()
parser.generate_first_set()
parser.print_first_set()

lhs = 'expression'
print(f'\n{lhs} = {parser.first_set[lhs]}')



