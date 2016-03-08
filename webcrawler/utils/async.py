import workerpool


class SimpleCrawlJob(workerpool.Job):
    def __init__(self, target, kwargs):
        self.target = target
        self.kwargs = kwargs

    def run(self):
        self.target(**self.kwargs)
