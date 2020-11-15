#!/bin/bash
set -e

if [[ -z "${NAND2_FPGA_HARDWARESIM}" ]]; then
  echo "Environment variable NAND2_FPGA_HARDWARESIM is undefined, please set it to the location of HardwareSimulator.sh (e.g. export NAND2_FPGA_HARDWARESIM=<dir>/nand2tetris/nand2tetris/tools/HardwareSimulator.sh"
  exit 1
fi

list=$(find . -name '*.tst')

echo "############# Checking test modules pass on nand2fpga Hardware Simulator #############"
for testFile in $list
do
  echo "Testing $testFile" 
  "${NAND2_FPGA_HARDWARESIM}" $testFile
done

echo "############# Converting modules #############"
cd ..
python3 ./hdl2verilog.py -i ./test_modules -o ./tmp_generated

cd tmp_generated
if [[ ! -d ./out ]]; then
    mkdir out
fi

chmod +x ./runme.sh

echo "############# Running generated tests #############"
./runme.sh