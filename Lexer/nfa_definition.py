nfa_start = 1

nfa_trans = {1: {'$': [2, 9, 14, 20, 23, 25, 32, 37, 44, 50, 58, 65, 69, 76, 81, 86, 92, 95, 99, 103, 107,
                       111, 117, 121, 130, 137, 146, 155, 160, 166, 174, 177, 182, 184, 185, 187, 188, 189, 191,
                       201, 205, 208, 211, 214, 218, 222, 224, 226, 228, 231, 235, 237, 240, 242, 244, 246]},

             2: {'S': [3]},
             3: {'E': [4]},
             4: {'L': [5]},
             5: {'E': [6]},
             6: {'C': [7]},
             7: {'T': [8]},

             9: {'F': [10]},
             10: {'R': [11]},
             11: {'O': [12]},
             12: {'M': [13]},

             14: {'W': [15]},
             15: {'H': [16]},
             16: {'E': [17]},
             17: {'R': [18]},
             18: {'E': [19]},

             20: {'A': [21]},
             21: {'S': [22]},

             23: {'*': [24]},

             25: {'I': [26]},
             26: {'N': [27]},
             27: {'S': [28]},
             28: {'E': [29]},
             29: {'R': [30]},
             30: {'T': [31]},

             32: {'I': [33]},
             33: {'N': [34]},
             34: {'T': [35]},
             35: {'O': [36]},

             37: {'V': [38]},
             38: {'A': [39]},
             39: {'L': [40]},
             40: {'U': [41]},
             41: {'E': [42]},
             42: {'S': [43]},

             44: {'V': [45]},
             45: {'A': [46]},
             46: {'L': [47]},
             47: {'U': [48]},
             48: {'E': [49]},

             50: {'D': [51]},
             51: {'E': [52]},
             52: {'F': [53]},
             53: {'A': [54]},
             54: {'U': [55]},
             55: {'L': [56]},
             56: {'T': [57]},

             58: {'U': [59]},
             59: {'P': [60]},
             60: {'D': [61]},
             61: {'A': [62]},
             62: {'T': [63]},
             63: {'E': [64]},

             65: {'S': [66]},
             66: {'E': [67]},
             67: {'T': [68]},

             69: {'D': [70]},
             70: {'E': [71]},
             71: {'L': [72]},
             72: {'E': [73]},
             73: {'T': [74]},
             74: {'E': [75]},

             76: {'J': [77]},
             77: {'O': [78]},
             78: {'I': [79]},
             79: {'N': [80]},

             81: {'L': [82]},
             82: {'E': [83]},
             83: {'F': [84]},
             84: {'T': [85]},

             86: {'R': [87]},
             87: {'I': [88]},
             88: {'G': [89]},
             89: {'H': [90]},
             90: {'T': [91]},

             92: {'O': [93]},
             93: {'N': [94]},

             95: {'M': [96]},
             96: {'I': [97]},
             97: {'N': [98]},

             99: {'M': [100]},
             100: {'A': [101]},
             101: {'X': [102]},

             103: {'A': [104]},
             104: {'V': [105]},
             105: {'G': [106]},

             107: {'S': [108]},
             108: {'U': [109]},
             109: {'M': [110]},

             111: {'U': [112]},
             112: {'N': [113]},
             113: {'I': [114]},
             114: {'O': [115]},
             115: {'N': [116]},

             117: {'A': [118]},
             118: {'L': [119]},
             119: {'L': [120]},

             121: {'G': [122]},
             122: {'R': [123]},
             123: {'O': [124]},
             124: {'U': [125]},
             125: {'P': [126]},
             126: {' ': [127]},
             127: {'B': [128]},
             128: {'Y': [129]},

             130: {'H': [131]},
             131: {'A': [132]},
             132: {'V': [133]},
             133: {'I': [134]},
             134: {'N': [135]},
             135: {'G': [136]},

             137: {'D': [138]},
             138: {'I': [139]},
             139: {'S': [140]},
             140: {'T': [141]},
             141: {'I': [142]},
             142: {'N': [143]},
             143: {'C': [144]},
             144: {'T': [145]},

             146: {'O': [147]},
             147: {'R': [148]},
             148: {'D': [149]},
             149: {'E': [150]},
             150: {'R': [151]},
             151: {' ': [152]},
             152: {'B': [153]},
             153: {'Y': [154]},

             155: {'T': [156]},
             156: {'R': [157]},
             157: {'U': [158]},
             158: {'E': [159]},
             160: {'F': [161]},
             161: {'A': [162]},
             162: {'L': [163]},
             163: {'S': [164]},
             164: {'E': [165]},

             166: {'U': [167]},
             167: {'N': [168]},
             168: {'K': [169]},
             169: {'N': [170]},
             170: {'O': [171]},
             171: {'W': [172]},
             172: {'N': [173]},

             174: {'I': [175]},
             175: {'S': [176]},
             177: {'N': [178]},
             178: {'U': [179]},
             179: {'L': [180]},
             180: {'L': [181]},

             182: {'=': [183]},
             184: {'>': [185]},
             185: {'=': [186]},
             187: {'<': [188]},
             188: {'=': [189]},
             189: {'>': [190]},
             191: {'!': [192]},
             192: {'=': [193]},


             201: {'A': [202]},
             202: {'N': [203]},
             203: {'D': [204]},

             205: {'&': [206]},
             206: {'&': [207]},

             208: {'O': [209]},
             209: {'R': [210]},

             211: {'|': [212]},
             212: {'|': [213]},

             214: {'X': [215]},
             215: {'O': [216]},
             216: {'R': [217]},

             218: {'N': [219]},
             219: {'O': [220]},
             220: {'T': [221]},

             222: {'!': [223]},
             224: {'-': [225]},
             226: {'.': [227]},

             228: {'0': [230], '1': [229], '2': [229], '3': [229], '4': [229], '5': [229], '6': [229], '7': [229],
                   '8': [229], '9': [229]},
             229: {'0': [229], '1': [229], '2': [229], '3': [229], '4': [229], '5': [229], '6': [229], '7': [229],
                   '8': [229], '9': [229]},

             231: {'0': [232], '1': [232], '2': [232], '3': [232], '4': [232], '5': [232], '6': [232], '7': [232],
                   '8': [232], '9': [232]},
             232: {'0': [232], '1': [232], '2': [232], '3': [232], '4': [232], '5': [232], '6': [232], '7': [232],
                   '8': [232], '9': [232], '.': [233]},
             233: {'0': [234], '1': [234], '2': [234], '3': [234], '4': [234], '5': [234], '6': [234], '7': [234],
                   '8': [234], '9': [234]},
             234: {'0': [234], '1': [234], '2': [234], '3': [234], '4': [234], '5': [234], '6': [234], '7': [234],
                   '8': [234], '9': [234]},


             235: {'_': [236], 'A': [236], 'B': [236], 'C': [236], 'D': [236], 'E': [236], 'F': [236], 'G': [236],
                   'H': [236], 'I': [236],
                   'J': [236], 'K': [236], 'L': [236], 'M': [236], 'N': [236], 'O': [236], 'P': [236], 'Q': [236],
                   'R': [236], 'S': [236],
                   'T': [236], 'U': [236], 'V': [236], 'W': [236], 'X': [236], 'Y': [236], 'Z': [236],
                   'a': [236], 'b': [236], 'c': [236], 'd': [236], 'e': [236], 'f': [236], 'g': [236], 'h': [236],
                   'i': [236], 'j': [236],
                   'k': [236], 'l': [236], 'm': [236], 'n': [236], 'o': [236], 'p': [236], 'q': [236], 'r': [236],
                   's': [236], 't': [236],
                   'u': [236], 'v': [236], 'w': [236], 'x': [236], 'y': [236], 'z': [236]},

             236: {'_': [236], 'A': [236], 'B': [236], 'C': [236], 'D': [236], 'E': [236], 'F': [236], 'G': [236],
                   'H': [236], 'I': [236],
                   'J': [236], 'K': [236], 'L': [236], 'M': [236], 'N': [236], 'O': [236], 'P': [236], 'Q': [236],
                   'R': [236], 'S': [236],
                   'T': [236], 'U': [236], 'V': [236], 'W': [236], 'X': [236], 'Y': [236], 'Z': [236],
                   'a': [236], 'b': [236], 'c': [236], 'd': [236], 'e': [236], 'f': [236], 'g': [236], 'h': [236],
                   'i': [236], 'j': [236],
                   'k': [236], 'l': [236], 'm': [236], 'n': [236], 'o': [236], 'p': [236], 'q': [236], 'r': [236],
                   's': [236], 't': [236],
                   'u': [236], 'v': [236], 'w': [236], 'x': [236], 'y': [236], 'z': [236],
                   '0': [236], '1': [236], '2': [236], '3': [236], '4': [236], '5': [236], '6': [236], '7': [236],
                   '8': [236], '9': [236]},

             237: {'"': [238]},

             238: {'"': [239], '_': [238], '=': [238], '<': [238], '>': [238], '!': [238], '.': [238], '*': [238],
                   '&': [238], '(': [238], ')': [238], '|': [238], ',': [238], ' ': [238], '#': [238], '@': [238],
                   '-': [238], '~': [238], '`': [238], '%': [238], '^': [238], '{': [238], '}': [238], '\\': [238],
                   '[': [238], ']': [238], '?': [238], '/': [238], '+': [238], ';': [238], ':': [238],
                   '0': [238], '1': [238], '2': [238], '3': [238], '4': [238], '5': [238], '6': [238], '7': [238],
                   '8': [238], '9': [238],
                   'A': [238], 'B': [238], 'C': [238], 'D': [238], 'E': [238], 'F': [238], 'G': [238], 'H': [238],
                   'I': [238], 'J': [238], 'K': [238], 'L': [238], 'M': [238], 'N': [238], 'O': [238], 'P': [238],
                   'Q': [238], 'R': [238], 'S': [238], 'T': [238], 'U': [238], 'V': [238], 'W': [238], 'X': [238],
                   'Y': [238], 'Z': [238],
                   'a': [238], 'b': [238], 'c': [238], 'd': [238], 'e': [238], 'f': [238], 'g': [238], 'h': [238],
                   'i': [238], 'j': [238], 'k': [238], 'l': [238], 'm': [238], 'n': [238], 'o': [238], 'p': [238],
                   'q': [238], 'r': [238], 's': [238], 't': [238], 'u': [238], 'v': [238], 'w': [238], 'x': [238],
                   'y': [238], 'z': [238]},

             240: {'(': [241]},
             242: {')': [243]},
             244: {',': [245]},
             246: {' ': [246]},
             }

