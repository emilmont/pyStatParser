from os.path import join, dirname, abspath

ROOT = abspath(dirname(__file__))

TREEBANKS_DIR = join(ROOT, "treebanks")
TEMP_DIR = join(ROOT, "temp")

QUESTIONBANK_DIR = join(TREEBANKS_DIR, "QuestionBank")
QUESTIONBANK_DATA = join(QUESTIONBANK_DIR, "4000qs.txt")
QUESTIONBANK_NORM = join(TEMP_DIR, "4000qs.json")

PENNTREEBANK_DIR = join(TREEBANKS_DIR, "PennTreebank")
PENNTREEBANK_GLOB = join(PENNTREEBANK_DIR, "*.mrg")
PENNTREEBANK_NORM = join(TEMP_DIR, "penn_treebank.json")

MODEL = join(TEMP_DIR, 'model.json')
