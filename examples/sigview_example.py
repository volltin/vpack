from vpack import sigview
sigview.enable()

import time

def main():
    while True:
        print('1')
        time.sleep(1)
        print('2')
        time.sleep(2)

if __name__ == '__main__':
    main()
