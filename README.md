# hdl2verilog

Dependencies:
pip3 install ply 


Create .env file with:
# In macOS / Linux:
PYTHONPATH=./:$PYTHONPATH

Known Limitations:
1. Tst files that have file names with multiple dashes or spaces in fields 'load', 'output-file' or 'compare-to' won't be parsed correctly.