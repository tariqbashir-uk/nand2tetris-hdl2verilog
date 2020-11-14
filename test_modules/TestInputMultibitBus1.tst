// TestInputMultibitBus1

load TestInputMultibitBus1.hdl,
output-file TestInputMultibitBus1.out,
compare-to TestInputMultibitBus1.cmp,
output-list a%B2.8.2 b%B3.8.3 out%B3.16.3;

set a %B00000000,
set b %B00000000,
eval,
output;

set a %B11111111,
set b %B00000000,
eval,
output;

set a %B00000000,
set b %B11111111,
eval,
output;

set a %B11111111,
set b %B11111111,
eval,
output;

set a %B11001111,
set b %B11001111,
eval,
output;

set a %B10101010,
set b %B10101010,
eval,
output;