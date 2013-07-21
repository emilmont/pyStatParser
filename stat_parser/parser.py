from collections import defaultdict
from stat_parser.learn import build_model


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


def CKY(pcfg, sentence):
    x, n = [""] + sentence, len(sentence)
    
    # Charts
    pi = defaultdict(float)
    bp = {}
    for i in range(1, n+1):
        for X in pcfg.N:
            if (X, x[i]) in pcfg.q1:
                pi[i, i, X] = pcfg.q1[X, x[i]]
                bp[i, i, X] = (X, x[i], i, i)
    
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
    
    return backtrace(bp[1, n, "SBARQ"], bp)


class Parser:
    def __init__(self, pcfg=None):
        if pcfg is None:
            pcfg = build_model()
        
        self.pcfg = pcfg
    
    def parse(self, sentence):
        # TODO: Write a proper tokenizer
        s = map(self.pcfg.norm_word, sentence.strip().split())
        return CKY(self.pcfg, s)
