from os.path import exists
from glob import glob
from os import makedirs

from stat_parser.treebanks.normalize import gen_norm
from stat_parser.pcfg import PCFG

from stat_parser.paths import QUESTIONBANK_NORM, QUESTIONBANK_DATA
from stat_parser.paths import PENNTREEBANK_NORM, PENNTREEBANK_GLOB
from stat_parser.paths import TEMP_DIR, MODEL


def build_model():
    pcfg = PCFG()
    if exists(MODEL):
        pcfg.load_model(MODEL)
    
    else:
        print "Building the grammar model for the first time..."
        if not exists(TEMP_DIR):
            makedirs(TEMP_DIR)
        
        # Normalise the treebanks
        if not exists(QUESTIONBANK_NORM):
            gen_norm(QUESTIONBANK_NORM, [QUESTIONBANK_DATA])
        
        if not exists(PENNTREEBANK_NORM):
            gen_norm(PENNTREEBANK_NORM, glob(PENNTREEBANK_GLOB))
        
        # Learn PCFG
        pcfg.learn_from_treebanks([QUESTIONBANK_NORM, PENNTREEBANK_NORM])
        pcfg.save_model(MODEL)
    
    return pcfg
