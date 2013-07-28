from json import loads
from time import time

from stat_parser.paths import TEST_DAT, TEST_KEY
from stat_parser.parser import Parser
from stat_parser.eval_parser import ParseEvaluator


if __name__ == '__main__':
    parser = Parser()
    evaluator = ParseEvaluator()
    
    start = time()
    for key, dat in zip(open(TEST_KEY), open(TEST_DAT)):
        tree = None
        try:
            tree = parser.norm_parse(dat)
            evaluator.check_trees(loads(key), tree)
        except Exception, e:
            print '\nparsed: {%s}' % (tree)
            print 'key   : {%s}' % (key.strip())
            print e
    evaluator.output()
    print '\nCompleted in (%.2f)sec' % (time() - start)
