# hdl2verilog

[Nand To Tetris](nand2tetris.org) is an amazing course which guides students and self-learners through the construction of a modern, full-scale computer system - hardware and software - from the ground up.

### Intro

The course uses a simplified HDL that runs on a simulator. This HDL is great for learning how to implement complex logic using simple gates without the distraction of using a fully featured HDL like Verilog or VHDL. I wanted something to help me go from using the simplified HDL to using real Verilog.

The result is the hdl2verliog tool, which I created to help me achieve this.

![Example: Intro](./assets/Intro.png?raw=true)

Using this tool and a verilog compiler you will be able to: 
- Convert all the HDL modules you created in exercise 01 to 03 (will be expanded later) to verilog modules.
- Convert the tst files that go with the HDL modules to verilog test bench files.
- Use the provided cmp file to verify the testbench output (i.e. test that the converted verilog code works).

### Setting up tool (recommended tools)
1. Ensure you have python3 installed on your machine
2. Ensure you have the correct dependencies installed: pip install -r requirements.txt
3. Install [Icarus Verilog](http://iverilog.icarus.com/)
4. Install [GTKWave](http://gtkwave.sourceforge.net/)

### Using the tool
1. Complete an HDL course project (01, 02 or 03a or 03b) and verify your HDL implementation passes on the simulator.
2. Run the tool on the project folder and provide an output folder:
python3 ./hdl2verilog.py -i ~/nand2tetris/projects/01/ -o ./output/01

After running the tool should have created the output folder and put all the generated modules and testbench files in it. It will also generate a script iverilog_compile_and_test.sh which can be run to compile the modules and test benches using Icarus Verilog (which must be installed and in your path), run the test benches and then compare the generated out file with the cmp files in your input folder. The script will terminate on any Icarus compilation error or comparison error when the output is checked.
You may use other Verilog compilers and simulators, but you would need to manually import the test bench and modules if you do this (I have tested with Modelsim).
Every testbench that is run will produce a vcd file and this can be opened in a simulator like GTKWave to debug.

![Example: Generated And](./assets/Nand2Tetris_Project_Folder.png?raw=true "Example: Generated And")

![Example: Generated And](./assets/Generated_And_Example.png?raw=true "Example: Generated And")

![Example: Generated And In Simulator](./assets/GTKWave.png?raw=true "Example: Generated And")

### Known Limitations:
1. Tst files that have file names with multiple dashes or spaces in fields 'load', 'output-file' or 'compare-to' won't be parsed correctly.
2. Keyword BULTIN is not supported yet

# VSCode pylint issues:
In macOS / Linux:
Create .env file with:
PYTHONPATH=./:$PYTHONPATH