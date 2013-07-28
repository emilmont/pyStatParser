"""
Extract the words from a treebank and reverse the tokenization
"""

def get_words(tree):
    # Assume well formed
    if len(tree) == 2:
        return [tree[1]]
    else:
        return get_words(tree[1]) + get_words(tree[2])


def get_sentence(tree):
    words = get_words(tree)
    sentence = []
    
    open_quotes = False
    open_parenthesis = False
    dollar = False
    for word in words:
        # Quotes
        if word == '``':
            open_quotes = True
            sentence.append('"')
        elif open_quotes:
            sentence[-1] += word
            open_quotes = False
        elif word == "''":
            sentence[-1] += '"'
        
        # Parenthesis
        elif word == '-LRB-':
            open_parenthesis = True
            sentence.append('(')
        elif open_parenthesis:
            sentence[-1] += word
            open_parenthesis = False
        elif word == "-RRB-":
            sentence[-1] += ')'
        
        # Dollar
        elif word == '$':
            sentence.append(word)
            dollar = True
        elif dollar:
            sentence[-1] += word
            dollar = False
        
        elif word in ("?", ",", ".", ":", "%", "n't") or word[0] == "'":
            sentence[-1] += word
        
        else:
            sentence.append(word)
    
    return ' '.join(sentence), len(words)
