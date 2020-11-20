class VerilogWireAssignment():
    def __init__(self, variable, assignment):
        self.variable   = variable
        self.assignment = assignment
        return

    ##########################################################################
    def GetAssignmentStr(self):
        return ("assign %s = %s;" % (self.variable, self.assignment))