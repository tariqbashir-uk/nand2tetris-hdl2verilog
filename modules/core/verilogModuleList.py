from os.path import join
from modules.core.logger import Logger
from modules.core.fileActions import FileActions
from modules.verilogTypes.verilogModule import VerilogModule
from modules.generator.verilogModuleGenerator import VerilogModuleGenerator

class VerilogModuleList():
    def __init__(self, builtInChipFolder):
        self.logger = Logger()
        self.moduleList = [] # type: list[VerilogModule]
        self.builtInModuleList = [] # type: list[VerilogModule]
        self.builtInChipFolder = builtInChipFolder
        return

    ##########################################################################
    def AddModule(self, module):
        self.moduleList.append(module)
        return

    ##########################################################################
    def AddBuiltInModule(self, module):
        self.builtInModuleList.append(module)
        return

    ##########################################################################
    def GetFilenamesForModules(self, inputModuleList):
        filenameList = []
        for inputModule in inputModuleList:
            moduleFromList        = [x for x in self.moduleList if inputModule == x.moduleName]
            moduleFromBuiltInList = [x for x in self.builtInModuleList if inputModule == x.moduleName]

            if len(moduleFromList) > 0:
                # Generated module was found, so let use that
                filenameList.append(moduleFromList[0].moduleFilename)
            elif len(moduleFromBuiltInList) > 0:
                # Module must be taken from the builtin list
                filenameList.append(moduleFromBuiltInList[0].moduleFilename)
            else:
                self.logger.Error("Couldn't find module %s in the generated or built-in list" % (inputModule))

        return filenameList

    ##########################################################################
    def CheckModulesInBuiltInList(self, moduleList):
        missingBuiltInModuleList = []
        for module in moduleList:
            result = [x for x in self.builtInModuleList if module == x.moduleName]

            if len(result) == 0:
                missingBuiltInModuleList.append(module)

        return missingBuiltInModuleList

    ##########################################################################
    def WriteModules(self, outputFolder):
        verilogModGen = VerilogModuleGenerator(outputFolder)

        for module in self.moduleList:
            verilogModGen.CreateModule(module)

        return

    ##########################################################################
    def CopyInternalModules(self, outputFolder, usedBuiltInModules):
        fileActions = FileActions()

        for moduleName in usedBuiltInModules: 
            for verilogModule in self.builtInModuleList:
                if verilogModule.moduleName == moduleName:        
                    fileActions.CopyFile(join(self.builtInChipFolder, verilogModule.moduleFilename), 
                                         join(outputFolder, verilogModule.moduleFilename))
                    break
        return        