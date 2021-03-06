
from . lmao_to_rofl import convert_LMAOcode_to_ROFLcode
from . lolcode_parser import build_parser, parse_LOLcode
from . symbol_table import SymbolTable

def convert_compiled_code_to_str(compiled_code):
    lines = ''
    for row in compiled_code:
        line = ''
        for elem in row:
            line += str(elem) + ' '
        line += '\n'
        lines += line
    return lines

def generate_LMAOcode_from_LOLcode(lolcode_str):
    parse_tree = parse_LOLcode(lolcode_str)
    print("Parse Tree:")
    print(parse_tree)

    symbol_table = SymbolTable()
    compiled_code = []
    parse_tree.compile(symbol_table, compiled_code)
    
    lmaocode_str = convert_compiled_code_to_str(compiled_code)
    return lmaocode_str
    
def generate_ROFLcode_from_LOLcode(lolcode_str):
    lmaocode_str = generate_LMAOcode_from_LOLcode(lolcode_str)
    return convert_LMAOcode_to_ROFLcode(lmaocode_str)
