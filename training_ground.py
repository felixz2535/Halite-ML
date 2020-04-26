import os
import matplotlib.pyplot as plt
from statistics import mean



all_files = os.listdir('training_data')

halite_amounts = []

for f in all_files:
        halite_amount = int(f.split("-")[0])
        halite_amounts.append(halite_amount)


plt.hist(halite_amounts , 5)
plt.show()
