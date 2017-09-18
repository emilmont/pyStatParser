from __future__ import print_function
# http://bulba.sdsu.edu/jeanette/thesis/PennTags.html
TAGS = set((
    'S',      # simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a wh-word and that does not exhibit subject-verb inversion.
    'SBAR',   # Clause introduced by a (possibly empty) subordinating conjunction.
    'SBARQ',  # Direct question introduced by a wh-word or a wh-phrase. Indirect questions and relative clauses should be bracketed as SBAR, not SBARQ.
    'SINV',   # Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal.
    'SQ',     # Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ.
    
    'ADJP',   # Adjective Phrase.
    'ADVP',   # Adverb Phrase.
    'CONJP',  # Conjunction Phrase.
    'FRAG',   # Fragment.
    'INTJ',   # Interjection. Corresponds approximately to the part-of-speech tag UH.
    'LST',    # List marker. Includes surrounding punctuation.
    'NAC',    # Not a Constituent; used to show the scope of certain prenominal modifiers within an NP.
    'NP',     # Noun Phrase. 
    'NX',     # Used within certain complex NPs to mark the head of the NP. Corresponds very roughly to N-bar level but used quite differently.
    'PP',     # Prepositional Phrase.
    'PRN',    # Parenthetical. 
    'PRT',    # Particle. Category for words that should be tagged RP. 
    'QP',     # Quantifier Phrase (i.e. complex measure/amount phrase); used within NP.
    'RRC',    # Reduced Relative Clause. 
    'UCP',    # Unlike Coordinated Phrase. 
    'VP',     # Verb Phrase. 
    'WHADJP', # Wh-adjective Phrase. Adjectival phrase containing a wh-adverb, as in how hot.
    'WHADVP',  # Wh-adverb Phrase. Introduces a clause with an NP gap. May be null (containing the 0 complementizer) or lexical, containing a wh-adverb such as how or why.
    'WHNP',   # Wh-noun Phrase. Introduces a clause with an NP gap. May be null (containing the 0 complementizer) or lexical, containing some wh-word, e.g. who, which book, whose daughter, none of which, or how many leopards.
    'WHPP',   # Wh-prepositional Phrase. Prepositional phrase containing a wh-noun phrase (such as of which or by whose authority) that either introduces a PP gap or is contained by a WHNP
    
    'CC',     # Coordinating conjunction
    'CD',     # Cardinal number
    'DT',     # Determiner
    'EX',     # Existential there
    'FW',     # Foreign word
    'IN',     # Preposition or subordinating conjunction
    'JJ',     # Adjective
    'JJR',    # Adjective, comparative
    'JJS',    # Adjective, superlative
    'LS',     # List item marker
    'MD',     # Modal
    'NN',     # Noun, singular or mass
    'NNS',    # Noun, plural
    'NNP',    # Proper noun, singular
    'NNPS',   # Proper noun, plural
    'PDT',    # Predeterminer
    'POS',    # Possessive ending
    'PRP',    # Personal pronoun
    'PRP$',   # Possessive pronoun (prolog version PRP-S)
    'RB',     # Adverb
    'RBR',    # Adverb, comparative
    'RBS',    # Adverb, superlative
    'RP',     # Particle
    'SYM',    # Symbol
    'TO',     # to
    'UH',     # Interjection
    'VB',     # Verb, base form
    'VBD',    # Verb, past tense
    'VBG',    # Verb, gerund or present participle
    'VBN',    # Verb, past participle
    'VBP',    # Verb, non-3rd person singular present
    'VBZ',    # Verb, 3rd person singular present
    'WDT',    # Wh-determiner
    'WP',     # Wh-pronoun
    'WP$',    # Possessive wh-pronoun (prolog version WP-S)
    'WRB',    # Wh-adverb
    
    '.',      # Sentence final puntuation
    ',',      # Comma
    ':',      # Mid sentence punctuation
    '-LRB-',  # Left parenthesis
    '-RRB-',  # Right parenthesis
    '``',     # Start quote
    "''",     # End quote
    '#',      # Pound sign
    '$',      # Dollar sign
    
    # These will be filtered in the following steps
    '',       # Empty
    '-NONE-', # 
    'X'       # Uncertain
))


def normalize_tag(tag):
    for sep in ('-', '=', '|'):
        i = tag.find(sep)
        if i > 0:
            return tag[:i]
    return tag


def normalize_word(word):
    return word.replace("\\/", '/')


TAG, SEPARATOR, WORD = 1, 2, 3
def parse_node(f, node, text):
    tag = []
    state = TAG
    while True:
        c = f.read(1) # default system buffering
        text.append(c)
        if c == '':
            raise Exception("Unexpected end of file")
        
        if state == TAG:
            if c.isspace():
                state = SEPARATOR
                tag = normalize_tag(''.join(tag))
                if tag not in TAGS:
                    raise Exception("Unrecognized tag: {%s}" % tag)
                node.append(tag)
            elif c == '(':
                # Handle starting ((
                state = SEPARATOR
                node.append('')
                branch = []
                node.append(branch)
                parse_node(f, branch, text)
            else:
                tag.append(c)
        
        elif state == SEPARATOR:
            if c.isspace():
                pass
            elif c == '(':
                branch = []
                node.append(branch)
                parse_node(f, branch, text)
            elif c == ')':
                break
            else:
                word = [c]
                state = WORD
        
        elif state == WORD:
            if c == ')':
                node.append(normalize_word(''.join(word)))
                break
            else:
                word.append(c)


def parse_treebank(file_path):
    f = open(file_path)
    text = None
    while True:
        try:
            c = f.read(1) # default system buffering
            if c == '': break
            
            if c == '(':
                tree = []
                text = [c]
                parse_node(f, tree, text)
                if tree[0] == '':
                    # Remove initial empty node from penn treebank
                    tree = tree[1]
                yield tree
        except Exception as e:
            print(''.join(text))
            print(e)
            import sys
            sys.exit()

REPLACEMENTS = (
    ('(` `)', '(`` ``)'),
    ("(' <)", "('' '')"),
    ('<', "'"),
    ('NPP', 'NP'),
    ('(! !)', '(. !)'),
    ('(? ?)', '(. ?)'),
)
def normalize_questionbank(in_path, out_path):
    with open(in_path) as original, open(out_path, 'w') as penn_norm:
        for line in original:
            for old, new in REPLACEMENTS:
                line = line.replace(old, new)
            penn_norm.write(line)
