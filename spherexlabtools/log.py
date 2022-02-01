import logging


class Logger:
    """ Basic convenience class for logging actions taken in an experiment.
    """

    def __init__(self, name=None, log=None):
        """ Initialize a logger

        :param: name: Name of the logger.
        :param: log: dictionary of the following form:
                     {
                        "level": log level.
                        "handler": logging file handler.
                     }
        """
        self.level = None
        self.logger = None
        if name is not None and log is not None:
            self.logger = logging.getLogger(name)
            assert "level" in log.keys(), "Log level must be specified in 'log' argument!"
            assert "handler" in log.keys(), "File handler must be specified in 'log' argument!"
            self.level = log["level"]
            self.logger.setLevel(log["level"])
            self.logger.addHandler(log["handler"])

    def log(self, record, level=None):
        """ Log a record if a level and handler have been set.

        :param: record: Message to log.
        :param: level: Log level to override the default set on instantiation.
        """
        lvl = level if level is not None else self.level
        if self.logger is not None:
            self.logger.log(lvl, record)
