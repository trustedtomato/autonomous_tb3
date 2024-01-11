import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes as axes

msft = pd.read_csv('sim-results.csv', delimiter=' ')
msft['t'] = msft['t'] - 32.99
msft.insert(2, "ETA + t", msft['t'] + msft['ETA'], True)

msft.plot(0, [1, 2, 3], subplots=True, xlim=(0), ylim=(0), grid=True)
plt.show()

msft2 = msft.iloc[11:]
msft2.plot(0, [1, 2, 3], subplots=True, xlim=(0), grid=True)
plt.show()