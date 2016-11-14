
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
