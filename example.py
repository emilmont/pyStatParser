from stat_parser.parser import Parser
from json import dumps


if __name__ == '__main__':
    parser = Parser()
    print parser.parse("Who leads the star ship Enterprise in Star Trek ?")
