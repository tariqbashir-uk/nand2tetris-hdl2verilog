import atexit
import time
import datetime
import modules.settings as settings
from os.path import join
import os

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    pass

    logFile = None

    ##########################################################################
    # SetLogFolder
    ##########################################################################
    def SetLogFolder(self, folder, filename=settings.LOGFILE_NAME):
#       print("Creating logfile: " + join(folder, filename)) 
        atexit.register(self._OnQuit)
        
        logFolder = join(folder, settings.LOG_DIRECTORY_NAME)
        if os.path.exists(logFolder) != True:
            os.makedirs(logFolder)
       
        self.logFile = open(join(logFolder, filename), "w")
        self.Info("Created using v%s" % settings.VERSION_NUMBER)
       
    ##########################################################################
    # Debug
    ##########################################################################
    def Debug(self, logText):
        self._WriteTrace("Debug", logText)

    ##########################################################################
    # Error
    ##########################################################################
    def Error(self, logText):
        self._WriteTrace("Error", logText, writeToConsole=True)

    ##########################################################################
    # Warn
    ##########################################################################
    def Warn(self, logText):
        self._WriteTrace("Warn ", logText)

    ##########################################################################
    # info
    ##########################################################################
    def Info(self, logText, writeToConsole=True):
        self._WriteTrace("Info ", logText, writeToConsole=writeToConsole)

    ##########################################################################
    # EmptyLine
    ##########################################################################
    def EmptyLine(self):
        self.Error("")

    ##########################################################################
    # Private: _WriteTrace
    ##########################################################################
    def _WriteTrace(self, level, logText, writeToConsole=False):
        ts = time.time()
#            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        
        if len(logText) > 0:
            fullText = st + " [" + level + "] " + logText
        else: 
            fullText = logText  
            
        if self.logFile != None:
            self.logFile.write(fullText + "\n")
            self.logFile.flush()

        if writeToConsole == True:
            print(fullText)

    ##########################################################################
    # Private: _OnQuit
    ##########################################################################
    def _OnQuit(self):
#        print("Quit detected")
        if self.logFile != None:
            self.logFile.close()

