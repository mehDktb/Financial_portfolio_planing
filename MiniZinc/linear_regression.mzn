% regression.mzn

int: n_samples;
int: n_features;
array[1..n_samples, 1..n_features] of float: X;
array[1..n_samples] of float: y;

array[1..n_features] of var float: beta;

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

var float: prediction = sum(j in 1..n_features)(X[n_samples,j] * beta[j]);

output [
  "Regression coefficients:\n",
  show(beta) ++ "\n\n",
  "Prediction for last row: ", 
  show(prediction)
];
