'''
Defines the `split` function, which helpfully splits a line of tokens into a list of strings,
grouping together tokens within quotes.
'''

import enum

class SplitStringError(Exception):
    '''Exception thrown when the "split" function receivies an illegal input.'''
    def __init__(self, *args):
        super().__init__(args)

class InvalidAcceptError(SplitStringError):
    '''Exception thrown when one of the accept functions receives an illegal input.'''
    def __init__(self, *args):
        super().__init__(args)

class QuoteError(SplitStringError):
    '''Exception thrown when a quote in the split input is unclosed.'''
    def __init__(self, *args):
        super().__init__(args)

class EscapeError(SplitStringError):
    '''Exception thrown when an invalid backslash character appears in the string.'''
    def __init__(self, *args):
        super().__init__(args)

class _State(enum.Enum):
    SPACE = 0
    WORD = 1
    QUOTES = 2

def _accept_word_char(string, i) -> int:
    if str.isspace(string[i]) or (string[i] == '"' and not (i - 1 >= 0 and string[i - 1] == '\\')):
        raise InvalidAcceptError(
            f'Expected a valid word character, found "{string[i]}" at index {i}.')
    return i + 1

def _accept_space_char(string, i) -> int:
    if not str.isspace(string[i]):
        raise InvalidAcceptError(
            f'Expected a valid space character, found "{string[i]}" at index {i}.')
    return i + 1

def _make_word(string, begin, end):
    word = string[begin:end]

    # Take out non-escaped backslashes and interpret escaped backslashes.
    # Except if there is an invalid character after the backslash.
    backslash_loc = word.find('\\')
    while backslash_loc != -1:
        next_idx = backslash_loc + 1
        if next_idx < len(word):
            next_char = word[next_idx]
            if '\\' == next_char:
                word = word[:backslash_loc] + word[backslash_loc + 1:]
                backslash_loc = word.find('\\', backslash_loc + 1)
            elif '"' == next_char:
                word = word[:backslash_loc] + word[backslash_loc + 1:]
                backslash_loc = word.find('\\', backslash_loc)
            else:
                raise EscapeError(
                    f'Cannot escape {next_char} character index {begin + next_idx}'
                )
        else:
            raise EscapeError(
                f'Invalid character "\\" at index {begin + backslash_loc}'
            )

    return word

def _process_space_state(string, i) -> (_State, int):
    # If the check character is a quote, we are beginning a quote section.
    if string[i] == '"':
        return (_State.QUOTES, i + 1)

    # If it's anything else but space, process as a word input.
    if not str.isspace(string[i]):
        return (_State.WORD, i)

    # Otherwise, move to the next character in the space state.
    return (_State.SPACE, i + 1)

def _process_word_state(string, i, begin_word, result) -> (_State, int, int):
    '''Returns (next state, i, begin word)'''
    # If the begin word isn't set, then set it and continue. Since we assume that we've
    # entered the state properly, the first character is assumed to be a non-space non-quote.
    if begin_word is None:
        return (_State.WORD, _accept_word_char(string, i), i)

    # If the string is a space, add the word to the result list and return to the space
    # state.
    if str.isspace(string[i]):
        word = _make_word(string, begin_word, i)
        result.append(word)
        return (_State.SPACE, i, None)

    # Otherwise, move on.
    return (_State.WORD, _accept_word_char(string, i), begin_word)

def _process_quote_state(string, i, begin_word, result) -> (_State, int, int):
    '''Returns (next state, i, begin_word)'''
    # Setup if this is the first time in this state. If the first character is a quote, that means
    # the user provided "".
    if begin_word is None:
        # There is a special case in which the user inputs '"",' or an empty word, which we need to
        # handle here.
        if string[i] == '"':
            result.append('')

            # Except if the next character is not a space.
            next_idx = i + 1
            if next_idx < len(string) and not str.isspace(string[next_idx]):
                raise QuoteError(
                    'A space must follow quotes before beginning the next word.'
                )

            return (_State.SPACE, i + 1, None)

        return (_State.QUOTES, i + 1, i)

    # End the quote if the end of quote char is found. If it is escaped, ignore it.
    if string[i] == '"' and not (i - 1 >= 0 and string[i - 1] == '\\'):
        word = _make_word(string, begin_word, i)
        result.append(word)

        # Except if the next character is not a space.
        next_idx = i + 1
        if next_idx < len(string) and not str.isspace(string[next_idx]):
            raise QuoteError(
                'A space must follow quotes before beginning the next word.'
            )

        return (_State.SPACE, i + 1, None)

    # Otherwise, progress through the quote.
    return (_State.QUOTES, i + 1, begin_word)

def split(string: str) -> list:
    '''Splits the string into a list of strings, grouping together arguments inbetween quotes
    (").'''

    result = []
    begin_word = None
    state = _State.SPACE
    i = 0

    # This is just implemented as a DFA.
    while i < len(string):
        if state == _State.SPACE:
            state, i = _process_space_state(string, i)

        elif state == _State.WORD:
            state, i, begin_word = _process_word_state(string, i, begin_word, result)

        elif state == _State.QUOTES:
            state, i, begin_word = _process_quote_state(string, i, begin_word, result)

    # Raise an exception if we ended in the QUOTES state, because this ought never to happen; every
    # quote block should end in a quote, so it should end in the SPACE state.
    if state == _State.QUOTES:
        raise QuoteError("Quote was not closed.")

    # If we ended in a word, add it to the result.
    if not begin_word is None:
        word = _make_word(string, begin_word, i)
        result.append(word)

    return result
