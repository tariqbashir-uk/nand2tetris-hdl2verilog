// TestOutputMultibit1

load TestOutputMultibit1.hdl,
output-file TestOutputMultibit1.out,
compare-to TestOutputMultibit1.cmp,
output-list a%B2.1.2 b%B2.1.2 out1%B3.1.3 out2%B3.2.3;

set a %B0,
set b %B0,
eval,
output;

set a %B0,
set b %B1,
eval,
output;

set a %B1,
set b %B0,
eval,
output;

set a %B1,
set b %B1,
eval,
output;