
def iterate_and_cast_back(func):
    def run_machine (input = '', *args, **kwargs):
        input_type = type(input)
        if input_type is str:
            input = (ord(x) for x in input) 
        output = func(input, *args, **kwargs)
        if input_type is str:
            output_list = list(output)
            output_str = ''.join(chr(x) for x in output_list)
            return output_str if output_str.isprintable() else output_list
        else:
            return input_type(output)

