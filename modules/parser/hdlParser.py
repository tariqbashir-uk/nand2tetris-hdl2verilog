from modules.core.logger import Logger
from modules.hdlTypes.hdlChip import HdlChip
from modules.hdlTypes.hdlChipPart import HdlChipPart
from modules.hdlTypes.hdlConnection import HdlConnection
from modules.hdlTypes.hdlPin import HdlPin

from ply import lex, yacc

class HdlParser:
    reserved = [
        'CHIP', 'IN', 'OUT', 'PARTS', 'BUILTIN', 'CLOCKED'
    ]   
    
    tokens = [
        'COMMA', 'NAME', 'COMMENT1', 'COMMENT2', 'SEMICOLON', 'OCURLEYBRACKET', 
        'CCURLEYBRACKET', 'COLON', 'OBRACKET', 'CBRACKET', 'EQUALS', 'BIT_WIDTH'
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
    t_BIT_WIDTH = r'\[(.*?)\]'

    def __init__(self):
        self.logger  = Logger()
        self.hdlChip = HdlChip()
        self.lexer   = lex.lex(module=self)
        self.parser  = yacc.yacc(module=self)      
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

    def p_program(self, p):
        '''program : chip
                   | empty
                   '''
        p[0] = p[1]
        return

    # The empty production
    def p_empty(self, p):
        'empty :'
        p[0] = None #Node("EMPTY", [])
        return

    def p_statement(self, p):
        '''statement : in_list
                     | out_list
                     | parts
                     '''
        p[0] = p[1]
        return

    def p_partparam(self, p):
        '''partparam : pin EQUALS pin'''
        p[0] = HdlConnection(p[1], p[3])
        return

    def p_partparamlist(self, p):
        '''partparamlist : partparamlist COMMA partparam
                         | partparam'''

        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [p[1]]
        return

    def p_part(self, p):
        '''part : NAME OBRACKET partparamlist CBRACKET SEMICOLON'''
        hdlChipPart = HdlChipPart(p[1], p.lineno(1))
        for part in p[3]:
            hdlChipPart.AddConnection(part)

        p[0] = hdlChipPart
        return

    def p_partlist(self, p):
        '''partlist : partlist part
                    | part'''        

        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1]]
        return

    def p_parts(self, p):
        '''parts : PARTS COLON partlist'''
        for part in p[3]:
            self.hdlChip.AddPart(part)
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

    def p_chip(self, p):
        '''chip : CHIP NAME OCURLEYBRACKET statement_list CCURLEYBRACKET'''
        self.hdlChip.SetChipName(p[2])
        return

    def p_pin(self, p):
        '''pin : NAME BIT_WIDTH
               | NAME'''
        pinName     = p[1]
        pinBitWidth = None
        if len(p) > 2:
            pinBitWidth = p[2]

        if pinBitWidth:
            p[0] = HdlPin(pinName, bitWidthString=pinBitWidth)
        else:
            p[0] = HdlPin(pinName)
        return

    def p_pinlist(self, p):
        '''pinlist : pinlist COMMA pin
                   | pin'''

        if len(p) > 2:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [p[1]]
        return

    def p_in_list(self, p):
        '''in_list : IN pinlist SEMICOLON'''
        self.hdlChip.AddInputPins(p[2])
        return

    def p_out_list(self, p):
        '''out_list : OUT pinlist SEMICOLON'''
        self.hdlChip.AddOutputPins(p[2])
        return

    # def p_comment1(self, p):
    #     "comment1 : COMMENT1"
    #     pass

    # def p_comment2(self, p):
    #     "comment2 : COMMENT2"
    #     pass

    def p_error(self, p):
        if p:
            error_msg = "syntax error '%s'" % p.value
        else:
            error_msg = "syntax error at end of file"

        self.logger.Error(error_msg)
        return

    ##########################################################################
    def Parse(self, fileContent):
        self.lexer.input(fileContent)

        # for token in self.lexer:
        #     print(token)

        self.parser.parse(fileContent, tracking=True)
        self.hdlChip.DumpChipDetails()
        return self.hdlChip