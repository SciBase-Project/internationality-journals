__author__ = 'Sukrit'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def poly_fit(x,y,deg):
    #POLYNOMIAL FIT
    # calculate polynomial
    z = np.polyfit(x, y, deg)
    f = np.poly1d(z)

    # calculate new x's and y's
    x_new = np.linspace(np.amin(x), np.amax(x), 50)
    y_new = f(x_new)

    plt.plot(x,y,'o', x_new, y_new)
    plt.xlim([np.amin(x), np.amax(x) ])
    plt.legend()
    plt.show()

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

def curvefit():
    x = np.linspace(0,4,50)
    y = func(x, 2.5, 1.3, 0.5)
    yn = y + 0.2*np.random.normal(size=len(x))

    popt, pcov = curve_fit(func, x, yn)

    plt.figure()
    plt.plot(x, yn, 'ko', label="Original Noised Data")
    plt.plot(x, func(x, *popt), 'r-', label="Fitted Curve")
    plt.legend()
    plt.show()

def scatter_plot(journals,SNIP_year,IPP_year):
    journals.plot(kind='scatter', x=SNIP_year,y=IPP_year)
    plt.legend()
    plt.show()



list_of_cols = [1,7,8,10,11,13,14,16,17,19,20,22,23,25,26,28,29,31,32,34,35,38,40,41,43,44,46,47,49,50,52,53]
SNIP = pd.read_excel(io="../data/journal_SNIP_values.xlsx",parse_cols=list_of_cols,skip_footer=16000)


SNIP = SNIP.fillna(0) # removing all np.nan values because (np.nan == np.nan) is FALSE

# print SNIP
i = 0

jnames = []

journals = pd.DataFrame()

# checking if SNIP values exist for these years, if yes, appending it to new DF
for index, row in SNIP.iterrows():
    if ( (row['2010 SNIP'] != 0) and (row['2011 SNIP'] != 0) and (row['2012 SNIP'] != 0) and (row['2013 SNIP'] != 0) and (row['2014 SNIP'] != 0) ) : #checking if that journal has SNIP values
        #print "[DEBUG]" + row['Source Title']
        jnames.append(row['Source Title'])
        journals = journals.append( SNIP[SNIP['Source Title'] == row['Source Title'] ], ignore_index = True )
        i = i+ 1
print i

print journals

#journals = pd.DataFrame(journals,dtype=float)
#journals.to_csv("../data/journal_SNIP_values.csv")

'''


#j= j.rename(columns= lambda x: x.replace('SNIP', '')) #removing 'SNIP' from '2011 SNIP'
#j= j.rename(columns= lambda x: x.replace('IPP', '')) #removing 'IPP' from '2011 IPP'

j.drop(j.columns[[1]], inplace=True, axis=1) #not needed anymore, to remove extra column
#j = pd.melt(j, id_vars='Source Title',var_name="SNIP Year", value_name="Value") #converting column to rows
j.drop(j.columns[[0]], inplace=True, axis=1)

journal = pd.DataFrame(j,dtype=float)
i = 0
j = 0

xarray = pd.DataFrame()
yarray = pd.DataFrame()

for i in range(0,30,2) : #putting SNIP and IPP values into two different arrays
    xarray = xarray.append( journal.ix[:,i], ignore_index = True )
    #print(journal.ix[:,i])
    yarray = yarray.append( journal.ix[:,i+1], ignore_index = True )
    #print(journal.ix[:,i+1])


print xarray
print yarray

plt.plot(xarray,yarray,'ro')
plt.show()


#journal = journalnew.append(journalnew2,ignore_index=True)

print journal

jname.drop(jname.columns[[1]], inplace=True, axis=1) # removing print ISSN column
jname.drop(jname.columns[[0]],inplace=True,axis=1) #removing Source Title column

jname = pd.DataFrame(jname,dtype=float) # converting 'SNIP Year','Value' column into float type

plt.plot(jname['2014 SNIP'],jname['2014 IPP'],'ro')
plt.plot(jname['2013 SNIP'],jname['2013 IPP'],'bo')
plt.plot(jname['2012 SNIP'],jname['2012 IPP'],'go')
plt.plot(jname['2011 SNIP'],jname['2011 IPP'],'yo')
plt.axis([-5, 40, -5, 40])
plt.legend()
plt.show()

#journals = journals.rename(columns= lambda x: x.replace('SNIP', '')) #removing 'SNIP' from 'XXXX SNIP'
#journals = journals.rename(columns= lambda x: x.replace('IPP', '')) #removing 'IPP' from 'XXXX IPP'

#journals.drop(journals.columns[[1]], inplace=True, axis=1) # removing print ISSN column
#journals = pd.melt(journals, id_vars='Source Title',var_name="SNIP Year", value_name="Value") # converting columns to rows
journals.drop(journals.columns[[1]], inplace=True, axis=1) # removing print ISSN column
journals.drop(journals.columns[[0]],inplace=True,axis=1) #removing Source Title column

#print journals

journals = pd.DataFrame(journals,dtype=float) # converting 'SNIP Year','Value' column into float type


plt.plot(SNIP['2014 SNIP'],SNIP['2014 IPP'],'ro')
plt.plot(SNIP['2013 SNIP'],SNIP['2013 IPP'],'bo')
plt.plot(SNIP['2012 SNIP'],SNIP['2012 IPP'],'go')
plt.plot(SNIP['2011 SNIP'],SNIP['2011 IPP'],'yo')
plt.axis([-5, 40, -5, 40])
plt.legend()
plt.show()

#poly_fit(x,y,4)
#scatter_plot(df,'2011 SNIP','2011 IPP')
#curvefit()


#journals.to_csv("../data/journal_SNIP_info.csv",columns = (1,2))


'''




jnames1 = "AAC: Augmentative and Alternative Communication"
jname2 = "Academic Medicine"

selected_journals = SNIP[SNIP["Source Title"] == jnames]
journal_2 = SNIP[SNIP["Source Title"] == jname2]

journal_2= journal_2.rename(columns= lambda x: x.replace('SNIP', ''))
selected_journals = selected_journals.rename(columns = lambda x: x.replace('SNIP',''))

selected_journals.drop(selected_journals.columns[[1]], inplace=True, axis=1)
selected_journals = pd.melt(selected_journals, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
selected_journals.drop(selected_journals.columns[[0]], inplace=True, axis=1)


journal_2.drop(journal_2.columns[[1]], inplace=True, axis=1)
journal_2 = pd.melt(journal_2, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
journal_2.drop(journal_2.columns[[0]],inplace=True,axis=1)

journalnew = pd.DataFrame(selected_journals,dtype=float)
journalnew2 = pd.DataFrame(journal_2,dtype=float)

journal = journalnew.append(journalnew2,ignore_index=True)

journal.plot(kind='scatter',x='SNIP Year',y='Value')

scatter_plot_with_correlation_line(journal['SNIP Year'],journal['Value'])





