import sys
import opengita

def main():
    args = sys.argv[1:]
    if not args:
        print_usage()
        sys.exit(0)
        
    cmd = args[0].lower()
    if cmd == "random":
        print(opengita.get_random_verse())
    elif cmd == "today":
        print(opengita.today())
    elif cmd == "verse":
        if len(args) < 3:
            print("Error: Please specify chapter and verse numbers. Example: opengita verse 2 47")
            sys.exit(1)
        try:
            ch = int(args[1])
            v = int(args[2])
            print(opengita.get_verse(ch, v))
        except ValueError:
            print("Error: Chapter and verse must be integers.")
            sys.exit(1)
    elif cmd == "chapter":
        if len(args) < 2:
            print("Error: Please specify chapter number. Example: opengita chapter 2")
            sys.exit(1)
        try:
            ch = int(args[1])
            print(opengita.get_chapter(ch))
        except ValueError:
            print("Error: Chapter number must be an integer.")
            sys.exit(1)
    elif cmd == "search":
        if len(args) < 2:
            print("Error: Please specify a keyword to search. Example: opengita search karma")
            sys.exit(1)
        keyword = " ".join(args[1:])
        print(opengita.search(keyword))
    elif ":" in cmd:
        try:
            parts = cmd.split(":")
            ch = int(parts[0])
            v = int(parts[1])
            print(opengita.get_verse(ch, v))
        except ValueError:
            print_usage()
            sys.exit(1)
    else:
        print_usage()
        sys.exit(1)

def print_usage():
    print("""OpenGita - Modern Python SDK for Bhagavad Gita

Usage:
  opengita random             Get a formatted random verse
  opengita today              Get today's verse
  opengita verse <ch> <v>     Get a specific verse
  opengita chapter <ch>       Get chapter details
  opengita search <keyword>   Search verses
""")
