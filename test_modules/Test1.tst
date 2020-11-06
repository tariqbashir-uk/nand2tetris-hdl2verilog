// Test 1

load Test1.hdl,
output-file Test1.out,
compare-to Test1.cmp,
output-list a%B2.2.2 b%B3.3.3 out%B3.2.3;

set a %B00,
set b %B000,
eval,
output;

set a %B01,
set b %B101,
eval,
output;

set a %B10,
set b %B011,
eval,
output;

set a %B11,
set b %B111,
eval,
output;
