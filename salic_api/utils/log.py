import inspect
import logging

from ..app import app


class Log:
    """
    Log Class provides a unique way to record log messages of this program.
    """

    logger = None

    @classmethod
    def instantiate(cls, stream_type="SCREEN", log_level="INFO"):
        """
        Create a new instance of Log class.

        Args:
            stream_type:
                String containing the stream type name.
            log_level:
                String containing the name of the level to be used in the log.
        """
        try:
            logging.VERBOSE = 5
            logging.addLevelName(logging.VERBOSE, "VERBOSE")
            logging.Logger.verbose = lambda inst, msg, * \
                args, **kwargs: inst.log(logging.VERBOSE, msg, *args, **kwargs)
            logging.verbose = lambda msg, * \
                args, **kwargs: logging.log(logging.VERBOSE, msg, *args,
                                            **kwargs)

            cls.logger = logging.getLogger()

            if log_level not in logging._levelNames:
                raise Exception('Invalid file level')

            cls.logger.setLevel(logging._levelNames[log_level])

            stream_type = app.config['STREAMTYPE']

            if stream_type == "SCREEN":
                stream = logging.StreamHandler()
            else:
                stream = logging.FileHandler(app.config['LOGFILE'])

            formatter = logging.Formatter(
                '[%(levelname)-7s - %(asctime)s] %(message)s')
            stream.setFormatter(formatter)
            cls.logger.addHandler(stream)
        except Exception as e:
            print(('Unable to get/set log configurations. Error: %s' % (e)))
            cls.logger = None

    ##
    # Records a message in a file and/or displays it in the screen.
    # @param level - String containing the name of the log message.
    # @param message - String containing the message to be recorded.
    #
    @classmethod
    def log(cls, level, message, caller=None):
        if not cls.logger:
            cls.instantiate(log_level=app.config['LEVELOFLOG'])

        try:
            if level not in logging._levelNames:
                cls.log("ERROR", 'Invalid file level \'%s\'' % (level))

            log_level = logging._levelNames[level]
            if not caller:
                callers = Log.get_callers(inspect.stack())
            else:
                callers = caller
            message = '%s.%s - %s' % (callers[0], callers[1], message)

            cls.logger.log(log_level, message)
        except Exception as e:
            print(('Unable to record the log. Error: %s' % (e)))

    @classmethod
    def info(cls, message):
        cls.log("INFO", message, Log.get_callers(inspect.stack()))

    @classmethod
    def error(cls, message):
        cls.log("ERROR", message, Log.get_callers(inspect.stack()))

    @classmethod
    def warn(cls, message):
        cls.log("WARN", message, Log.get_callers(inspect.stack()))

    @classmethod
    def debug(cls, message):
        cls.log("DEBUG", message, Log.get_callers(inspect.stack()))

    @classmethod
    def verbose(cls, message):
        cls.log("VERBOSE", message, Log.get_callers(inspect.stack()))

    @staticmethod
    def get_callers(stack):
        """
        Gets the data about the caller of the log method.

        Args:
            stack:
                Array containing the system calling stack.
        Return:
            Array containing the caller class name and the caller method,
            respectively.
        """

        caller_class = None
        caller_method = None
        if stack:
            if len(stack) > 1:
                if stack[1][3] == '<module>':
                    caller_method = stack[1][0].f_locals.get('__name__')
                    caller_class = \
                        ((str(stack[1][0].f_locals.get('__file__'))).split(
                            '/')[-1]).split('.')[0]
                else:
                    caller_method = stack[1][3]
                    if 'self' in stack[1][0].f_locals:
                        caller_class = stack[1][0].f_locals.get(
                            'self').__class__.__name__
                    elif 'cls' in stack[1][0].f_locals:
                        caller_class = stack[1][0].f_locals.get('cls').__name__
                    else:
                        caller_class = 'NoneType'
        return (caller_class, caller_method)
