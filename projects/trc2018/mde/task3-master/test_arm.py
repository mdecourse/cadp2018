# -*- coding: utf-8 -*-

from os import remove
from os.path import isfile
from time import sleep
_com_folder = "communication"
_go_txt = "go.txt"
_end_txt = "end.txt"
com_go = _com_folder + '/' + _go_txt
com_end = _com_folder + '/' + _end_txt


def main():
    while True:
        while not isfile(com_go):
            try:
                sleep(1)
            except KeyboardInterrupt:
                return
        else:
            try:
                remove(com_go)
            except PermissionError:
                pass
            else:
                sleep(5)
                with open(com_end, 'w') as f:
                    f.write("")


if __name__ == '__main__':
    main()
