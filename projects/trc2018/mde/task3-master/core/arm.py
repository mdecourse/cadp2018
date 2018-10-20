# -*- coding: utf-8 -*-

from os import mkdir, remove
from os.path import isdir, isfile
from core.QtModules import pyqtSignal, QThread, QWidget
from core.g_code import gcd
_com_folder: str = "communication" #gcd['location']
_go_txt = "go.txt"
_end_txt = "end.txt"
com_go = _com_folder + '/' + _go_txt
com_end = _com_folder + '/' + _end_txt

__all__ = ['com_go', 'com_end', 'ArmThread']


class ArmThread(QThread):

    """File detection thread."""

    finish = pyqtSignal()

    def __init__(self, g_code: str, parent: QWidget):
        super(ArmThread, self).__init__(parent)
        self.g_code = g_code

    def run(self):
        """Create file and detect file to communicate."""
        if not isdir(_com_folder):
            mkdir(_com_folder)
        with open(com_go, 'w') as f:
            f.write(self.g_code)

        while not isfile(com_end):
            self.sleep(1)
        else:
            remove(com_end)
            self.finish.emit()
