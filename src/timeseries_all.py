import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import statsmodels.api as sm


def scatter_plot_with_correlation_line(x, y, filepath=0 ):
    # Scatter plot
    plt.scatter(x, y)
    # Add correlation line
    axes = plt.gca()
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(axes.get_xlim()[0],axes.get_xlim()[1],100)
    plt.plot(X_plot, m*X_plot + b, '-')
    plt.show()
    # Save figure
    #plt.savefig(graph_filepath, dpi=300, format='png', bbox_inches='tight')



list_of_cols = [1,2,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52]
SNIP = pd.read_excel(io="../data/journal_SNIP_values.xlsx", parse_cols=list_of_cols, skip_footer=32000)


SNIP = SNIP.fillna(0) # removing all np.nan values because (np.nan == np.nan) is FALSE
#SNIP = SNIP[~np.isnan(SNIP)]
i = 0

sumval = []
for i in range(16):
    sumval.append(0)

#print sumval

jnames = []
x
journals = pd.DataFrame()

for index, row in SNIP.iterrows():
    if ( (row['1999 SNIP'] != 0) and (row['2000 SNIP'] != 0) and (row['2001 SNIP'] != 0) and (row['2002 SNIP'] != 0) and (row['2003 SNIP'] != 0) and (row['2004 SNIP'] != 0) and (row['2005 SNIP'] != 0) and (row['2006 SNIP'] != 0) and (row['2007 SNIP'] != 0) and (row['2008 SNIP'] != 0) and (row['2009 SNIP'] != 0) and (row['2010 SNIP'] != 0) and (row['2011 SNIP'] != 0) and (row['2012 SNIP'] != 0) and (row['2013 SNIP'] != 0) and (row['2014 SNIP'] != 0) ) : #checking if that journal has SNIP values
        #print "[DEBUG]" + row['Source Title']
        jnames.append(row['Source Title'])
        journals = journals.append( SNIP[SNIP['Source Title'] == row['Source Title'] ], ignore_index = True )
        i = i+ 1
print i

#print journals

for index, row in SNIP.iterrows():
    print "\n"
    for j in range(16):
        sumval[j] += row[j+2]
        print row[j+2],
        print " "

print sumval

for j in range(16):
    sumval[j] /= i

print "\n"
print sumval

File = open("../data/SNIP_avg.txt",'w')

for item in sumval:
  File.write("%s\n" % item)

journals = journals.rename(columns= lambda x: x.replace('SNIP', '')) #removing 'SNIP' from 'XXXX SNIP'
journals.drop(journals.columns[[1]], inplace=True, axis=1) # removing print ISSN column
journals = pd.melt(journals, id_vars='Source Title',var_name="SNIP Year", value_name="Value") # converting columns to rows
journals.drop(journals.columns[[0]],inplace=True,axis=1) #removing Source Title column
journals = pd.DataFrame(journals,dtype=float) # converting 'SNIP Year','Value' column into float type

print journals

#journals.to_csv("../data/journal_SNIP_info.csv",columns = (1,2))



'''


#DID NOT WORK - Univariate Spline
x = journals['SNIP Year']
y = journals['Value']
plt.plot(x, y, 'ro', ms=5)
spl = UnivariateSpline(x, y)
xs = np.linspace(1995, 2015, 1000)
plt.plot(xs, spl(xs), 'g', lw=3)
spl.set_smoothing_factor(0.5)
plt.plot(xs, spl(xs), 'b', lw=3)
plt.show()


#journals.plot(kind='scatter', x ='SNIP Year', y = 'Value')

#scatter_plot_with_correlation_line( journals['SNIP Year'],journals['Value'] )





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

'''



