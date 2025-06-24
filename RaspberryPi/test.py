import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import json
import math
import numpy as np



with open("test1.json", "r") as f:
    test = json.load(f)

# with open("test2.json", "r") as f:
#     test2 = json.load(f)

test = [val[1] for val in test if len(val[1]) > 0]

x = [val[0][0] for val in test]
y = [val[0][1] for val in test]


for i in range(len(x)):
    r = math.sqrt(x[i]**2 + y[i]**2)
    phi = math.atan2(y[i], x[i]) + 0.10337803649523618
    x[i] = r*math.cos(phi)
    y[i] = r*math.sin(phi)

# ak,ck=np.polyfit(np.array(x),np.array(y),1)
# print(math.atan(ak))

# circle = Circle((0, 0), 779.559, fill = False)

plt.scatter(x, y)
ax=plt.gca()
# ax.add_artist(circle)
ax.set_xlim(-4000,4000)
ax.set_ylim(-4000,4000)
plt.show()