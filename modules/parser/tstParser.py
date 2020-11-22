from modules.core.logger import Logger
from modules.tstTypes.tstScript import TstScript
from modules.tstTypes.tstSetSequence import TstSetSequence
from modules.tstTypes.tstSetOperation import TstSetOperation
from modules.tstTypes.tstSetSequenceTypes import TstSetSequenceTypes
from modules.tstTypes.tstOutputParam import TstOutputParam

from ply import lex, yacc

class TstParser:
    reserved = [
        'set', 'output', 'list', 'eval', 'load', 'compare', 'to', 'file', 'tick', 'tock'
    ]   
    
    tokens = [
        'NAME', 'NUMBER', 'COMMA', 'DOT', 'DASH', 'COMMENT1', 
        'COMMENT2', 'SEMICOLON', 'PERCENT'
     ] + reserved

    #literals = ['%']

    t_ignore = " \t"
    t_COMMA = r','
    t_DOT = r'\.'
    t_DASH = r'-'
    t_SEMICOLON = r';'
    t_PERCENT = r'%'

    def __init__(self):
        self.logger    = Logger()
        self.lexer     = lex.lex(module=self)
        self.parser    = yacc.yacc(module=self)
        self.tstScript = TstScript()   
        return

    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9_]*'
        if t.value in self.reserved:
            t.type = t.value
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMMENT1(self, t):
        r'(/\*(.|\n)*?\*/\n)'
        t.lexer.lineno += len(t.value.split("\n")) - 1
        #return t
        pass

    def t_COMMENT2(self, t):
        r'(//.*?(\n|$))'
        t.lexer.lineno += 1
        #return t
        pass

# statement-list:

    def p_test(self, p):
        '''test  : statement_list
                 | empty
                 '''
        p[0] = p[1]
        return

    # The empty production
    def p_empty(self, p):
        'empty :'
        p[0] = None #Node("EMPTY", [])
        return

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                          | statement'''        
        
        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1]]
        return

    def p_statement(self, p):
        '''statement : set_sequence 
                     | output_statement
                     | load_statement
                     | compare_statement
                     '''
        p[0] = p[1]
        #print("Statement: " + str(p[1]))
        return

    def p_load_statement(self, p):
        '''load_statement : load NAME DOT NAME COMMA'''
        self.tstScript.testHdlModule = p[2]
        return

    def p_compare_statement(self, p):
        '''compare_statement : compare DASH to NAME DOT NAME COMMA
                             | compare DASH to NAME DASH NAME DOT NAME COMMA'''
        if len(p) > 8:
            self.tstScript.compareFile = ("%s-%s.%s" % (p[4], p[6], p[8]))
        else:
            self.tstScript.compareFile = ("%s.%s" % (p[4], p[6]))
        return

    def p_eval_statement(self, p):
        '''eval_statement : eval COMMA'''
        p[0] = p[1]
        return

    def p_tock_statement(self, p):
        '''tock_statement : tock COMMA'''
        p[0] = p[1]
        return

    def p_tick_statement(self, p):
        '''tick_statement : tick COMMA'''
        p[0] = p[1]
        return

    def p_set_sequence(self, p):
        '''set_sequence : set_list eval_statement output SEMICOLON
                        | set_list tick_statement output SEMICOLON
                        | set_list tock_statement output SEMICOLON
                        | tock_statement output SEMICOLON
                        '''
        if len(p) == 5:
            setList      =  p[1]
            sequenceType = self.GetSequenceType(p[2])
        else:
            setList      = None
            sequenceType = self.GetSequenceType(p[1])
            
        self.tstScript.AddSetSequence(TstSetSequence(sequenceType, setList))
        #print("set_sequence: %s, len = %d" % (sequenceType, len(p)))
        return

    def p_set_statement(self, p):
        '''set_statement : set NAME NUMBER COMMA
                         | set NAME DASH NUMBER COMMA
                         | set NAME PERCENT NAME COMMA
                         | set NAME PERCENT NAME SEMICOLON  
                         | set load NUMBER COMMA
                         | set load DASH NUMBER COMMA
                         | set load PERCENT NAME COMMA
                         | set load PERCENT NAME SEMICOLON 
                         '''
        pinValue = ""
        pinName  = p[2]
        if len(p) > 5:
            pinValue += ("%s%s" % (p[3], p[4]))
        else:
            pinValue += str(p[3])

        p[0] = TstSetOperation(pinName, pinValue)
        #print("set_statement: %s = %s" % (pinName, pinValue))
        return

    def p_set_list(self, p):
        '''set_list : set_list set_statement
                    | set_statement    
                    '''        
        
        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1]]
        return

    def p_output_statement(self, p):
        '''output_statement : output_file
                            | output_list
                            '''
        p[0] = p[1]
        #print("set_statement: " + str(p[3]))
        return

    def p_output_file(self, p):
        '''output_file : output DASH file NAME DOT NAME COMMA
                       | output DASH file NAME DASH NAME DOT NAME COMMA'''
        if len(p) > 8:
            self.tstScript.outputFile = ("%s-%s.%s" % (p[4], p[6], p[8]))
        else:
            self.tstScript.outputFile = ("%s.%s" % (p[4], p[6]))
        return

    def p_output_list(self, p):
        '''output_list : output DASH list output_param_list SEMICOLON'''
        self.tstScript.SetOutputFormatList(p[4])
        #print("output_list: " + str(p[4]))
        return

    def p_output_param_list(self, p):
        '''output_param_list : output_param_list output_param
                             | output_param    
                             '''        
        
        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1]]
        return

    def p_output_param(self, p):
        # a%B1.16.1
        '''output_param : NAME PERCENT NAME DOT NUMBER DOT NUMBER
                        | load PERCENT NAME DOT NUMBER DOT NUMBER
                        '''
        #p[0] = ("%s%s%s%s%s%s%s" % (p[1], p[2], p[3], p[4], p[5], p[6], p[7]))
        p[0] = TstOutputParam(p[1], p[3])
        return

    def p_error(self, p):
        if p:
            error_msg = "syntax error '%s' at %d" % (p.value, p.lineno)
        else:
            error_msg = "syntax error at end of file"

        self.logger.Error(error_msg)
        return

    ##########################################################################
    def GetSequenceType(self, typeName):
        sequenceType = TstSetSequenceTypes.eval
        for seqType in TstSetSequenceTypes:
            if typeName.casefold() == str(seqType).casefold():
                sequenceType = seqType
        return sequenceType

    ##########################################################################
    def Parse(self, fileContent, testName):
        self.lexer.input(fileContent)

        # for token in self.lexer:
        #     print(token)

        self.tstScript.testName = testName
        self.parser.parse(fileContent)
        self.tstScript.DumpTestDetails()
        return self.tstScript