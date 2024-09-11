# Построй диаграмму рассеяния для двух наборов
# случайных данных, сгенерированных с помощью функции
# `numpy.random.rand`

import numpy as np
import matplotlib.pyplot as plt

x = np.random.rand(50)
y = np.random.rand(50)
plt.scatter(x, y)
plt.show()

