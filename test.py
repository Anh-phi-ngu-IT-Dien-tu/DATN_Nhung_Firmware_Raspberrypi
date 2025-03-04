import matplotlib.pyplot as plt
import json

with open("test1.json", "r") as f:
    test = json.load(f)

test = [val[1] for val in test if len(val[1]) > 0]

x = [val[0][0] for val in test]
y = [val[0][1] for val in test]


plt.scatter(x, y)
ax=plt.gca()
ax.set_xlim(-2000,2000)
ax.set_ylim(-2000,2000)
plt.show()