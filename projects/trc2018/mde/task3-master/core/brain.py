# -*- coding: utf-8 -*-

from typing import Sequence, Dict
from core.QtModules import pyqtSignal, QThread
from core import main as mn
from core.wafer import WaferData


class BrainThread(QThread):

    """Workflow thread. We call it brain."""

    mv_wafer = pyqtSignal(int, str)
    finish = pyqtSignal()

    def __init__(self, parent: 'mn.MainWindow'):
        super(BrainThread, self).__init__()
        self.wafers = parent.wafers
        self.stations: Dict[str, int] = {}
        self.wafer_moving = parent.wafer_moving
        self.__stop = False

    def set_stations(self, stations: Sequence[str]):
        """Set station names."""
        for station in stations:
            self.stations[station] = 0

    def run(self):
        """Planing the workflow."""
        self.__stop = False

        while not self.__is_all_done():

            if self.__stop:
                return

            # Pick a wafer.
            for w_id, wafer in self.wafers.items():

                # Find the way.
                s_to = self.__movable_check(wafer)

                # I'm busy.
                if not s_to:
                    continue

                # Finally picked a wafer.
                c_id = w_id
                c_wafer = wafer
                c_to = s_to
                break
            else:
                continue

            # Arm should be free.
            if self.wafer_moving():
                continue

            # Move wafer.
            self.mv_wafer.emit(c_id, c_to)
            if c_wafer.pos in self.stations:
                self.stations[c_wafer.pos] = 0
            if c_to in self.stations:
                self.stations[c_to] = c_id
            self.msleep(500)

        # All finished.
        self.finish.emit()

    def __movable_check(self, wafer: WaferData) -> str:
        """Check wafer if it can move, return next position.

        Status:
        + 0: CassA
        + 1: A
        + 2 or -1: B or D
        + 3 or -1: E or F
        + 4: C
        """
        if wafer.status == 0 and wafer.pos.startswith('CassA'):
            if self.stations['A'] == 0:
                return 'A'
            else:
                return ''

        elif wafer.status == 1 and wafer.pos == 'A':
            if self.stations['B'] == 0:
                return 'B'
            elif self.stations['D'] == 0:
                return 'D'
            return ''

        elif wafer.status == 2 and wafer.pos in {'B', 'D'}:
            if self.stations['E'] == 0:
                return 'E'
            elif self.stations['F'] == 0:
                return 'F'
            return ''

        elif wafer.status == 3 and wafer.pos in {'E', 'F'}:
            if self.stations['C'] == 0:
                return 'C'
            else:
                return ''

        elif wafer.status == 4 and wafer.pos == 'C':
            return 'CassB'

        elif wafer.status == -1 and not wafer.pos.startswith('CassA'):
            return 'CassA'

    def __is_all_done(self) -> bool:
        """Check all wafer."""
        for wafer in self.wafers.values():
            if wafer.status == -1:
                if not wafer.pos.startswith('CassA'):
                    return False
            elif wafer.status == 4:
                if not wafer.pos.startswith('CassB'):
                    return False
            else:
                return False
        return True

    def stop_thinking(self):
        """Let the brain stop."""
        self.__stop = True
