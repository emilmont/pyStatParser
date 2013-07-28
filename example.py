from stat_parser.parser import Parser, nltk_installed


parser = Parser()

# http://www.thrivenotes.com/the-last-question/
tree = parser.parse("How can the net amount of entropy of the universe be massively decreased?")

if nltk_installed:
    tree.draw()
else:
    print tree
