import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(6, 6))
A = [0, 1]
B = [1, 1]
C = [1, 0]
D = [0, 0]
x_values = [A[0], B[0], C[0], D[0], A[0]]
y_values = [A[1], B[1], C[1], D[1], A[1]]
plt.plot(x_values, y_values, 'b')
plt.show()