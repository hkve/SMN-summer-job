import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

n = 100
x = np.random.uniform(0,2*np.pi,n)
y = np.sin(x) + np.random.normal(0,0.1,n)

sort_idx = np.argsort(x)
x = x[sort_idx]
y = y[sort_idx]

yhat = savgol_filter(y, 11, 2)

plt.plot(x,y, c="r")
plt.plot(x, yhat)
plt.show()