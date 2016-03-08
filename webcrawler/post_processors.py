from abc import ABCMeta, abstractmethod


class BasePostProcessor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, item):
        pass
