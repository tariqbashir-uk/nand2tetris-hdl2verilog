if [[ -z "${NAND2_FPGA_HARDWARESIM}" ]]; then
  echo "Environment variable NAND2_FPGA_HARDWARESIM is undefined, please set it to the location of HardwareSimulator.sh (e.g. export NAND2_FPGA_HARDWARESIM=<dir>/nand2tetris/nand2tetris/tools/HardwareSimulator.sh"
  exit 1
fi

list=$(find . -name '*.tst')

for testFile in $list
do
  echo "Testing $testFile" 
  "${NAND2_FPGA_HARDWARESIM}" $testFile
done
