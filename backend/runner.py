from services import parser, search, TTinfo
from sys import argv

if __name__ == "__main__":
    if len(argv) < 2:
        print("USAGE: python runner.py <script> <arg3>")
        exit(1)
    main = None
    if argv[1] == "parser" and len(argv) == 3:
        main = parser.main
    elif argv[1] == "TTinfo" and len(argv) == 4:
        main = TTinfo.main
    elif argv[1] == "search" and len(argv) == 2:
        main = search.main
    else:
        print("Could not find specified module with specified arguments")
        exit(1)
    main(argv[2:])
