from abc import ABCMeta, abstractmethod


class MonitoredDeviceStatusInterface(metaclass=ABCMeta):
    @abstractmethod
    def heart_beat(self):
        """called periodically. device status then needs to see
            if device is still considered alive or not
        """

    @property
    @abstractmethod
    def usable(self):
        pass


class MonitoredDeviceWithPlanesStatusInterface(metaclass=ABCMeta):
    @property
    @abstractmethod
    def enabled_x(self):
        pass

    @property
    @abstractmethod
    def enabled_y(self):
        pass

