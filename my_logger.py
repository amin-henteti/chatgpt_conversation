"""
The class MyLogger encapsulates the logging functionality.
We define two class variables called LEVELS and COLOR_SCHEMES that store dictionaries 
    - LEVELS define the mapping between log levels and their respective integer values
    - COLOR_SCHEMES define the mapping between color schemes and their respective color dictionaries
"""

import logging
import colorlog

class MyLogger:
    LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    COLOR_SCHEMES = {
        'AUTOCOLOR': None,
        'NOCOLOR': '%(message)s',
        'LIGHTBG': {
            'DEBUG': 'black',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        },
        'DARKBG': {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        }
    }

    def __init__(self, logfile='output.log', console_color='AUTOCOLOR'):
        """
        we create the console and file handlers, and add them to the logger. 
        We set the console formatter's log colors based on the input console_color argument 
        using the COLOR_SCHEMES dictionary.
        """
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        
        # Define log format
        log_format = '%(asctime)s - %(levelname)s - %(message)s'

        # Create a console handler with a colored formatter
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(message)s',
            log_colors=self.COLOR_SCHEMES[console_color.upper()],
            secondary_log_colors={}
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Create a file handler with a timestamp formatter
        file_formatter = logging.Formatter(log_format)
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def log(self, level, msg, *args, **kwargs):
        """
        Takes the log_color argument that defaults to None, 
        and uses it to set the log color for the console
        """
        log_color = kwargs.pop('log_color', None)
        if log_color:
            record = self.logger.makeRecord(
                self.logger.name, self.LEVELS[level], self.logger.funcName, None, msg, args, None, None)
            record.log_color = log_color
            self.logger.handle(record)
        else:
            getattr(self.logger, level.lower())(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.log('DEBUG', msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log('INFO', msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log('WARNING', msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log('ERROR', msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log('CRITICAL', msg, *args, **kwargs)
