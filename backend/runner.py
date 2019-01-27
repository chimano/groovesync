from services import parser
from sys import argv

if __name__ == "__main__":
    if len(argv) < 3:
        print("USAGE: python runner.py <script> <arg3>")
    if argv[1] == "parser" and len(argv) == 3:
        parser.main(argv[2])
