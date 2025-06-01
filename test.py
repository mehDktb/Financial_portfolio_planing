# e.g. Python + scikit-learn
from sklearn.linear_model import LinearRegression
import numpy as np

x = np.array([1,2,3,4,5]).reshape(-1,1)
y = np.array([2,4,5,4,5])

model = LinearRegression().fit(x, y)
print("a =", model.coef_[0], " b =", model.intercept_)

