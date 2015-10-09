'''
Please put 'aminer_publications.txt' in 'data' folder
'''

print "[INFO] Processing journals to be considered"

journals_to_consider = []
file = open("../data/journal_snip.txt")
for line in file.readlines() :
    line = line.strip()
    journal = line.split(" : ")[0]
    journals_to_consider.append(journal)
file.close()

print "[DEBUG] Journals : ", journals_to_consider
print "[INFO] Done processing journals to be considered"



print "[INFO] Processing papers"

file = open("../data/aminer_publications.txt")
lines = file.readlines()
papers = {}
i = 0
while i < len(lines) :
    paper = {}
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

        if line.startswith('#index') : paper['index']        = line[len('#index'):]
        if line.startswith('#*') :     paper['title']        = line[len('#*'):]
        if line.startswith('#@') :     paper['authors']      = line[len('#@'):].split(',')
        if line.startswith('#o') :     paper['affiliations'] = line[len('#o'):]
        if line.startswith('#t') :     paper['year']         = line[len('#t'):]
        if line.startswith('#c') :     paper['publication']  = line[len('#c'):]
        if line.startswith('#!') :     paper['abstract']     = line[len('#!'):]
        if line.startswith('#%') :
            if 'references' not in paper : paper['references'] = []
            paper['references'].append( line[len('#%'):] )

        i += 1

    if paper['publication'] in journals_to_consider :
        index = paper['index']

        # store papers by index
        papers[index] = paper

    i += 1

file.close()

print "[DEBUG] Number of papers ", len(papers)
print "[INFO] Done processing papers"



print "[INFO] Finding self citations"
edge_list = []
self_cites = {}
for ind in papers :
    paper = papers[ind]
    publication = paper['publication']
    authors = paper['authors']
    for ref in paper['references'] :
        if ref not in papers :
            continue

        # get cited paper and authors
        cited_paper = papers[ref]
        cited_authors = cited_paper['authors']
        cited_publication = cited_paper['publication']

        # check if common author exists
        if set(authors) & set(cited_authors) :
            if publication not in self_cites : self_cites[publication] = {}
            if ind not in self_cites[publication] : self_cites[publication][ind] = []
            self_cites[publication][ind].append({"index" : ref, "publication" : cited_publication})

            # adding to edge list
            # type 1 - common authors / 0 - no common authors
            src = ind
            dest = ref
            type = 1
            edge_list.append( [src, dest, type] )

        else:
            # adding to edge list
            # type 1 - common authors / 0 - no common authors
            src = ind
            dest = ref
            type = 0
            edge_list.append( [src, dest, type] )


print "[DEBUG] Number of self cited papers ", len(self_cites)
print "[INFO] Done finding self citations"



print "[INFO] Writing self cites to file"

import json
file = open("../output/aminer_self_cites.json", "w")
file.write(json.dumps(self_cites, indent=4))
file.close()

print "[INFO] Done writing self cites to file"



print "[INFO] Writing edge list to file"

import csv
with open('../output/aminer_edge_list.csv', 'w') as csvfile:
    fields = ['src', 'dest', 'type']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    for entry in edge_list :
        writer.writerow(dict(zip(fields, entry)))

print "[INFO] Done writing edge list to file"