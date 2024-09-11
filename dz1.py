#  Создай гистограмму для случайных данных,
#  сгенерированных с помощью функции `numpy.random.normal`
import numpy as np
import matplotlib.pyplot as plt

data = np.random.normal(0, 1, 1000)

plt.hist(data, bins=20)
plt.show()