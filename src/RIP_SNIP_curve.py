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


list_of_cols = [1,2,38,40,41,43,44,46,47,49,50,52,53] #2009-2014
list_of_cols = [1,7,8,10,11,13,14,16,17,19,20,22,23,25,26,28,29,31,32,34,35,38,40,41,43,44,46,47,49,50,52,53] #1999-2014
#SNIP = pd.read_excel(io="../data/journal_SNIP_values.xlsx",parse_cols=list_of_cols, skip_footer=0)
SNIP = pd.read_csv("../data/journal_SNIP_values.csv")


SNIP = SNIP.fillna(0) # removing all np.nan values because (np.nan == np.nan) is FALSE

i = 0

jnames = []

journals = pd.DataFrame()

for index, row in SNIP.iterrows():
    if(1):
    #if ( (row['2010 SNIP'] != 0) and (row['2011 SNIP'] != 0) and (row['2012 SNIP'] != 0) and (row['2013 SNIP'] != 0) and (row['2014 SNIP'] != 0) ) : #checking if that journal has SNIP values
        #print "[DEBUG]" + row['Source Title']
        jnames.append(row['Source Title'])
        journals = journals.append( SNIP[SNIP['Source Title'] == row['Source Title'] ], ignore_index = True )
        i = i+ 1
print i

#print journals

#journals = journals.rename(columns= lambda x: x.replace('SNIP', '')) #removing 'SNIP' from 'XXXX SNIP'
#journals = journals.rename(columns= lambda x: x.replace('IPP', '')) #removing 'IPP' from 'XXXX IPP'

#journals.drop(journals.columns[[1]], inplace=True, axis=1) # removing print ISSN column
#journals = pd.melt(journals, id_vars='Source Title',var_name="SNIP Year", value_name="Value") # converting columns to rows
#journals.drop(journals.columns[[1]], inplace=True, axis=1) # removing print ISSN column
journals.drop(journals.columns[[0]],inplace=True,axis=1) #removing Source Title column

print journals

journals = pd.DataFrame(journals,dtype=float) # converting 'SNIP Year','Value' column into float type

journals.to_csv("../data/SNIP_IPP_1994to2014_values")

'''
plt.plot(SNIP['2014 SNIP'],SNIP['2014 IPP'],'ro')
plt.plot(SNIP['2013 SNIP'],SNIP['2013 IPP'],'bo')
plt.plot(SNIP['2012 SNIP'],SNIP['2012 IPP'],'go')
plt.plot(SNIP['2011 SNIP'],SNIP['2011 IPP'],'yo')
plt.plot(SNIP['2010 SNIP'],SNIP['2010 IPP'],'bo')
plt.axis([-5, 40, -5, 40])
plt.legend()
plt.show()
'''

#poly_fit(x,y,4)
#scatter_plot(df,'2011 SNIP','2011 IPP')
#curvefit()


#journals.to_csv("../data/journal_SNIP_info.csv",columns = (1,2))





