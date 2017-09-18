from __future__ import print_function
from json import dumps
from six.moves import filter, range
from six import text_type as str
string_types = str

from stat_parser.treebanks.parse import parse_treebank
from stat_parser.word_classes import is_cap_word


def chomsky_normal_form(tree):
    if not isinstance(tree, list):
        raise Exception("Rule should be a list")
    
    n = len(tree)
    if n < 2:
        raise Exception("Rule should have at least two items: %s" % str(tree))
    
    if not isinstance(tree[0], string_types):
        raise Exception("Root should be a string: %s" % str(tree))
    
    if n == 2:
        # X -> word
        if isinstance(tree[1], list):
            # (1) Normalise single non-terminal on the right
            tree[0] = "%s+%s" % (tree[0], tree[1][0])
            tree[1:] = tree[1][1:]
            chomsky_normal_form(tree)
        else:
            if not isinstance(tree[1], string_types):
                raise Exception("Terminal should be a string: %s" % str(tree))
    
    elif n == 3:
        # X -> Y1, Y2
        for i in (1, 2):
            if isinstance(tree[i], string_types):
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


def un_chomsky_normal_form(tree):
    sym = tree[0]
    if len(tree) == 2:
        i = sym.find('+')
        if i != -1:
            # Undo (1)
            tree[0] = sym[:i]
            tree[1] = [sym[i+1:], tree[1]]
            un_chomsky_normal_form(tree)
    else:
        transformed = False
        for i in range(2, len(tree)):
            if sym == tree[i][0]:
                # Undo (3)
                tree[i:i+1] = tree[i][1:]
                transformed = True
        if transformed:
            un_chomsky_normal_form(tree)
        else:
            for t in tree[1:]:
                un_chomsky_normal_form(t)


def null_elements_filter(node):
    if isinstance(node, list):
        n = len(node)
        if n < 2:
            return False
        elif n == 2:
            if '-NONE-' in node[0]:
                return False
    
    return True


class UncertainParsing(Exception):
    pass


def prune_null_elements(tree, parents):
    tree[:] = list(filter(null_elements_filter, tree))
    
    n = len(tree)
    if n < 2:
        prune_null_elements(parents[id(tree)], parents)
    
    else:
        root = tree[0]
        
        if not isinstance(tree[0], string_types):
            import ipdb; ipdb.set_trace()
            raise Exception("Root should be a string: %s" % str(tree))
        
        if root == 'X':
            raise UncertainParsing()
        
        for node in tree[1:]:
            if isinstance(node, list):
                parents[id(node)] = tree
                prune_null_elements(node, parents)


def lower_first_word(tree):
    if len(tree) == 2:
        if is_cap_word(tree[1]):
            tree[1] = tree[1].lower()
    else:
        lower_first_word(tree[1])


def gen_norm(norm_path, input_treebanks):
    with open(norm_path, 'w') as norm:
        for path in input_treebanks:
            for tree in parse_treebank(path):
                try:
                    prune_null_elements(tree, {})
                    chomsky_normal_form(tree)
                    lower_first_word(tree)
                    norm.write(dumps(tree) + '\n')
                except UncertainParsing as e:
                    pass
                except Exception as e:
                    print(e)
                    print('Discarding: %s' % str(tree))
