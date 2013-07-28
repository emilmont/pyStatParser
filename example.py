from stat_parser import Parser, display_tree


parser = Parser()

# http://www.thrivenotes.com/the-last-question/
tree = parser.parse("How can the net amount of entropy of the universe be massively decreased?")

display_tree(tree)
