import abc
from typing import Any
from typing import Callable
from typing import Dict
from typing import List


class BaseJournalLogStorage(abc.ABC):
    """Base class for Journal storages.

    Storage classes implementing this base class must guarantee process safety. This means,
    multiple processes might concurrently call ``read_logs`` and ``append_logs``. If the
    backend storage does not internally support mutual exclusion mechanisms, such as locks,
    you might want to use :class:`~optuna.storages.JournalFileSymlinkLock` or
    :class:`~optuna.storages.JournalFileOpenLock` for creating a critical section.

    """

    @abc.abstractmethod
    def read_logs(self, log_number_from: int) -> List[Dict[str, Any]]:
        """Read logs with a log number greater than or equal to ``log_number_from``.

        If ``log_number_from`` is 0, read all the logs.

        Args:
            log_number_from:
                A non-negative integer value indicating which logs to read.

        Returns:
            Logs with log number greater than or equal to ``log_number_from``.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def append_logs(self, logs: List[Dict[str, Any]]) -> None:
        """Append logs to the backend.

        Args:
            logs:
                A list that contains json-serializable logs.
        """

        raise NotImplementedError


class SnapshotRestoreError(Exception):
    """Exception for BaseJournalLogSnapshot."""

    pass


class BaseJournalLogSnapshot(abc.ABC):
    """Optional base class for Journal storages.

    Storage classes implementing this base class may work faster when
    constructing the internal state from the large amount of logs.

    Args:
        snapshot_interval: An interval of trials and studies to save a snapshot.
    """

    def __init__(self, snapshot_interval: int) -> None:

        self.snapshot_interval = snapshot_interval

    @abc.abstractmethod
    def save_snapshot(self, snapshot: bytes) -> None:
        """Save snapshot to the backend.

        Args:
            snapshot: A serialized snapshot (bytes)
        """
        raise NotImplementedError

    @abc.abstractmethod
    def load_snapshot(self, loader: Callable[[bytes], None]) -> None:
        """Load snapshot from the backend.

        Args:
            loader: A callback function which accept one positional argument.
                This callback is supposed to be called inside the
                :meth:`~optuna.storages._journal.base.BaseJournalLogSnapshot.load_snapshot`
                method.
                This callback may raise :class:`optuna.storages._journal.base.SnapshotRestoreError`
                when a serialized snapshot object is invalid or broken.
        """
        raise NotImplementedError
