# -*- coding: utf-8 -*-

from typing import Sequence, Callable
from threading import Thread
from core.QtModules import (
    pyqtSignal,
    QThread,
    QWidget,
)
from .colorfilterdefect import image_detect

__all__ = ['ImageThread']


class ImageThread(QThread):

    """Image inspection thread."""

    receive = pyqtSignal(str)
    finish = pyqtSignal()

    def __init__(self, request: Sequence[str], parent: QWidget):
        super(ImageThread, self).__init__(parent)
        self.request = request
        self.receive_list = []

    def run(self):
        """Image thread."""
        threads = []
        for file_name in self.request:
            thread = Thread(target=self.__mini_thread(file_name))
            threads.append(thread)
            thread.start()

        count = 0
        while count != len(self.request):
            if self.receive_list:
                self.receive.emit(self.receive_list.pop(0))
                count += 1
            self.msleep(500)
        self.finish.emit()

    def __mini_thread(self, file_name: str) -> Callable[[], None]:
        """Create mini thread function."""

        def func():
            points = image_detect(f"images/{file_name}")
            p_str = '|'.join(f"{x}_{y}" for x, y in points)
            if p_str:
                p_str = ',' + p_str
            self.receive_list.append(
                "~Evt,InspectionCompleted,"
                f"{file_name},{len(points)}{p_str}@"
            )

        return func
