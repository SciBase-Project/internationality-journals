__author__ = 'Sukrit'
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

f = open('../data/journal_snip.txt', 'r') #reading list of journals present in Aminer
x = f.readlines()
xn = []
for line in x:
    line = line.replace('&','and') #converting & to 'and' [UGH]
    xn.append(line.rstrip())



SNIP = pd.read_csv("../data/journal_SNIP_values.csv")


journals = SNIP['Source Title'] #taking only 'Source Title' column
jlist = []
i = 0
j = 0

for jname in journals :
    for name in xn :
        if jname == name :
            jlist.append(jname)
            i += 1

#print xn
#print len(xn)
#print jlist
#print i

SNIP_2 = pd.DataFrame()

#now we corroborate SNIP values.

for name in jlist :
        SNIP_2 = SNIP_2.append(SNIP[ SNIP['Source Title'] == name ],ignore_index = True) #copy all SNIP/IPP values for which we have citations in Aminer

#print SNIP_2

SNIP_2 = SNIP_2.fillna(0)

SNIP_2010 = SNIP_2[['Source Title','2010 SNIP']].copy() #copying 'Source Title' and '2010 SNIP' columns to new df

our_SNIP = {'Applied Mathematics and Computation': 0 , 'Artificial Intelligence' :1.99047619048 , 'Artificial Intelligence in Medicine' : 0.707346904582 , 'Automatica' : 0.373679952833 , 'Computer Communications' :0.42907910953 , 'Computer Methods and Programs in Biomedicine' :0.379046231074 , 'Computer Networks' : 0.749387157754 , 'Computer Vision and Image Understanding' :1.67294857909 , 'Computers and Education' : 0.704265888257, 'Computers and Geosciences' : 0.188574973214, 'Computers and Graphics' :0.442495274102 , 'Computers and Mathematics with Applications' : 0.329331757583 , 'Computers and Security' : 0 , 'Computers in Human Behavior' :0.650123718628 , 'Discrete Mathematics' : 0 , 'Environmental Modelling and Software' :0.367386629266 ,'Expert Systems with Applications' : 0.588827994966,'Future Generation Computer Systems' :1.07051816557 ,'Games and Economic Behavior' :0.00331943617232,'Information and Management' :  1.03949275362,'Information Processing Letters' : 0 , 'Information Sciences' : 0.453232588419, 'Journal of Approximation Theory' :  0.162687560813, 'Mathematics and Computers in Simulation' :0.173084886128 , 'Neural Networks' :0.678374260303 , 'Neurocomputing' : 0.634644582471, 'Parallel Computing' : 0.712270531401, 'Pattern Recognition' : 1.17715942029, 'Performance Evaluation' :0.713109730849 , 'Robotics and Autonomous Systems' :  0.739277818718, 'Science of Computer Programming' : 0  , 'Signal Processing' :0.554988312295 , 'Speech Communication' :0.540711462451 , 'Systems and Control Letters' : 0 }



print
xarray = []
yarr = []
yarray = []
i = 0
print SNIP_2010

print jlist
#jlist.remove("Games and Economic Behavior")
for name in jlist :
    if ( our_SNIP[name] != 0 and SNIP_2010['2010 SNIP'][SNIP_2010['Source Title'] == name ].values != 0 ) :
        xarray.append(our_SNIP[name])
        yarr.append(SNIP_2010['2010 SNIP'][SNIP_2010['Source Title'] == name ].values)

#plt.plot(xarray,yarray,'ro')

#plt.plot(xarray, np.poly1d(np.polyfit(xarray, yarray, 1))(xarray))
#plt.show()
yarr = [float(i) for i in yarr]
for item in yarr :
    yarray.append(item)

print yarray
print "\n\n"
data = [xarray,yarray]

with open('../data/SNIP_ourSNIP2.csv','wb') as f:
    out = csv.writer(f, delimiter=',',quoting=csv.QUOTE_ALL)
    out.writerows(zip(*data))

