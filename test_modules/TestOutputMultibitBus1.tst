// TestOutputMultibitBus1

load TestOutputMultibitBus1.hdl,
output-file TestOutputMultibitBus1.out,
compare-to TestOutputMultibitBus1.cmp,
output-list a%B2.16.2 out%B3.16.3;

set a %B0000000000000000,
eval,
output;

set a %B1000000000000001,
eval,
output;

set a %B1111111100000000,
eval,
output;

set a %B0000000110000000,
eval,
output;

set a %B0000000011111111,
eval,
output;