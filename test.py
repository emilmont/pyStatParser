from json import loads
from time import time

from stat_parser.paths import TEST_DAT, TEST_KEY
from stat_parser.parser import Parser
from stat_parser.eval_parser import ParseEvaluator


if __name__ == '__main__':
    start = time()
    parser = Parser()
    evaluator = ParseEvaluator()
    for key, dat in zip(open(TEST_KEY), open(TEST_DAT)):
        tree = None
        try:
            tree = parser.parse(dat)
            evaluator.check_trees(loads(key), tree)
        except Exception, e:
            print '\nparsed: {%s}' % (tree)
            print 'key   : {%s}' % (key)
            print e
    
    evaluator.output()
    
    print '\nCompleted in (%d)sec' % (time() - start)
