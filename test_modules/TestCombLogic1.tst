// TestCombLogic1

load TestCombLogic1.hdl,
output-file TestCombLogic1.out,
compare-to TestCombLogic1.cmp,
output-list time%S1.4.1 a%B2.1.2 out%B3.1.3;

set a 0,
tick,
output;

tock,
output;

set a 1,
tick,
output;

tock,
output;

set a 0,
tick,
output;

tock,
output;