nfa_accept = {8:   ['KW', 1],
              13:  ['KW', 2],
              19:  ['KW', 3],
              22:  ['KW', 4],
              24:  ['KW', 5],
              31:  ['KW', 6],
              36:  ['KW', 7],
              43:  ['KW', 8],
              49:  ['KW', 9],
              57:  ['KW', 10],
              64:  ['KW', 11],
              68:  ['KW', 12],
              75:  ['KW', 13],
              80:  ['KW', 14],
              85:  ['KW', 15],
              91:  ['KW', 16],
              94:  ['KW', 17],
              98:  ['KW', 18],
              102: ['KW', 19],
              106: ['KW', 20],
              110: ['KW', 21],
              116: ['KW', 22],
              120: ['KW', 23],
              129: ['KW', 24],
              136: ['KW', 25],
              145: ['KW', 26],
              154: ['KW', 27],
              159: ['KW', 28],
              165: ['KW', 29],
              173: ['KW', 30],
              176: ['KW', 31],
              181: ['KW', 32],
              183: ['OP', 1],
              185: ['OP', 2],
              186: ['OP', 4],
              188: ['OP', 3],
              189: ['OP', 5],
              190: ['OP', 7],
              193: ['OP', 6],
              204: ['OP', 8],
              207: ['OP', 9],
              210: ['OP', 10],
              213: ['OP', 11],
              217: ['OP', 12],
              221: ['OP', 13],
              223: ['OP', 14],
              225: ['OP', 15],
              227: ['OP', 16],
              229: ['INT'],
              230: ['INT'],
              234: ['FLOAT'],
              236: ['IDN'],
              239: ['STRING'],
              241: ['SE', 1],
              243: ['SE', 2],
              245: ['SE', 3]
              }
