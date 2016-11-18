
# gives a string with enough < or > to apply a required shift
def bf_shift_str(diff):
    if diff > 0:
        shift_char = '>'
    else:
        shift_char = '<'
        diff *= -1
    return ''.join(shift_char for i in range(diff))

class bf_shifter:
    def __init__(self, current_loc=0):
        self.loc = current_loc
    
    def shift(self, new_loc, silent_shift=0):
        diff = new_loc - self.loc
        self.loc = new_loc
        return bf_shift_str(diff + silent_shift)


#bfo_args()[x] gives x, whereas bfo_args(non_zero_list)[x] gives non_zero_list[x]
#bfo_args() is meant to represent bf routines that operate on the tape directly
class bfo_args(list):
    def __getitem__(self, ind):
        if self:
            return list.__getitem__(self, ind)
        else:
            return ind


class bfo_primitive:
    def __init__(self, bf):
        self.bf = bf
    
    def do(self, shifter, args):
        ret = ''
        try:
            for arg in args:
                ret += shifter.shift(arg)
                ret += self.bf
        except(TypeError):
            ret += shifter.shift(args)
            ret += self.bf

class bfo:
    def __init__(self, routine):
        self.routine = routine  # sequence of length 2 sequences, similar to [(obj, [callargs])]
                                #    representing instruction: obj.do(shift, callargs)
        
    def do(self, shifter, argmap):
        ret = ''
        for obj, subargs in routine:
            subargs = bfo_args(argmap[subarg] for subarg in subargs)
            ret += obj.do(shifter, subargs)

class bfo_loop(bfo):
    def __init__(self, base, post_shift=0):
        self.base = base
        self.post_shift = post_shift
    
    def do(self, shifter, argmap):
        pre_shift = shifter.shift(argmap[0])
        body = base.do(shifter, argmap[1:])
        post_shift = shifter.shift(argmap[0], self.post_shift)
        return pre_shift + '[' + body + post_shift + ']'

# for example:
#  inc = bfo_primitive('+')
#  dec = bfo_primitive('-')
#  mov = bfo(bfo_loop(((inc, (1,)), (dec, (0,))), 0), (0, 0, 1))
