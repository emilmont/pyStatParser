"""
CKY algorithm from the "Natural Language Processing" course by Michael Collins
https://class.coursera.org/nlangp-001/class
"""
from collections import defaultdict

try:
    from nltk import Tree
    
    def nltk_tree(t):
        return Tree(t[0], [c if isinstance(c, basestring) else nltk_tree(c) for c in t[1:]])
    
    nltk_installed = True

except ImportError:
    nltk_installed = False

from stat_parser.learn import build_model
from stat_parser.tokenizer import PennTreebankTokenizer
from stat_parser.treebanks.normalize import un_chomsky_normal_form


def argmax(lst):
    return max(lst) if lst else (0.0, None)


def backtrace(back, bp):
    # Extract the tree from the backpointers
    if not back: return None
    if len(back) == 6:
        (X, Y, Z, i, s, j) = back
        return [X, backtrace(bp[i  , s, Y], bp),
                   backtrace(bp[s+1, j, Z], bp)]
    else:
        (X, Y, i, i) = back
        return [X, Y]


def CKY(pcfg, norm_words):
    x, n = [("", "")] + norm_words, len(norm_words)
    
    # Charts
    pi = defaultdict(float)
    bp = defaultdict(tuple)
    for i in range(1, n+1):
        for X in pcfg.N:
            norm, word = x[i]
            if (X, norm) in pcfg.q1:
                pi[i, i, X] = pcfg.q1[X, norm]
                bp[i, i, X] = (X, word, i, i)
    
    # Dynamic program
    for l in range(1, n):
        for i in range(1, n-l+1):
            j = i+l
            for X in pcfg.N:
                # Note that we only check rules that exist in training
                # and have non-zero probability
                score, back = argmax([(
                        pcfg.q2[X, Y, Z] * pi[i, s, Y] * pi[s+1, j, Z],
                        (X, Y, Z, i, s, j)
                    ) for s in range(i, j)
                        for Y, Z in pcfg.binary_rules[X]
                            if pi[i  , s, Y] > 0.0
                            if pi[s+1, j, Z] > 0.0
                ])
                
                if score > 0.0:
                    bp[i, j, X], pi[i, j, X] = back, score
    
    _, top = max([(pi[1, n, X], bp[1, n, X]) for X in pcfg.N])
    return backtrace(top, bp)


class Parser:
    def __init__(self, pcfg=None):
        if pcfg is None:
            pcfg = build_model()
        
        self.pcfg = pcfg
        self.tokenizer = PennTreebankTokenizer()
        
        if nltk_installed:
            self.parse = self.__nltk_parse
        else:
            self.parse = self.__parse
    
    def raw_parse(self, sentence):
        norm_words = []
        for word in self.tokenizer.tokenize(sentence):
            if isinstance(word, tuple):
                # This is already a word normalized to the Treebank conventions
                norm_words.append(word)
            else:
                # _RARE_ normalization
                norm_words.append((self.pcfg.norm_word(word), word))
        return CKY(self.pcfg, norm_words)
    
    def __parse(self, sentence):
        tree = self.raw_parse(sentence)
        un_chomsky_normal_form(tree)
        return tree
    
    def __nltk_parse(self, sentence):
        tree = nltk_tree(self.__parse(sentence))
        return tree
