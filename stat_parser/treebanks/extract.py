"""
Extract the words from a tree and reverse the tokenization
"""

def get_words(tree):
    # Assume well formed
    if len(tree) == 2:
        return [tree[1]]
    else:
        return get_words(tree[1]) + get_words(tree[2])


LEFT = {
    '``': '"',
    '-LRB-': '(',
    '$': '$',
}
RIGHT = {
    "''": '"',
    "-RRB-": ')',
}

def get_sentence(tree):
    words = get_words(tree)
    n = len(words)
    sentence = []
    skip = False
    for i, word in enumerate(words):
        if skip:
            skip = False
        
        elif word in LEFT and i+1 < n:
            sentence.append(LEFT[word] + words[i+1])
            skip = True
        
        elif word in RIGHT:
            sentence[-1] += RIGHT[word]
        
        elif word in ("?", ",", ".", ":", "%", "n't") or word[0] == "'":
            sentence[-1] += word
        
        else:
            sentence.append(word)
    
    return ' '.join(sentence), n
