# -*- coding: utf-8 -*-

from .QtModules import (
    QApplication,
)
from .main import MainWindow

__all__ = ['startup']


def startup():
    app = QApplication([])
    run = MainWindow()
    run.show()
    exit(app.exec_())
