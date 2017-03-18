import sys


def readfile(filename):
    f = open(filename)
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        print(line)
    f.close()

    if len(sys.argv) < 2:
        print('no action detect.')
        sys.exit()
    if sys.argv[1].startwith('--'):
        option = sys.argv[1][2:]
        if option == 'version':
            print('version 1.2')
        elif option == 'help':
            print('...')
        else:
            print('unkonwn option')
        sys.exit()
    else:
        for filename in sys.argv[1]:
            readfile(filename)
