% PARAMETERS
float: GOLD_PROFIT;
float: BTC_PROFIT;
float: ETH_PROFIT;

float: RW_GOLD;
float: RW_BTC;
float: RW_ETH;
float: RW_BOND;
float: RW_NONE;

float: ACC_GOLD;
float: ACC_BTC;
float: ACC_ETH;
float: ACC_BOND;
float: ACC_NONE;

float: ML_BTC;
float: ML_ETH;

float: SOP_RW_ACC;
float: CAPITAL;

% VARIABLES
var 0.0..CAPITAL: x_gold;
var 0.0..CAPITAL: x_btc;
var 0.0..CAPITAL: x_eth;
var 0.0..CAPITAL: x_bond;
var 0.0..CAPITAL: x_nothing;

var 1..3: lev_btc;
var 1..3: lev_eth;

% OBJECTIVE
var float: total_return =
    x_gold * (1.0 + GOLD_PROFIT) +
    x_btc  * (1.0 + BTC_PROFIT) * lev_btc +
    x_eth  * (1.0 + ETH_PROFIT) * lev_eth +
    x_bond * (1.0 + 0.0055 / 4.0) +
    x_nothing;

solve maximize total_return;

% CONSTRAINTS
constraint x_gold + x_eth + x_btc + x_bond + x_nothing = CAPITAL;

constraint x_gold    <= CAPITAL * RW_GOLD * ACC_GOLD / SOP_RW_ACC;
constraint x_eth     <= CAPITAL * RW_ETH  * ACC_ETH  / SOP_RW_ACC;
constraint x_btc     <= CAPITAL * RW_BTC  * ACC_BTC  / SOP_RW_ACC;
constraint x_bond    <= CAPITAL * RW_BOND * ACC_BOND / SOP_RW_ACC;
constraint x_nothing <= CAPITAL * RW_NONE * ACC_NONE / SOP_RW_ACC;

constraint lev_btc * ML_BTC <= 0.9;
constraint lev_eth * ML_ETH <= 0.9;
