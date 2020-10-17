
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COMMA COMMENT1 COMMENT2 DASH DOT NAME NUMBER PERCENT SEMICOLON compare eval file list load output set totest  : statement_list\n                 | empty\n                 empty :statement_list : statement_list statement\n                          | statementstatement : set_sequence \n                     | output_statement\n                     | load_statement\n                     | compare_statement\n                     load_statement : load NAME DOT NAME COMMAcompare_statement : compare DASH to NAME DOT NAME COMMAeval_statement : eval COMMAset_sequence : set_list eval_statement output SEMICOLON\n                        set_statement : set NAME NUMBER COMMA\n                         | set NAME PERCENT NAME COMMA\n                         set_list : set_list set_statement\n                    | set_statement    \n                    output_statement : output_file\n                            | output_list\n                            output_file : output DASH file NAME DOT NAME COMMAoutput_list : output DASH list output_param_list SEMICOLONoutput_param_list : output_param_list output_param\n                             | output_param    \n                             output_param : NAME PERCENT NAME DOT NUMBER DOT NUMBER'
    
_lr_action_items = {'$end':([0,1,2,3,4,5,6,7,8,11,12,17,33,43,46,52,54,],[-3,0,-1,-2,-5,-6,-7,-8,-9,-18,-19,-4,-13,-21,-10,-20,-11,]),'load':([0,2,4,5,6,7,8,11,12,17,33,43,46,52,54,],[13,13,-5,-6,-7,-8,-9,-18,-19,-4,-13,-21,-10,-20,-11,]),'compare':([0,2,4,5,6,7,8,11,12,17,33,43,46,52,54,],[14,14,-5,-6,-7,-8,-9,-18,-19,-4,-13,-21,-10,-20,-11,]),'output':([0,2,4,5,6,7,8,11,12,17,18,26,33,43,46,52,54,],[10,10,-5,-6,-7,-8,-9,-18,-19,-4,25,-12,-13,-21,-10,-20,-11,]),'set':([0,2,4,5,6,7,8,9,11,12,15,17,19,33,40,43,46,48,52,54,],[16,16,-5,-6,-7,-8,-9,16,-18,-19,-17,-4,-16,-13,-14,-21,-10,-15,-20,-11,]),'eval':([9,15,19,40,48,],[20,-17,-16,-14,-15,]),'DASH':([10,14,],[21,23,]),'NAME':([13,16,27,28,29,30,32,35,36,42,44,45,47,57,],[22,24,34,37,38,39,41,37,-23,49,-22,50,51,-24,]),'COMMA':([20,31,38,41,49,51,],[26,40,46,48,52,54,]),'file':([21,],[27,]),'list':([21,],[28,]),'DOT':([22,34,39,50,55,],[29,42,47,53,56,]),'to':([23,],[30,]),'NUMBER':([24,53,56,],[31,55,57,]),'PERCENT':([24,37,],[32,45,]),'SEMICOLON':([25,35,36,44,57,],[33,43,-23,-22,-24,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'test':([0,],[1,]),'statement_list':([0,],[2,]),'empty':([0,],[3,]),'statement':([0,2,],[4,17,]),'set_sequence':([0,2,],[5,5,]),'output_statement':([0,2,],[6,6,]),'load_statement':([0,2,],[7,7,]),'compare_statement':([0,2,],[8,8,]),'set_list':([0,2,],[9,9,]),'output_file':([0,2,],[11,11,]),'output_list':([0,2,],[12,12,]),'set_statement':([0,2,9,],[15,15,19,]),'eval_statement':([9,],[18,]),'output_param_list':([28,],[35,]),'output_param':([28,35,],[36,44,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> test","S'",1,None,None,None),
  ('test -> statement_list','test',1,'p_test','tstParser.py',66),
  ('test -> empty','test',1,'p_test','tstParser.py',67),
  ('empty -> <empty>','empty',0,'p_empty','tstParser.py',74),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','tstParser.py',79),
  ('statement_list -> statement','statement_list',1,'p_statement_list','tstParser.py',80),
  ('statement -> set_sequence','statement',1,'p_statement','tstParser.py',90),
  ('statement -> output_statement','statement',1,'p_statement','tstParser.py',91),
  ('statement -> load_statement','statement',1,'p_statement','tstParser.py',92),
  ('statement -> compare_statement','statement',1,'p_statement','tstParser.py',93),
  ('load_statement -> load NAME DOT NAME COMMA','load_statement',5,'p_load_statement','tstParser.py',100),
  ('compare_statement -> compare DASH to NAME DOT NAME COMMA','compare_statement',7,'p_compare_statement','tstParser.py',105),
  ('eval_statement -> eval COMMA','eval_statement',2,'p_eval_statement','tstParser.py',110),
  ('set_sequence -> set_list eval_statement output SEMICOLON','set_sequence',4,'p_set_sequence','tstParser.py',114),
  ('set_statement -> set NAME NUMBER COMMA','set_statement',4,'p_set_statement','tstParser.py',121),
  ('set_statement -> set NAME PERCENT NAME COMMA','set_statement',5,'p_set_statement','tstParser.py',122),
  ('set_list -> set_list set_statement','set_list',2,'p_set_list','tstParser.py',136),
  ('set_list -> set_statement','set_list',1,'p_set_list','tstParser.py',137),
  ('output_statement -> output_file','output_statement',1,'p_output_statement','tstParser.py',148),
  ('output_statement -> output_list','output_statement',1,'p_output_statement','tstParser.py',149),
  ('output_file -> output DASH file NAME DOT NAME COMMA','output_file',7,'p_output_file','tstParser.py',156),
  ('output_list -> output DASH list output_param_list SEMICOLON','output_list',5,'p_output_list','tstParser.py',161),
  ('output_param_list -> output_param_list output_param','output_param_list',2,'p_output_param_list','tstParser.py',167),
  ('output_param_list -> output_param','output_param_list',1,'p_output_param_list','tstParser.py',168),
  ('output_param -> NAME PERCENT NAME DOT NUMBER DOT NUMBER','output_param',7,'p_output_param','tstParser.py',179),
]
