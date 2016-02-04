import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


list_of_cols = [1,2,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49]
SNIP = pd.read_excel(io="../data/journal_SNIP_values.xlsx", parse_cols=list_of_cols, skip_footer=32000)

jname = "AAC: Augmentative and Alternative Communication"

selected_journal = SNIP[SNIP["Source Title"]==jname] #make sure it exists!

selected_journal.drop(selected_journal.columns[[1]], inplace=True, axis=1) # removes Print ISSN
selected_journal = pd.melt(selected_journal, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
selected_journal.drop(selected_journal.columns[[0]], inplace=True, axis=1)

selected_journal.plot()
plt.legend()
plt.show()


jnames = []
for journal in jnames:
	selected_journal.append( SNIP[SNIP["Source Title"]==journal] )

selected_journal.drop(selected_journal.columns[[1]], inplace=True, axis=1) # removes Print ISSN
selected_journal = pd.melt(selected_journal, id_vars='Source Title',var_name="SNIP Year", value_name="Value")
selected_journal.drop(selected_journal.columns[[0]], inplace=True, axis=1)

selected_journal.plot()
plt.legend()
plt.show()





