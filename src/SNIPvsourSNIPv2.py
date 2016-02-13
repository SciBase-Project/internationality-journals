__author__ = 'Sukrit'
import pandas as pd
import csv



f = open('../output/both_journal_list.txt', 'r') #reading list of journals present in Aminer and Elesevier
x = f.readlines()
f.close()
bothjs = []

for line in x:
    bothjs.append(line.rstrip()) # list of common journals, removing '\n'

# OUR SNIP
our_SNIP = pd.read_csv('../output/SNIP_all_journals.csv',usecols=[1,3]) # reading SNIP values calculated by US
our_SNIP.sort_values('Jname',inplace = True) #sorting alphabetically

our_SNIP = our_SNIP[ our_SNIP['SNIP'] != 0 ]
our_SNIP2 = pd.DataFrame()
our_SNIP2 = our_SNIP2.append(our_SNIP,ignore_index = True) #resetting index value

our_SNIP = our_SNIP2

oSNIPnames = our_SNIP['Jname']
#print our_SNIP

# SNIP

SNIP = pd.read_csv("../data/journal_SNIP_values.csv")


journals = SNIP['Source Title'] #taking only 'Source Title' column
SNIPlist = []

'''
for jname in oSNIPnames :
    for name in journals :
        if jname == name :
            SNIPlist.append(jname)

'''

SNIP_2 = pd.DataFrame()

#now we corroborate SNIP values.

for name in oSNIPnames :
        SNIP_2 = SNIP_2.append(SNIP[ SNIP['Source Title'] == name ],ignore_index = True) # copy all SNIP/IPP values for which we have citations in Aminer

#print SNIP_2

SNIP_2010 = SNIP_2[['Source Title','2010 SNIP']].copy() # copying 'Source Title' and '2010 SNIP' columns to new df

SNIP_2010 = SNIP_2010.fillna(0) # replacing NaN values with 0

#print SNIP_2010

#print our_SNIP

xarray = []
xarray2 = []
yarray = []
yarray2 = []
names = []

for name in oSNIPnames :
    a = our_SNIP['SNIP'][ our_SNIP['Jname']== name ].values
    b = SNIP_2010['2010 SNIP'][ SNIP_2010['Source Title'] == name ].values
    #if ( a != 0 and a <10 and b != 0 and b < 10 and a > 0.01 ) :
    if ( a != 0 and b!= 0 ) :
        xarray.append(our_SNIP['SNIP'][our_SNIP['Jname']== name ].values)
        yarray.append(SNIP_2010['2010 SNIP'][SNIP_2010['Source Title'] == name ].values)
        names.append(name)


yarray = [float(i) for i in yarray]
for item in yarray :
    yarray2.append(item)

xarray = [float(i) for i in xarray]
for item in xarray :
    xarray2.append(item)


print len(xarray)
print len(yarray)
print len(names)
print "\n\n"
data = [names,xarray,yarray]

with open('../data/SNIP_ourSNIP_ALL.csv','wb') as f:
    out = csv.writer(f, delimiter=',',quoting=csv.QUOTE_ALL)
    out.writerows(zip(*data))