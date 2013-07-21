from json import dumps


TAG, SEPARATOR, WORD = 1, 2, 3
def parse_node(f, node):
    tag = []
    state = TAG
    while True:
        c = f.read(1) # default system buffering
        if c == '':
            raise Exception("Unexpected end of file")
        
        if state == TAG:
            if c.isspace():
                state = SEPARATOR
                node.append(''.join(tag))
            else:
                tag.append(c)
        
        elif state == SEPARATOR:
            if c.isspace():
                pass
            elif c == '(':
                branch = []
                node.append(branch)
                parse_node(f, branch)
            elif c == ')':
                break
            else:
                word = [c]
                state = WORD
        
        elif state == WORD:
            if c == ')':
                node.append(''.join(word))
                break
            else:
                word.append(c)


def parse_treebank(file_path):
    print 'parsing: %s' % file_path
    f = open(file_path)
    while True:
        c = f.read(1) # default system buffering
        if c == '': break
        
        if c == '(':
            tree = []
            parse_node(f, tree)
            if tree[0] == '':
                # Remove initial empty node from penn treebank
                tree = tree[1]
            yield tree


def empty_rule_filter(node):
    if isinstance(node, list) and len(node) < 2:
        if node[0] != '':
            raise Exception("Unexpected content for empty rule")
        return False
    return True


def chomsky_normal_form(tree):
    # Prune possible empty rules (questionbank defect)
    tree[:] = filter(empty_rule_filter, tree)
    
    if not isinstance(tree[0], basestring):
        raise Exception("Left symbol should be a string: %s" % str(tree))
    
    n = len(tree)
    if n < 2:
        raise Exception("Rule should have at least two items: %s" % str(tree))
    
    if n == 2:
        # X -> word
        if isinstance(tree[1], list):
            # (1) Normalise single non-terminal on the right
            tree[0] = "%s+%s" % (tree[0], tree[1][0])
            tree[1:] = tree[1][1:]
            chomsky_normal_form(tree)
        else:
            if not isinstance(tree[1], basestring):
                raise Exception("Terminal should be a string: %s" % str(tree))
    
    elif n == 3:
        # X -> Y1, Y2
        for i in (1, 2):
            if isinstance(tree[i], basestring):
                # (2) Normalise rule that mixes terminal with non-terminal
                tree[i] = [tree[i].upper(), tree[i]]
            else:
                if not isinstance(tree[i], list):
                    raise Exception("Non-terminal should be a list: %s" % str(tree))
                chomsky_normal_form(tree[i])
    
    else:
        # (3) Normalise illegal n-ary rule
        tree[2] = [tree[0]] + tree[2:]
        del tree[3:]
        chomsky_normal_form(tree)


def gen_norm(norm_path, input_treebanks):
    with open(norm_path, 'w') as norm:
        for path in input_treebanks:
            for tree in parse_treebank(path):
                try:
                    chomsky_normal_form(tree)
                    norm.write(dumps(tree) + '\n')
                except Exception, e:
                    print e
                    print 'Discarding: %s' % str(tree)
