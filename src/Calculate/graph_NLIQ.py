import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

with open('../../output/NLIQ.txt','r') as infile:
	data = infile.readlines()
x = []
y = []
for  record in data:
	x.append(record.split('\t')[0])
	y.append(record.split('\t')[1])
plt.plot(x,y,marker="o")
plt.ylabel('Number of Papers')
plt.xlabel('NLIQ')
plt.show()
"""
index=[0,1,2,3]
url=['Health Professions','Physics and Astronomy','Earth and Planetory Sciences','Computer Science']
for i in index :
   x1=[]
   y1=[]
   f = open("avgathr"+str(i)+".txt","r")
   lines = f.readlines()
   for line in lines :
      line=line.strip()
      x1.append(line.split('\t')[0])
      y1.append(line.split('\t')[1])
   labl=plt.plot(x1,y1,marker="o",label=(url[i]))
   f.close()
legend = plt.legend(loc='best', shadow=True, fontsize='large')
legend.get_frame().set_facecolor('#00FFCC')
plt.ylabel('Number of Authors per post')
plt.xlabel('Year')
plt.show()
"""