from __future__ import print_function
from json import loads
from time import time
from multiprocessing import Process, JoinableQueue, cpu_count
from threading import Thread
from six.moves import range, zip

from stat_parser.paths import TEST_DAT, TEST_KEY
from stat_parser.parser import Parser
from stat_parser.eval_parser import ParseEvaluator


def test_process(parser, sentences, parsed):
    while True:
        key, sent = sentences.get()
        tree = parser.norm_parse(sent)
        parsed.put((key, tree))
        sentences.task_done()


class Evaluator(Thread):
    def __init__(self, parsed):
        Thread.__init__(self)
        self.results = ParseEvaluator()
        self.parsed = parsed
        
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            key, tree = self.parsed.get()
            try:
                self.results.check_trees(loads(key), tree)
            except Exception as e:
                print('\nparsed: {%s}' % (tree))
                print('key   : {%s}' % (key.strip()))
                print(e)
            self.parsed.task_done()


def test():
    parser = Parser()
    sentences = JoinableQueue()
    parsed = JoinableQueue()
    
    # Parsers Processes consuming sentences
    for _ in range(cpu_count()):
        p = Process(target=test_process, args=(parser, sentences, parsed))
        p.daemon = True
        p.start()
    
    # Evaluator Thread consuming parsed trees
    evaluator = Evaluator(parsed)
    start = time()
    for key, sent in zip(open(TEST_KEY), open(TEST_DAT)):
        sentences.put((key, sent))
    
    # Wait completion
    sentences.join()
    parsed.join()
    evaluator.results.output()
    print('\nCompleted in (%.2f)sec' % (time() - start))


if __name__ == '__main__':
    test()
