from abc import ABCMeta, abstractproperty, abstractmethod


class BaseSpider(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def domains(self):
        pass

    @abstractproperty
    def start_urls(self):
        pass

    @abstractmethod
    def parse(self, response):
        pass


class CrawlSpider(BaseSpider):
    pass
