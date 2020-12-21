#/usr/bin/python3
import os
import sys
from os.path import join

import argparse
import modules.settings as settings

from modules.core.hdl2verilogMain import Hdl2verilogMain
from modules.core.logger import Logger

baseFolder = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description='Convert nand2tetris hdl and tst files into verilog.')

parser.add_argument('--version', action='version', version='%(prog)s: v' + settings.VERSION_NUMBER)

parser.add_argument("-i", dest="inFolder", required=True,
                    help="The source folder")

parser.add_argument("-o", dest="outFolder", required=True,
                    help="The output folder")

args = parser.parse_args()

baseOutputFolder = args.outFolder
if not os.path.exists(baseOutputFolder):
    os.makedirs(baseOutputFolder)

logger = Logger()
logger.SetLogFolder(baseOutputFolder)

hdl2verilogMain = Hdl2verilogMain()
hdl2verilogMain.Run(args.inFolder, join(baseFolder, settings.BUILTIN_CHIP_DIRECTORY_NAME), args.outFolder)