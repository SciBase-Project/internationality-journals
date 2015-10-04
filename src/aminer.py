journals_to_consider = []


print "[INFO] Processing journals to be considered"

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
self_cites = {}
for ind in papers :
    paper = papers[ind]
    authors = paper['authors']
    for ref in paper['references'] :
        if ref not in papers :
            continue

        # get cited paper and authors
        cited_paper = papers[ref]
        cited_authors = cited_paper['authors']

        # check if common author exists
        if set(authors) & set(cited_authors) :
            if ind not in self_cites : self_cites[ind] = []
            self_cites[ind].append(ref)

print "[DEBUG] Number of self cited papers ", len(self_cites)
print "[INFO] Done finding self citations"



print "[INFO] Writing self cites to file"

import json
file = open("../output/aminer_self_cites.json", "w")
file.write(json.dumps(self_cites, indent=4))
file.close()

print "[INFO] Done writing self cites to file"

