import re


CAP = re.compile('^[A-Z][a-z]+$')
def is_cap_word(word):
    return CAP.match(word) is not None


PATTERNS = {
    '_CAP_': CAP,
    '_LY_' : re.compile('^[a-z]+ly$'),
    '_NUM_': re.compile('^[0-9\.,/-]+$'),
    '_ED_' : re.compile('^[a-z]+ed$'),
    '_ING_': re.compile('^[a-z]+ing$'),
}


def word_class(word):
    for tag, p in PATTERNS.items():
        if p.match(word) is not None:
            return tag
    
    return '_RARE_'