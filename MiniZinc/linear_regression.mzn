% regression.mzn - Updated for forecasting

% Training data
int: n_samples;
int: n_features;
array[1..n_samples, 1..n_features] of float: X;
array[1..n_samples] of float: y;

% Prediction data (features for forecasting)
array[1..1, 1..n_features] of float: X_predict;

% Regression coefficients to be learned
array[1..n_features] of var float: beta;

% Normal equations constraint (solving X'X * beta = X'y)
constraint
  forall(j in 1..n_features) (
    let {
      var float: lhs = sum(i in 1..n_features)(
        sum(k in 1..n_samples)(X[k,i] * X[k,j]) * beta[i]
      );
      float: rhs = sum(k in 1..n_samples)(X[k,j] * y[k])
    } in
    lhs = rhs
  );

solve satisfy;

% Make prediction using the separate prediction features
var float: prediction = sum(j in 1..n_features)(X_predict[1,j] * beta[j]);

output [
  "Regression coefficients:\n",
  show(beta) ++ "\n\n",
  "Future prediction: ",
  show(prediction) ++ "\n"
];