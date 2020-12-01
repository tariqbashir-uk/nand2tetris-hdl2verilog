// TestInputMultibitBus1

load TestInputMultibitBus1.hdl,
output-file TestInputMultibitBus1.out,
compare-to TestInputMultibitBus1.cmp,
output-list a%D2.3.2 address%D2.3.2 b%B3.8.3 out%B3.16.3 out%X3.4.3 out%D1.5.1;

set a 0,
set address %B101010,
set b %B00000000,
eval,
output;

set a -1,
set b %B00000000,
set address 63,
eval,
output;

set a 0,
set b %B11111111,
eval,
output;

set a -1,
set b %B11111111,
eval,
output;

set a -49,
set b %B11001111,
set address %X11,
eval,
output;

set a -86,
set b %B10101010,
set address %B111111,
eval,
output;