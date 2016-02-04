import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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





