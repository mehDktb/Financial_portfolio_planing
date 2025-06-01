
% Parameters
int: n_samples;  % Number of data points
int: n_features; % Number of features (including intercept)
array[1..n_samples, 1..n_features] of float: X; % Feature matrix
array[1..n_samples] of float: y; % Target values

% Coefficients to solve for
array[1..n_features] of var float: beta;

% Normal equations: (X'X)β = X'y
constraint
    forall(j in 1..n_features) (
        sum([sum([X[k,i] * X[k,j] | k in 1..n_samples]) * beta[i] 
            | i in 1..n_features]) = 
        sum([X[k,j] * y[k] | k in 1..n_samples])
    );

solve satisfy;

% Prediction using last available data point
float: prediction = sum(j in 1..n_features)(X[n_samples,j] * beta[j]);

output [
    "Regression coefficients:\n",
    show(beta) ++ "\n\n",
    "Next week's predicted high: ", 
    show_float(5, 2, prediction)
];
