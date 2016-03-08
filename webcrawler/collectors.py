from abc import ABCMeta, abstractmethod


class BaseCollector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def clean(self, item):
        pass
