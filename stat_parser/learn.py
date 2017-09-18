from __future__ import print_function
from os.path import exists
from glob import glob
from os import makedirs
from json import loads
from time import time

from stat_parser.treebanks.parse import normalize_questionbank
from stat_parser.treebanks.normalize import gen_norm
from stat_parser.treebanks.extract import get_sentence
from stat_parser.pcfg import PCFG

from stat_parser.paths import QUESTIONBANK_NORM, QUESTIONBANK_DATA, QUESTIONBANK_PENN_DATA
from stat_parser.paths import PENNTREEBANK_NORM, PENNTREEBANK_GLOB
from stat_parser.paths import TEMP_DIR, MODEL_TREEBANK, MODEL
from stat_parser.paths import TEST_DAT, TEST_KEY


def build_model():
    pcfg = PCFG()
    if exists(MODEL):
        pcfg.load_model(MODEL)
    
    else:
        print("Building the Grammar Model")
        start = time()
        
        if not exists(TEMP_DIR):
            makedirs(TEMP_DIR)
        
        # Normalise the treebanks
        if not exists(QUESTIONBANK_NORM):
            normalize_questionbank(QUESTIONBANK_DATA, QUESTIONBANK_PENN_DATA)
            gen_norm(QUESTIONBANK_NORM, [QUESTIONBANK_PENN_DATA])
        
        if not exists(PENNTREEBANK_NORM):
            gen_norm(PENNTREEBANK_NORM, glob(PENNTREEBANK_GLOB))
        
        # Keep a part of the treebanks for testing
        i = 0
        with open(MODEL_TREEBANK, 'w') as model, open(TEST_DAT, 'w') as dat, open(TEST_KEY, 'w') as key:
            for treebank in [QUESTIONBANK_NORM, PENNTREEBANK_NORM]:
                for tree in open(treebank):
                    i += 1
                    if (i % 100) == 0:
                        sentence, n = get_sentence(loads(tree))
                        if n > 7 and n < 20:
                            dat.write(sentence+'\n')
                            key.write(tree)
                        else:
                            i -= 1
                    
                    model.write(tree)
        
        # Learn PCFG
        pcfg.learn_from_treebanks([MODEL_TREEBANK])
        pcfg.save_model(MODEL)
        print("Time: (%.2f)s\n" % (time() - start))
    
    return pcfg
