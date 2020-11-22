// TestCombLogic1

load TestCombLogic1.hdl,
output-file TestCombLogic1.out,
compare-to TestCombLogic1.cmp,
output-list time%S1.4.1 load%B3.1.3 out%B3.1.3;

set load 0,
tick,
output;

tock,
output;

set load 1,
tick,
output;

tock,
output;

set load 0,
tick,
output;

tock,
output;