# -*- coding: utf-8 -*-

from typing import Dict, Callable
from time import time
from core.QtModules import (
    pyqtSlot,
    Qt,
    QMainWindow,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QTableWidgetItem,
    QSleepThread,
    QMessageBox,
)
from numpy import (
    zeros as np_zeros,
    int8 as np_int8,
    float16 as np_float16,
)
from core.connection import Socket
from core.arm import ArmThread, com_end
from core.brain import BrainThread
from core.wafer import WaferData
from core.g_code import generate_g_code
from core.colorfilterdefect import ImageThread
from .Ui_main import Ui_MainWindow
_chambers = ('B', 'D', 'E', 'F')
_stations = ('A', 'B', 'C', 'D', 'E', 'F')


class MainWindow(QMainWindow, Ui_MainWindow):

    """Main window."""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Socket 5000
        self.socket_1 = Socket()
        self.socket_1.receive.connect(self.console_1.append)
        self.socket_1.receive.connect(self.__command_detect)
        self.socket_1.receive.connect(self.__arm_detect)
        # Socket 6000
        self.socket_2 = Socket()
        self.socket_2.receive.connect(self.__data_detect)

        # Wafers.
        self.wafers: Dict[int, WaferData] = {}
        self.wafer_table.setColumnCount(3)

        # Wafer movement command.
        self.mv_w_id = 0
        self.s_from = ""
        self.s_to = ""
        self.__wafer_moving = False

        # Send button.
        self.text_option.returnPressed.connect(self.send_button.click)

        def test_button_func(name_str: str) -> Callable[[], None]:
            """Test button function."""
            @pyqtSlot()
            def t_func():
                self.socket_1.send(f"~Evt,ChamberStart,{name_str}@")
            return t_func

        # Test button
        self.chamber_func: Dict[str, Callable[[], None]] = {}
        for name in _stations:
            button = QPushButton(f"Test Chamber {name}", self)
            self.chamber_func[name] = test_button_func(name)
            button.clicked.connect(self.chamber_func[name])
            self.test_button_layout.addWidget(button)

        # Win in, win out.
        self.win_out = np_zeros(4, dtype=np_int8)
        self.win_in = np_zeros(4, dtype=np_int8)
        self.data_start = np_zeros(4, dtype=np_float16)
        self.time_start = np_zeros(4, dtype=np_float16)
        self.time_min = np_zeros(4, dtype=np_float16)
        self.time_max = np_zeros(4, dtype=np_float16)
        self.win_height = np_zeros(4, dtype=np_float16)
        self.win_time = np_zeros(4, dtype=np_float16)
        self.win_out_limit = np_zeros(4, dtype=np_float16)
        self.win_in_limit = np_zeros(4, dtype=np_float16)

        # Win in, win out table widget.
        for i in range(4):
            for j in range(2):
                spinbox = QSpinBox()
                spinbox.setEnabled(False)
                self.data_limit_table.setCellWidget(i, j, spinbox)

            double_spinbox = QDoubleSpinBox()
            double_spinbox.setEnabled(False)
            self.data_limit_table.setCellWidget(i, 2, double_spinbox)

        # Brain thread.
        self.brain = BrainThread(self)
        self.brain.mv_wafer.connect(self.__mv_wafer)
        self.brain.finish.connect(self.__finished)

        # Time
        self.t0 = 0.

        # Reset.
        self.clear()

    @pyqtSlot(name='on_stop_auto_mode_button_clicked')
    def __stop_thinking(self):
        """Stop thinking."""
        # Stop the brain.
        self.brain.stop_thinking()
        self.auto_mode_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.stop_auto_mode_button.setEnabled(False)

    @pyqtSlot(name='on_reset_button_clicked')
    def clear(self):
        """Clear all data."""
        # Wafers.
        self.wafers.clear()
        self.wafer_table.setRowCount(0)

        # Wafer movement command.
        self.mv_w_id = 0
        self.s_from = ""
        self.s_to = ""
        self.__wafer_moving = False
        self.mv_counter.setValue(0)

        # Win in, win out.
        for data in (
            self.win_out,
            self.win_in,
            self.data_start,
            self.time_start,
            self.time_min,
            self.time_max,
            self.win_height,
            self.win_time,
            self.win_out_limit,
            self.win_in_limit,
        ):
            for i in range(len(data)):
                data[i] = 0

        # Win in, win out table widget.
        for i in range(4):
            for j in range(3):
                self.data_limit_table.cellWidget(i, j).setValue(0)

        # Consoles.
        self.console_1.clear()
        self.console_2.clear()

    def wafer_moving(self) -> bool:
        """Return True if a wafer is on the road."""
        return self.__wafer_moving

    @pyqtSlot()
    def __finished(self):
        """Finished."""
        self.socket_1.send("~Evt,ProcessCompleted@")
        QMessageBox.information(
            self,
            "Process Completed",
            f"Completed time: {time() - self.t0}"
        )

    def __wafer_completed(self, wafer: WaferData):
        """Set and update wafer when completed."""
        wafer.complete()
        self.wafer_table.item(wafer.order, 2).setText(f"{wafer.status}")
        self.wafer_table.viewport().repaint()

    def __wafer_failed(self, wafer: WaferData):
        """Set and update wafer when failed."""
        wafer.fail()
        self.wafer_table.item(wafer.order, 2).setText(f"{wafer.status}")
        self.wafer_table.viewport().repaint()

    @pyqtSlot(name='on_connect_button_clicked')
    def __connect(self):
        """Connect to address."""
        self.socket_1.connect(self.ip_option.text(), self.port_1.value())
        self.socket_1.start()
        self.socket_2.connect(self.ip_option.text(), self.port_2.value())
        self.socket_2.start()

    @pyqtSlot(name='on_disconnect_button_clicked')
    def __disconnect(self):
        """Disconnect from address."""
        self.socket_1.close()
        self.socket_2.close()
        self.__stop_thinking()

    @pyqtSlot(name='on_send_button_clicked')
    def __send(self):
        """Send text."""
        self.socket_1.send(self.text_option.text())
        self.text_option.clear()

    @pyqtSlot(name='on_auto_mode_button_clicked')
    def __auto_mode_startup(self):
        """Start auto mode."""
        self.auto_mode_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.stop_auto_mode_button.setEnabled(True)
        self.t0 = time()
        self.brain.set_stations(_stations)
        self.brain.start()

    @pyqtSlot(str)
    def __command_detect(self, command: str):
        """Detect main command.

        + Create wafer. (wafers)
        + Process start.
        + Chamber start.
        + Image inspection.
        """
        # Create wafer.
        if command.startswith("~Cmd,CreateJob,"):
            c = command[len("~Cmd,CreateJob,"):-1].split(';')
            p1 = c[0].split(',')
            w_id = int(p1[0][-2:])
            wafer = WaferData(
                cass_a_id=int(p1[1][-2:]),
                cass_b_id=int(c[5][-2:]),
                chamber_a_time=int(c[1][2:]),
                order=len(self.wafers),
            )
            self.wafers[w_id] = wafer
            self.mv_w_id_option.addItem(f"{w_id}")
            self.wafer_table.insertRow(self.wafer_table.rowCount())
            flags_readonly = Qt.ItemIsSelectable | Qt.ItemIsEnabled
            item_0 = QTableWidgetItem(f"W{w_id:02d}")
            item_0.setFlags(flags_readonly)
            self.wafer_table.setItem(wafer.order, 0, item_0)
            item_1 = QTableWidgetItem(wafer.pos)
            item_1.setFlags(flags_readonly)
            self.wafer_table.setItem(wafer.order, 1, item_1)
            item_2 = QTableWidgetItem(f"{wafer.status}")
            item_2.setFlags(flags_readonly)
            self.wafer_table.setItem(wafer.order, 2, item_2)
            self.socket_1.send(wafer.reply(w_id))

        # Process start.
        elif command == "~Cmd,ProcessStart@":
            self.socket_1.send("~Ack,ProcessStart@")
            if self.auto_mode_startup_option.isChecked():
                self.__auto_mode_startup()

        # Any chamber start.
        elif command.startswith("~Ack,ChamberStart,"):
            c = command[len("~Ack,ChamberStart,"):-1].split(',')
            if c[0] == 'A':
                for wafer in self.wafers.values():
                    if wafer.pos == 'A':
                        c_wafer = wafer
                        w_time = wafer.chamber_a_time
                        break
                else:
                    return

                @pyqtSlot()
                def func():
                    self.__wafer_completed(c_wafer)
                    self.socket_1.send("~Evt,ChamberCompleted,A@")

                thread = QSleepThread(w_time, self)
                thread.finish.connect(func)
                thread.start()

            elif c[0] in _chambers:
                i = _chambers.index(c[0])
                time_min, time_max = c[1].split('-')
                self.time_min[i] = float(time_min)
                self.time_max[i] = float(time_max)
                self.win_height[i] = float(c[2])
                self.win_time[i] = float(c[3])
                self.win_out_limit[i] = int(c[4])
                self.win_in_limit[i] = int(c[5])

        # A test of chamber has been started automatically.
        elif command.startswith("~Ack,PutWaferCompleted,"):
            self.__wafer_moving = False
            station = command[len("~Ack,PutWaferCompleted,"):-1].split(',')[1]
            if station in _stations:
                self.chamber_func[station]()

        # Image inspection.
        elif command.startswith("~Cmd,Inspection,"):
            self.socket_1.send("~Ack," + command.split(',', maxsplit=1)[1])
            images = command[len("~Cmd,Inspection,"):-1].split(',')
            counter_thread = ImageThread(images, self)
            counter_thread.receive.connect(self.socket_1.send)
            counter_thread.finish.connect(self.__image_completed)
            counter_thread.start()

    @pyqtSlot(name='on_virtual_reply_button_clicked')
    def __virtual_reply(self):
        """Virtual reply."""
        with open(com_end, 'w') as f:
            f.write("")

    @pyqtSlot(name='on_mv_w_button_clicked')
    def __mv_wafer_manual(self):
        """Move a wafer (manual)."""
        try:
            w_id = int(self.mv_w_id_option.currentText())
        except ValueError:
            return
        else:
            self.__mv_wafer(w_id, self.to_option.currentText())

    @pyqtSlot(int, str)
    def __mv_wafer(self, w_id: int, s_to: str):
        """Move a wafer."""
        self.console_2.append(f"W{w_id:02d} -> {s_to}")
        self.mv_counter.setValue(self.mv_counter.value() + 1)
        wafer = self.wafers[w_id]

        if s_to == 'CassA':
            s_to += f"-{wafer.cass_a_id:02d}"
        elif s_to == 'CassB':
            s_to += f"-{wafer.cass_b_id:02d}"

        self.s_from = wafer.pos
        self.s_to = s_to
        self.mv_w_id = w_id
        self.__wafer_moving = True
        self.socket_1.send(f"~Evt,GetWaferStart,W{self.mv_w_id:02d},{self.s_from}@")

    @pyqtSlot(str)
    def __arm_detect(self, command: str):
        """Arm function.

        Arguments:
        + self.mv_w_id
        + self.s_from
        + self.s_to

        Action:
        + Get wafer start.
        + Get wafer completed.
        + Put wafer start.
        + Put wafer completed.
        """

        if self.mv_w_id == 0:
            return

        if command.startswith("~Ack,GetWaferStart,"):
            # TODO: G code here.

            @pyqtSlot()
            def func():
                self.socket_1.send(f"~Evt,GetWaferCompleted,W{self.mv_w_id:02d},{self.s_from}@")

            thread = ArmThread(generate_g_code(self.s_from, True), self)
            thread.finish.connect(func)
            thread.start()

        elif command.startswith("~Ack,GetWaferCompleted,"):
            self.wafer_table.item(self.wafers[self.mv_w_id].order, 1).setText("Robot")
            self.socket_1.send(f"~Evt,PutWaferStart,W{self.mv_w_id:02d},{self.s_to}@")

        elif command.startswith("~Ack,PutWaferStart,"):

            @pyqtSlot()
            def func():
                self.wafers[self.mv_w_id].set_pos(self.s_to)
                self.wafer_table.item(self.wafers[self.mv_w_id].order, 1).setText(self.s_to)
                self.wafer_table.viewport().repaint()
                self.socket_1.send(f"~Evt,PutWaferCompleted,W{self.mv_w_id:02d},{self.s_to}@")

            thread = ArmThread(generate_g_code(self.s_to, False), self)
            thread.finish.connect(func)
            thread.start()

    @pyqtSlot(str)
    def __data_detect(self, command: str):
        """Detect data. (Win in, Win out)"""
        data_table = []
        for data in command[len("~Data,"):-1].split(','):
            data, d_time = data.replace('(', ',').replace(')', '').split(',')
            # TODO: Check about split error string '0@~Data'
            try:
                data_table.append((float(data), float(d_time)))
            except ValueError:
                data_table.append((0., 0.))

        if len(data_table) != 4:
            return

        for i, (data, d_time) in enumerate(data_table):
            out_widget: QSpinBox = self.data_limit_table.cellWidget(i, 0)
            in_widget: QSpinBox = self.data_limit_table.cellWidget(i, 1)
            time_widget: QDoubleSpinBox = self.data_limit_table.cellWidget(i, 2)

            if data == 0:
                self.win_out[i] = 0
                self.win_in[i] = 0
                self.data_start[i] = 0
                self.time_start[i] = 0
                out_widget.setValue(0)
                in_widget.setValue(0)
                time_widget.setValue(0)
                continue

            for wafer in self.wafers.values():
                if wafer.pos == _chambers[i]:
                    c_wafer = wafer
                    break
            else:
                continue

            time_widget.setValue(d_time)

            if d_time == 0.1:
                self.data_start[i] = data

            if d_time > self.time_max[i]:
                self.__wafer_failed(c_wafer)
                self.socket_1.send(f"~Evt,ChamberAlarm,{_chambers[i]},NA@")
                continue

            # Win out
            if data <= (self.data_start[i] - self.win_height[i] / 2):
                self.win_out[i] += 1
                out_widget.setValue(self.win_out[i])

                if self.win_out[i] >= self.win_out_limit[i] and (self.win_in_limit[i] == 0):
                    if d_time < self.time_min[i]:
                        status = 'ChamberAlarm'
                        self.__wafer_failed(c_wafer)
                    else:
                        status = 'Completed'
                        self.__wafer_completed(c_wafer)
                    self.socket_1.send(f"~Evt,Chamber{status},{_chambers[i]},{d_time}@")

                self.data_start[i] = data
                self.time_start[i] = d_time

            # Win in
            elif d_time >= (self.time_start[i] + self.win_time[i]):
                # Start counting if win out is over.
                if self.win_out[i] >= self.win_out_limit[i]:
                    self.win_in[i] += 1
                    in_widget.setValue(self.win_in[i])
                    # Win in over.
                    if self.win_in[i] >= self.win_in_limit[i]:
                        if d_time < self.time_min[i]:
                            status = 'ChamberAlarm'
                            self.__wafer_failed(c_wafer)
                        else:
                            status = 'Completed'
                            self.__wafer_completed(c_wafer)
                        self.socket_1.send(f"~Evt,Chamber{status},{_chambers[i]},{d_time}@")

                self.data_start[i] = data
                self.time_start[i] = d_time

    @pyqtSlot()
    def __image_completed(self):
        """Image completed function."""
        self.socket_1.send("~Evt,ChamberCompleted,C@")
        for wafer in self.wafers.values():
            if wafer.pos == 'C':
                c_wafer = wafer
                break
        else:
            return
        self.__wafer_completed(c_wafer)

    def closeEvent(self, event):
        """Close sockets."""
        self.__disconnect()
