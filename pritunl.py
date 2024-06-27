# Module to mock pritunl logger when running test.py

class Logger:
    def debug(self, message):
        print('DEBUG', message)

    def error(self, message):
        print('ERROR', message)

    def info(self, message):
        print('INFO', message)


logger = Logger()