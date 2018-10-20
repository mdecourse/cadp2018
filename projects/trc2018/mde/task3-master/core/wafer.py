# -*- coding: utf-8 -*-


class WaferData:

    """Wafer data structure."""

    def __init__(
        self,
        cass_a_id: int,
        cass_b_id: int,
        chamber_a_time: int,
        order: int,
    ):
        self.__cass_a_id = cass_a_id
        self.__cass_b_id = cass_b_id
        self.__chamber_a_time = chamber_a_time
        self.__pos = "CassA"
        self.__status = 0
        self.__order = order

    @property
    def cass_a_id(self) -> int:
        """CassA ID."""
        return self.__cass_a_id

    @property
    def cass_b_id(self) -> int:
        """CassB ID."""
        return self.__cass_b_id

    @property
    def chamber_a_time(self) -> int:
        """Chamber A time."""
        return self.__chamber_a_time

    @property
    def status(self) -> int:
        """Wafer checking status."""
        return self.__status

    @property
    def order(self) -> int:
        """Order of table widget."""
        return self.__order

    @property
    def pos(self) -> str:
        """Current position."""
        if self.__pos == "CassA":
            return self.__pos + f"-{self.cass_a_id:02d}"
        elif self.__pos == "CassB":
            return self.__pos + f"-{self.cass_b_id:02d}"
        else:
            return self.__pos

    def set_pos(self, pos: str):
        """Set position."""
        self.__pos = pos.split('-')[0]

    def complete(self):
        """Add 1 completed status."""
        self.__status += 1

    def is_completed(self) -> bool:
        """Return True if status is completed."""
        return self.__status == 2

    def fail(self):
        """Set status to failed."""
        self.__status = -1

    def reply(self, w_id: int) -> str:
        """Return command."""
        return (
            f"~Ack,CreateJob,W{w_id:02d},CassA-{self.cass_a_id:02d};"
            f"A:{self.chamber_a_time:d};"
            f"B|D:Endpoint;"
            f"E|F:Endpoint;"
            f"C:Inspection;"
            f"CassB-{self.cass_b_id:02d}@"
        )
