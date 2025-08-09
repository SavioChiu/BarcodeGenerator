import os, logging, datetime, inspect, traceback

DEBUG = False


class Logger:

    @staticmethod
    def __deBugLog(msg=None):
        if DEBUG:
            if msg is not None:
                print(f"Logger --- deBugLog --- {datetime.datetime.now().strftime('%d-%m-%Y.%H:%M:%S')} --- {msg}")

    def __init__(self, filename=""):

        self.__deBugLog("__inti__ start")

        rootPath = os.path.join(os.path.abspath(os.curdir),'Temp')
        self.__deBugLog(f"rootPath: {rootPath}")

        logPath = os.path.join(rootPath, "log")
        self.__deBugLog(f"logPath: {logPath}")

        if not os.path.exists(rootPath):
            os.mkdir(rootPath)
        else:
            self.__deBugLog(f"rootPath exist")

        if not os.path.exists(logPath): os.mkdir(logPath)
        else:
            self.__deBugLog(f"logPath exist")

        logPath = os.path.join(logPath, f"{filename}_{datetime.datetime.now().strftime('%d-%m-%Y')}.log")
        self.__deBugLog(f"log file path: {logPath}")

        self.logging_config(logPath)

    @staticmethod
    def logging_config(logPath:os.path) -> None:
        # set format and path for log file
        logging.basicConfig(level=logging.INFO,
                            filename=logPath,
                            filemode='a',
                            format='%(asctime)s ---- [ %(levelname)s ] ---- %(message)s',
                            datefmt='%d-%m-%Y_%H.%M.%S'
                            )

    @staticmethod
    def infoLog(msg: str) -> None:

        filename = os.path.split(inspect.stack()[1].filename)[-1]
        function = inspect.stack()[1].function
        line = inspect.stack()[1].lineno
        logging.info(f'{filename} Line: {line} ---- {function} ---- {msg}')

    @staticmethod
    def errorLog(eMsg: Exception) -> None:
        filename = os.path.split(inspect.stack()[1].filename)[-1]
        function = inspect.stack()[1].function
        line = inspect.stack()[1].lineno
        # logging.error(f'{inspect.stack()[1].function} ---- {eMsg}')
        logging.error(f'{filename} Line: {line} ---- {function} ---- {eMsg}')

    @staticmethod
    def criticalLog() -> None:
        logging.critical(traceback.format_exc().replace("\n", " "))

