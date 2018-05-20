import sys

from pycparser import c_parser
from ted import count_distance

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("""python3.7 code_clones.py file1.c another.c""")
        sys.exit(1)

    file1 = open(sys.argv[1], 'r').read()
    file2 = open(sys.argv[2], 'r').read()

    print(type(file1))

    parser = c_parser.CParser()

    original_ast = parser.parse(file1, filename='<none>', debuglevel=0)
    another_ast = parser.parse(file2, filename='<none>', debuglevel=0)

    result = count_distance(original_ast, another_ast)

    if result < 10:
        print("\nCODE IS THE SAME\n")
    else:
        print("\nOK\n")


