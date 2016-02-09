__author__ = 'Sukrit'
import csv
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit


ELElist = []
with open('../data/Elsevier_journal_list.csv', 'r') as file :
    x = file.readlines()
    for line in x :
        #print line
        line = line.replace('&','and') #converting & to 'and' [UGH]
        ELElist.append(line.rstrip()) #remove whitespaces



import pymongo
client = pymongo.MongoClient("localhost", 27017)
# db name - aminer
db = client.aminer
# collection
db.publications

jlist = []
i = 0

for jname in ELElist :
    if db.publications.find(filter = {'publication' : jname},limit = 1) != None :
        jlist.append(jname)
        print jname
        i += 1
print i

with open ("../output/both_journal_list.txt","w")as file:
    for line in jlist:
        file.write(line+"\n")

'''
cursor = db.publications.find()
for document in cursor :
    if document['publication'] not in jlist :
        if document['publication'] in ELElist :
            jlist.append(document['publication'])
            print document['publication']
'''



'''
citable_items = list(db.publications.find({"publication" : P})
citable_items_ids = []
for cite in citable_items : citable_items_ids.append(cite['index'])
'''


#print "[DEBUG] Number of papers ", len(papers)
#print papers






