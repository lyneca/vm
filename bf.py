
class bf_data:
    def __init__(self, data=None, data_ptr=0):
        self.data_ptr = data_ptr
        self.data = data or []
        while len(self.data) < self.data_ptr:
            self.data.append(0)
    
    def increment(self):
        self.data[data_ptr] += 1
    
    def decrement(self):
        self.data[data_ptr] -= 1
    
    def shiftr(self):
        self.data_ptr += 1
        
    def shiftl(self):
        if self.data_ptr:
            self.data_ptr -= 1

    def get(self):
        return self.data[self.data_ptr]
    
    def set(self, value):
        self.data[self.data_ptr] = value




class bf_code:
    def __init__(self, code=None, code_ptr=0):
        self.code = code or []
        self.code_ptr = code_ptr
    
    def get(self):
        return self.code[self.code_ptr]
        
    def match_bracket(self):
        bracket_values = {'[': +1, ']': -1}
        code_step = brackets = bracket_values[self.get()]
        while brackets != 0:
            self.code_ptr += code_step  # next char
            brackets += bracket_values.get(self.get(), 0)  # account for character
    
    def __iter__(self):
        while self.code_ptr < len(self.code):
            yield self.get()
            self.code_ptr += 1


class bf_iter:
    def __init__(self, code, input=(), data = None):
        self.code = bf_code(code)
        self.data = bf_data(data, 0)
        self.input = bf_input(self.data, input)
    
    def begin_while(self):
        if self.data.get() == 0:
            self.code.match_bracket()
    
    def end_while(self):
        if self.data.get() != 0:
            self.code.match_bracket()

    def input(self):
        self.data.set(self.input.__next__())
    
    def __iter__(self)
        for char in self.code:
            bf = {
                '+': self.data.increment,
                '-': self.data.decrement,
                '>': self.data.shiftr,
                '<': self.data.shiftl,
                '[': self.begin_while,
                ']': self.end_while
                ',': self.input,
            }
            if char == '.':
                yield self.data.get()
            elif char in bf:
                bf[char]()


def run_bf (code, input = '', data = None):
    input_type = type(input)
    if input_type is str:
        input = (ord(x) for x in input) 
    output = bf_iter(code, input, data)
    if input_type is str:
        output_list = list(output)
        output_str = ''.join(chr(x) for x in output_list)
        return output_str if output_str.isprintable() else output_list
    else:
        return input_type(output)


geq = ',+>,+<[->->>+<<[->+<]>[[-<+>]>-<]>[.-<<<[-]>>>]<<<]>[[-].]'
safe_sub = ',+>,+<[->->>+<<[->+<]>[[-<+>]>-<]>[-.<<<[-]>>>]<<<]>[.[-]]'
difference = ',+>,+<[->->>+<<[->+<]>[[-<+>]>-<]>[-<<<.[-]>>>]<<<]>[.[-]]'

sub = ',>,>,>,<<<[[->+<]>>[->+<]>[-[-<+>]<<-[-<+>]>>]<<<].>.>.>.'
bit = ',[->>+<[->->+<<]>[-<+>]<<]>.>>.'
bits = ',[[->>+<[->->+<<]>[-<+>]<<]>.[-]>>[-<<<+>>>]<<<]'
mod_ceiling = '>>,<,>[<[->>+>+<<<]>>[-<<+>>]<[[->+<]>>[->+<]>[-[-<+>]<<-[-<+>]>>]<<<]>[-<+>]>[-<<<->>>]<<]<.'
quotient = '>>,<,>+[-<<+>[->>+>+<<<]>>[-<<+>>]<[[->+<]>>[->+<]>[-[-<+>]<<-[-<+>]>>]<<<]>+[-<+>]>[[-<<<->>>]<<-<<->>>>]<<]<<.>.'


almost_array = ',[>[->+>>+<<<]>+[-<+>]+>>[-[->>+<<]>>]>,<+[<<[[-]>>[-<<+>>]]>>[-<<+>>]<<]<<-<<<-]>>>+>>,[-[->>+<<]>>]>.'

std = {}
def assemble_bf(static, compound = std, args=None):
    if not args: args = [0]
    args = dict(enumerate(args))
    bf = ''
    ptr = args[0]
    indent = [True]
    brackets = [0]
    
    primitive = {'inc': '+', 'dec': '-', 'ipt': ',', 'opt': '.', 'for': '['}
    
    def shift(new_arg):
        new_ptr = args.get(new_arg, new_arg + args[0])
        nonlocal ptr, bf
        bf += '>' * (new_ptr - ptr)
        bf += '<' * (ptr - new_ptr)
        ptr = new_ptr
    
    if type(static) is str:
        static = static.splitlines()
    for line in static:
        if line.isspace(): continue
        
        space = 0
        while line[space].isspace():
            space += 1
        if indent.count(True) < len(brackets):
            if space >= len(indent):
                indent.extend(False for i in range(space - len(indent)))
                indent.append(True)
            else:
                raise IndentationError
        if space >= len(indent) or not indent[space]:
            raise IndentationError
        for i in range(indent[space:].count(True) - 1):
            shift(brackets.pop())
            bf += ']'
            indent.pop()
            while not indent[-1]:
                indent.pop()
            
        line = line.split(None, 1)
        if len(line) == 1: line.append('')
        op, line = line
        terminals = [int(x) for x in line.split()]
        
        if op in primitive:
            terminals.append(1)
            shift(terminals[0])
            if op == 'for':
                brackets.append(terminals[0])
                if terminals[1] != 1:
                    raise SyntaxError
            bf += primitive[op] * terminals[1]
        elif op in compound:
            shift(terminals[0])
            bf += assemble_bf(compound[op], compound, terminals)
            
    for new_ptr in brackets[:0:-1]:
        shift(new_ptr)
        bf += ']'
    shift(brackets[0])
    return bf

std['mov'] = '''for 0
    dec 0
    inc 1'''
std['double'] = '''for 0
    dec 0
    inc 1 2'''
std['dmov'] = '''for 0
    dec 0
    inc 1
    inc 2'''
std['cnc'] = '''for 0
    dec 0
    dec 1'''

std['add'] = '''dmov 0 1 2
mov 2 0'''


std['sub'] = '''for 0
    mov 0 1
    mov 2 3
    for 3
        mov 3 2
        dec 2
        mov 1 0
        dec 0'''

std['divr_lazy'] = '''for 2
    inc 0
    add 1 4 3
    sub 2 3 4 5
    mov 3 2
    for 4
        cnc 4 1
        dec 0'''

std['divr'] = '''inc 2
for 2
    dec 2
    inc 0
    add 1 4 3
    sub 2 3 4 5
    mov 3 2
    inc 2
    for 4
        dec 2
        cnc 4 1
        dec 0'''

std['bit'] = '''for 3
 dec 3
 inc 2
 for 1
  mov 1 0
  dec 2
 mov 2 1'''
