import re

from addok.utils import yielder


_CACHE = {}


def _stemmize(s):
    """Very lite French stemming. Try to remove every letter that is not
    significant."""
    if not s in _CACHE:
        rules = (
            ("g(?=[eyi])", "j"),
            ("(?<=g)u(?=[aeio])", ""),
            ("c(?=[aou])", "k"),
            ("(?<=[aeiouy])s(?=[aeiouy])", "z"),
            ("q", "k"),
            ("cc(?=[ie])", "s"),  # Others will hit the c => k and deduplicate
            ("ck", "k"),
            ("ph", "f"),
            ("(?<=t)h", ""),
            ("sc", "s"),
            ("w", "v"),
            ("c(?=[eiy])", "s"),
            ("y", "i"),
            ("esn", "en"),
            ("s$", ""),
            ("(?<=u)l?x$", ""),  # eaux, eux, aux, aulx
            ("(?<=u)lt$", "t"),
            ("[td]$", ""),
            ("(?<=\\w\\w)(e$)", ""),  # Remove "e" at last position only if it
                                      # follows two letters?
            ("(?<=[aeiou])(m)(?=[pbg])", "n"),
            ("(\\D)(?=\\1)", ""),  # Remove duplicate letters.
        )
        _s = s
        for pattern, repl in rules:
            _s = re.sub(pattern, repl, _s)
        _CACHE[s] = _s
    return _CACHE[s]

stemmize = yielder(_stemmize)