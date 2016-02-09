__author__ = 'Sukrit'
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

file = open("../data/aminer_publications.txt")
lines = file.readlines()
papers = []
i = 0
while i < len(lines) :
    while lines[i] !=  '  \r\n' :
        line = lines[i].strip()

        '''
        #index ---- index id of this paper
        #* ---- paper title
        #@ ---- authors (separated by semicolons)
        #o ---- affiliations (separated by semicolons, and each affiliaiton corresponds to an author in order)
        #t ---- year
        #c ---- publication venue
        #% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
        #! ---- abstract
        '''
        if line.startswith('#c') :     papers.append(line[len('#c'):])


file.close()

print "[DEBUG] Number of papers ", len(papers)
print papers

'''
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

'''
