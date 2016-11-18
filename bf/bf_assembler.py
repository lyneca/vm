
def bfa_token(line):
    space = 0
    while line[space].isspace():
        space += 1
    op, *args = line.split()
    return space, op, args

def bfa_tokens(lines):
    if type(lines) is str:
        lines = lines.splitlines()
    return [bfa_token(line) for line in lines]


def bfa_indented_tokens(tokens):
    ret_stack = [([],tokens[0][0])]
    for space, op, args in tokens:
        if ret_stack[-1][1] < space:
            ret_stack.append(([(op, args)], space))
        elif prev_space == space:
            ret_stack[-1][0].append((op, args))
        #else: 
        while ret_stack[-1][1] > space:
            ret_stack[-2][0].append(ret_stack.pop()[0])
    while len(ret_stack) > 1:
        ret_stack[-2][0].append(ret_stack.pop()[0])
    return ret_stack[0]  # return type: [(op, [arg])] where op, arg are aliases of str
        
class bfa_symbols:
    def __init__(self, symbol_list):
        self.symbol_list = symbol_list
    
    def __getitem__(self, symbol):
        try:
            val = int(symbol)  # will work if symbol is an int or a base 10 string
            while len(self.symbol_list) <= val
                self.symbol_list.append(len(self.symbol_list))
        except(ValueError):
            try:
                val = self.symbol_list.index(symbol)
            except(ValueError):
                val = self.symbol_list.length()
                self.symbol_list.append(symbol)
        return val

std = {}
primitive = {
    op: bfo_primitive(bf) for op, bf in {
        'inc': '+', 
        'dec': '-', 
        'ipt': ',', 
        'opt': '.', 
    }.items()
}

def bfa_ops(base, symbols=None, objs=std)  # might even work
    while len(base) == 1:
        base = base[0]  # that way single line functions will not create new objs
                        # note this means subarg remaps will need to be included in any library
    symbols = symbols or []
    if type(symbols) == list:
        symbols = bfa_symbols(symbols)
    if type(base) is tuple:  # i.e. (op, args) or (str, [str])
        op, args = base
        if op in primitive:
            return (primitive[op], args)
        elif op in objs:
            return (objs[op], args)
        else:
            raise NameError
    routine = []
    loop_args = None
    for x in base:
        if type(x) is tuple and x[0] == 'wnz':
            loop_args = x[1]
            if len(loop_args) == 1:
                loop_args.append(0)
            elif len(loop_args) != 2:
                raise TypeError
            loop_args[1] = int(loop_args(1))
        else:
            obj, args = bfa_ops(x)
            if loop_args:
                obj = bfo_loop(obj, loop_args.pop())
                args = loop_args + args  # i.e. args = [loop_args[0]] + args
                loop_args = None
            routine.append(obj, tuple(symbols[arg] for arg in args))
    return bfo(routine), symbols.symbol_list
        
        
class bfo_lib(dict):
    def __setitem__(self, op, obj):
        if type(obj) is str:
            self.add_obj(op, obj)
        else:
            dict.__setitem__(self, op, obj)
    
    def assemble(self, bfa, symbols=None):
        tokens = bfa_tokens(bfa)
        tokens = bfa_indented_tokens(tokens)
        return bfa_ops(tokens, symbols, self)[0]

    def add_obj(self, op, bfa, symbols=None):
        obj = self.assemble(bfa, symbols)
        dict.__setitem__(self, op, obj)

std = bfo_lib()

std['mov'] = '''wnz 0
    dec 0
    inc 1'''
std['double'] = '''wnz 0
    dec 0
    inc 1 1'''
std['dmov'] = '''wnz 0
    dec 0
    inc 1
    inc 2'''
std['cnc'] = '''wnz 0
    dec 0
    dec 1'''

std['add'] = '''dmov 0 1 2
mov 2 0'''


std['sub'] = '''wnz 0
    mov 0 1
    mov 2 3
    wnz 3
        mov 3 2
        dec 2
        mov 1 0
        dec 0'''

std['divr_lazy'] = '''wnz 2
    inc 0
    add 1 4 3
    sub 2 3 4 5
    mov 3 2
    wnz 4
        cnc 4 1
        dec 0'''

std['divr'] = '''inc 2
wnz 2
    dec 2
    inc 0
    add 1 4 3
    sub 2 3 4 5
    mov 3 2
    inc 2
    wnz 4
        dec 2
        cnc 4 1
        dec 0'''

std['bit'] = '''wnz 3
 dec 3
 inc 2
 wnz 1
  mov 1 0
  dec 2
 mov 2 1'''