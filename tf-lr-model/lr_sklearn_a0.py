import numpy as np
import random
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def linear_regression_trial(n=25):
    k = random.random()
    b = random.random() * 1
    x = np.linspace(0, n, n)
    y = [item * k + (random.random() - 0.5) * k * 5 + b for item in x]
    true_y = [item * k for item in x]

    # LR fitting
    model = LinearRegression()
    model.fit(np.reshape(x, [len(x), 1]), np.reshape(y, [len(y), 1]))
    yy = model.predict(np.reshape(x, [len(x), 1]))

    # Plotting
    plt.figure()
    kk = model.coef_[0][0]
    bb = model.intercept_[0]
    plt.title('Linear Regression Trial \n True: y='
              + str(k)[0:4] + 'x +' + str(b)[0:4]
              + '\nPredicted:y=' + str(kk)[0:4] + 'x +' + str(bb)[0:4])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.plot(x, y, 'r.')
    plt.plot(x, yy, 'g-')
    plt.show()


if __name__ == '__main__':
    linear_regression_trial()
