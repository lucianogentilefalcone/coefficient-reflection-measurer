from abc import ABC, abstractmethod


class Plot(ABC):
    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def set_axis_limits(self, **kwargs):
        pass

    @abstractmethod
    def plot(self, **kwargs):
        pass

    @property
    @abstractmethod
    def started(self, *args):
        pass
