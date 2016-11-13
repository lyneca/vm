
def split_bits(arg, bits = 8):
    return (arg >> bits, arg & (1 << bits) - 1)

class NeumannMachine:
    class MechData:
        def __init__(self, data, input):
            self.data = data
            self.input = iter(input)
            self.has_output = False
        
        def __getitem__(self, i):
            return self.input.__next__() if i == 0xFF else self.data[i]
            
        def __setitem__(self, i, x):
            self.data[i] = x
            self.has_output = i == 0xFF
        
            
    
    def __init__(mech, data = None, input = (), fptr = 0x10, reg = None):
        mech.data = MechData(data if data else {}, input)
        mech.fptr = fptr
        if not reg:
            reg = [0x0000 for i in range(16)]
    def __iter__(mech):
        while mech.data[mech.fptr] >> 6:
            word = mech.data[mech.fptr]
            command, args = split_bits(word, 12)
            mech.operations[command](mech, args)
            if mech.data.has_output:
                yield mech.data.data[0xFF]
                mech.data.has_output = False

                
                
            


def max(x):
    return x & 0xFFFF if x >= 0 else -max(-x)

def operation(func):
    def decorated(mech, args):
        outr, args = split_bits(args, 8)
        mech.reg[outr] = NeumannMachine.max(func(mech, args))
    return decorated

def read_operation(func):
    def decorated(mech, args):
        outr, args = split_bits(args, 8)
        func(mech, mech.reg[outr], args)
    return decorated

def binary_operation(func):
    @operation
    def decorated(mech, args):
        return func(*(mech.reg[r] for r in split_bits(args, 4)))
    return decorated

vnm_add = binary_operation(int.__add__)
vnm_subtract = binary_operation(int.__sub__)
vnm_bit_and = binary_operation(int.__and__)
vnm_bit_xor = binary_operation(int.__xor__)
vnm_lshift = binary_operation(int.__lshift__)
vnm_rshift = binary_operation(int.__rshift__)

@operation
def vnm_set(mech, args):
    return args

@operation
def vnm_load(mech, args):
    return mech.data[args]

@read_operation
def vnm_store(mech, regval, args):
    mech.data[args] = regval

@operation
def vnm_i_load(mech, args):
    return mech.data[mech.reg[args & 0xF]]

@read_operation
def vnm_i_store(mech, regval, args):
    mech.data[mech.reg[args & 0xF]] = regval

@read_operation
def vnm_jez(mech, regval, args):
    if regval == 0:
        mech.fptr = args

@read_operation
def vnm_jgz(mech, regval, args):
    if regval > 0:
        mech.fptr = args

@read_operation
def vnm_i_jmp(mech, regval, args):
    mech.fptr = regval

@operation
def vnm_call(mech, args):
    out = mech.fptr
    mech.fptr = args
    return out



NeumannMachine.operations = [
    None, # this will be caught by the main loop and so no entry is needed
    vnm_add, 
    vnm_subtract, 
    vnm_bit_and, 
    vnm_bit_xor, 
    vnm_lshift, 
    vnm_rshift, 
    vnm_set, 
    vnm_load, 
    vnm_store, 
    vnm_i_load, 
    vnm_i_store, 
    vnm_jez, 
    vnm_jgz, 
    vnm_i_jmp, 
    vnm_call
]

