import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

with open('../../output/NLIQ.txt','r') as infile:
	data = infile.readlines()
x = []
y = []
for  record in data:
	x.append(record.split('\t')[0])
	y.append(record.split('\t')[1])
plt.plot(x,y,'o')
plt.ylabel('Number of Papers')
plt.xlabel('NLIQ')
plt.show()