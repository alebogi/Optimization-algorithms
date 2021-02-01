import matplotlib.pyplot as plt
import scipy.special as ss
import numpy as np

#ulaz f-je za x-osu
x = np.arange(0, 20, 0.1)

#red funkcije n = 1
line1 = ss.spherical_jn(1, x)

#red funkcije n = 2
line2 = ss.spherical_jn(2, x)

# plotting the line 1 points
plt.plot(x, line1, label="n=1")

# plotting the line 2 points
plt.plot(x, line2, label="n=2")

# naming the x axis
plt.xlim(0, 20)
plt.xlabel('x')
# naming the y axis
plt.ylabel('${J}_n(x)$')

# giving a title to my graph
plt.title("Spherical Bessel functions of the first kind for n = 1 and n = 2")

# show grid
plt.grid(b=True)

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()
