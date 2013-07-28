pyStatParser
============

Simple Python statistical (CKY) parser together with scripts for learning the PCFG from the QuestionBank and Penn treebanks.

```python
>>> from stat_parser import Parser
>>> parser = Parser()
>>> print parser.parse("How can the net amount of entropy of the universe be massively decreased?")
(SBARQ
  (WHADVP (WRB how))
  (SQ
    (MD can)
    (NP
      (NP (DT the) (JJ net) (NN amount))
      (PP
        (IN of)
        (NP
          (NP (NNS entropy))
          (PP (IN of) (NP (DT the) (NN universe))))))
    (VP (VB be) (ADJP (RB massively) (VBN decreased))))
  (. ?))
```
