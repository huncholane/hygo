import logging


class ReverseTruncateHandler(logging.FileHandler):
    def __init__(self, filename, num_lines=100, **kwargs):
        self.num_lines = num_lines
        super().__init__(filename, **kwargs)

    def emit(self, record):
        msg = self.format(record)+'\n'
        with open(self.baseFilename, 'r+') as f:
            lines = f.readlines()
            f.seek(0, 0)
            f.truncate()
            print(len(lines))
            f.writelines([msg]+lines[:self.num_lines])


class MemoryLogHandler(logging.Handler):
    buffer = []

    def __init__(self, num_lines=100, **kwargs):
        self.num_lines = num_lines
        super().__init__(**kwargs)

    def emit(self, record):
        MemoryLogHandler.buffer = [self.format(
            record)] + MemoryLogHandler.buffer[:self.num_lines]
