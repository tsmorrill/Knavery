from functools import reduce
from itertools import groupby, pairwise, product

bits = {'': '',
        '|': '',
        '.': '1',
        '?': '11',
        '!': '111',       
        ',': '1111',
        ';': '11111',
        'a': '10',
        'b': '100',
        'c': '1000',
        'd': '10000',
        'e': '110',
        'f': '1100',
        'g': '11000',
        'h': '1110',
        'i': '11100',
        'j': '111000',
        'k': '11110',
        'l': '111100',
        'm': '1111000',
        'n': '111110',
}

symbols = tuple(bits.keys())[1:] # omit empty string
letters = ('a', 'b', 'c', 'd', 'e',
           'f', 'g', 'h', 'i', 'j',
           'k', 'l', 'm', 'n', '|')


def run_length(data: str):
    return ((sum(1 for _ in y), x) for x, y in groupby(data))


def knave_run(pair):
    run, char = pair
    lie = {'0': '1', '1': '0'}
    return '{0:b}'.format(run) + lie[char]


def knave(word:str):
    pairs = tuple(run_length(word))
    desc = reduce(lambda x, y: x+y, map(knave_run, pairs), '')
    return desc


def guillotine(word:str):
    prefixes = (s for s in symbols[::-1] if bits[s] != '')
    for s in prefixes:
        p = bits[s]
        if word.startswith(p):
            return s, word.removeprefix(p)
    print(f'Cannot match word {word}')
    return None


def translate(word:str):
    acc = ''
    while len(word) > 0:
        s, word = guillotine(word)
        acc += s
    return acc    
                    

def knave_star(word:str):
    return translate(knave(word))


def bonds():
#   print('Lookup table for knave* bonds:')
#    print('--------')
    print('bond = {')
    for s in symbols:
        desc = knave_star(bits[s])
        v = desc[-1] if desc != '' else '|'
        v = v if v in ('|', '.', '?', '!', ',', ';') else ''
        print(f"        '{s}': '{v}',")
    print('}')


def knave_no_bleed(bond):
    bondname = {'|': 'pipe', # James
                '.': 'stop',
                '?': 'orly',
                '!': 'bang',
                ',': 'coma',
                ';': 'semi',
                '': 'none',}
    label = bondname[bond]
#    print(f'Lookup table for knave* descriptions, punctuation removed, bond = {label}:')
#    print('--------')
    print(f'desc_{label} = {{')

    match bond:
        case '|':
            compatible_symb = symbols
        case '':
            compatible_symb = ('|')
        case _:
            compatible_symb = letters
    for s in compatible_symb:
        desc = knave_star(bits[bond] + bits[s]) if s != '|' else '|'
        if bond == '|':
            desc = '|' + desc
        v = desc[-1]
        if v not in {'.', '?', '!', ',', ';'}:
            v = ''
        print(f"          '{s}': '{desc.removesuffix(v)}',")
    print('}')


def main():
    bonds()
    print()
    for bond in ('|', '.', '?', '!', ',', ';', ''):
        knave_no_bleed(bond)
        print('')

if __name__ == "__main__":
    main()
