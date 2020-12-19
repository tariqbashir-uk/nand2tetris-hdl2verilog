from modules.core.logger import Logger
from modules.verilogTypes.verilogModule import VerilogModule

from ply import lex, yacc

class VerilogModuleParser:
    reserved = [
        'module'
    ]   
    
    tokens = [
        'COMMA', 'NAME', 'COMMENT1', 'COMMENT2', 'SEMICOLON', 'OCURLEYBRACKET', 
        'CCURLEYBRACKET', 'COLON', 'OBRACKET', 'CBRACKET', 'EQUALS'
     ] + reserved

    #literals = ['=']

    t_ignore = " \t"
    t_COMMA = r','
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_OCURLEYBRACKET = r'{'
    t_CCURLEYBRACKET = r'}'
    t_OBRACKET = r'\('
    t_CBRACKET = r'\)'
    t_EQUALS = r'='

    def __init__(self):
        self.logger        = Logger()
        self.verilogModule = VerilogModule(None)
        self.lexer         = lex.lex(module=self)
        self.parser        = yacc.yacc(module=self)      
        return

    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9_]*'
        if t.value in self.reserved:
            t.type = t.value
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

    def p_verilogmodule(self, p):
        '''verilogmodule : module NAME OBRACKET paramlist CBRACKET SEMICOLON
                         | empty
                         '''
        p[0] = p[1]
        if len(p) > 2:
            self.verilogModule.SetModuleName(p[2])
        return

    # The empty production
    def p_empty(self, p):
        'empty :'
        p[0] = None #Node("EMPTY", [])
        return

    def p_paramlist(self, p):
        '''paramlist : paramlist COMMA NAME
                     | NAME'''

        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [p[1]]
        return

    # def p_comment1(self, p):
    #     "comment1 : COMMENT1"
    #     pass

    # def p_comment2(self, p):
    #     "comment2 : COMMENT2"
    #     pass

    def p_error(self, p):
        if p:
            error_msg = "syntax error '%s' at %d" % (p.value, p.lineno)
        else:
            error_msg = "syntax error at end of file"

        # We only care about getting the module name of built in modules.
        # Therefore we expect lots of errors, that can be ignored
        #self.logger.Error(error_msg)
        return

    ##########################################################################
    def Parse(self, fileContent):
        self.lexer.input(fileContent)

        # for token in self.lexer:
        #     print(token)

        self.parser.parse(fileContent, tracking=True)
        self.verilogModule.DumpModuleDetails()
        return self.verilogModule