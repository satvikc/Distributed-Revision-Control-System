#! /usr/bin/python

from optparse import OptionParser

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)

    parser.add_option("-i", "--init", help = "Initialize the repo",
                      action="store_true", dest="init")

    parser.add_option("-c", "--commit", dest="commit",
                      help="commit the required changes")

    (options, args) = parser.parse_args()

    if options.init:
        print("Initializing repo")
    elif options.commit:
        print("Commiting with message " + options.commit)


if __name__ == "__main__":
    main()
