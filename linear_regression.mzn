% regression_closedform.mzn
int: n = 5;
array[1..n] of int: x = [1,2,3,4,5];
array[1..n] of int: y = [2,4,5,4,5];

% Compute sums as floats by 1.0*int
float: Sx  = sum(i in 1..n)(1.0 * x[i]);
float: Sy  = sum(i in 1..n)(1.0 * y[i]);
float: Sxy = sum(i in 1..n)(1.0 * x[i] * y[i]);
float: Sxx = sum(i in 1..n)(1.0 * x[i] * x[i]);

% Closed-form L2 regression
float: a = (1.0*n * Sxy - Sx * Sy) / (1.0*n * Sxx - Sx * Sx);
float: b = (Sy / (1.0*n)) - a * (Sx / (1.0*n));

% Compute SSE for validation
float: SSE = sum(i in 1..n)(
  let { float: pred = a*(1.0*x[i]) + b } in
    (pred - (1.0*y[i])) * (pred - (1.0*y[i]))
);

solve satisfy;

output [
  "a (slope)     = ", show(a), "\n",
  "b (intercept) = ", show(b), "\n",
  "SSE           = ", show(SSE), "\n"
];
