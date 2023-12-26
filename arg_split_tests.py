'''
Unit tests for the arg_pos module.
'''

from arg_pos import split
from arg_pos import QuoteError
from arg_pos import InvalidAcceptError
from arg_pos import EscapeError

def _tests():
    '''Runs tests on the split function.'''
    tests = {
        'normal': {
            'input': 'the quick brown fox',
            'output': ['the', 'quick', 'brown', 'fox'],
        },
        'quote normal': {
            'input': 'the quick "brown fox"',
            'output': ['the', 'quick', 'brown fox'],
        },
        'space padding': {
            'input': '     the quick brown fox     ',
            'output': ['the', 'quick', 'brown', 'fox'],
        },
        'begin quote': {
            'input': '"the quick" brown fox',
            'output': ['the quick', 'brown', 'fox'],
        },
        'empty word': {
            'input': 'the "" quick brown fox',
            'output': ['the', '', 'quick', 'brown', 'fox'],
        },
        'begin empty word': {
            'input': '"" the quick brown fox',
            'output': ['', 'the', 'quick', 'brown', 'fox'],
        },
        'end empty word': {
            'input': 'the quick brown fox ""',
            'output': ['the', 'quick', 'brown', 'fox', ''],
        },
        'escaped quote': {
            'input': 'the qu\\"ck brown fox',
            'output': ['the', 'qu"ck', 'brown', 'fox'],
        },
        'escaped quote begin': {
            'input': '\\"the quick brown fox',
            'output': ['"the', 'quick', 'brown', 'fox'],
        },
        'escaped quote end': {
            'input': 'the quick brown fox\\"',
            'output': ['the', 'quick', 'brown', 'fox"'],
        },
        'escaped quote in quote': {
            'input': 'the "qu\\"ck" brown fox',
            'output': ['the', 'qu"ck', 'brown', 'fox'],
        },
        'escaped quote begin in quote': {
            'input': '"\\"the quick" brown fox',
            'output': ['"the quick', 'brown', 'fox'],
        },
        'escaped quote end in quote': {
            'input': 'the quick "brown fox\\""',
            'output': ['the', 'quick', 'brown fox"'],
        },
        'escape backslash': {
            'input': 'the qu\\\\ck brown fox',
            'output': ['the', 'qu\\ck', 'brown', 'fox'],
        },
        'escape backslash begin': {
            'input': '\\\\the quick brown fox',
            'output': ['\\the', 'quick', 'brown', 'fox']
        },
        'escape backslash end': {
            'input': 'the quick brown fox\\\\',
            'output': ['the', 'quick', 'brown', 'fox\\']
        },
        'open quote error': {
            'input': 'the quick "brown fox',
            'except': QuoteError,
        },
        'quote in word error': {
            'input': 'the qu"ck brown fox',
            'except': InvalidAcceptError,
        },
        'no space after quote error': {
            'input': 'the quick "brown"fox',
            'except': QuoteError,
        },
        'quote at end of string error': {
            'input': 'the quick brown fox "',
            'except': QuoteError,
        },
        'invalid escape character error': {
            'input': 'the \\quick brown fox',
            'except': EscapeError
        },
        'backslash at end of input error': {
            'input': 'the quick brown fox\\',
            'except': EscapeError
        }
    }

    for key, val in tests.items():
        if not 'except' in val:
            try:
                split_out = split(val['input'])
                result = 'PASSED' if split_out == val['output'] else 'FAILED'
                if 'FAILED' == result:
                    result += f'\n\tExpected: {val["output"]}\n\tFound: {split_out}'
            except Exception as err:
                result = f'FAILED\n\tUnexpected exception {err}'
        else:
            to_catch = val['except']
            try:
                split_out = split(val['input'])
                result = f'FAILED\n\tExpected exception {to_catch}'
                result += f'\n\tFinished with result {split_out}'
            except to_catch as err:
                result = 'PASSED'
            except Exception as err:
                result = f'FAILED\n\tExpected exception {to_catch}'
                result += f'\n\tFound exception {type(err)}'

        print(f'{key}: {result}')

if __name__ == '__main__':
    _tests()
