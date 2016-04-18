

import re


print "[INFO] Processing papers"

journal_list = set(open("../output/Aminer_elsevier_189_jlist.txt").readlines())
journal_list2 = set()
for journal in journal_list :
    journal_list2.add(journal.strip("\n"))
journal_list = journal_list2

author_list = set(open("../data/author_list_aminer.txt").readlines())

author_list2 = set()
for author in author_list :
    author_list2.add(author.strip("\n"))
author_list = author_list2


file = open("../data/aminer_publications.txt")
lines = file.readlines()
papers = {}
i = 0

jcount = 0
journal_unique = set()
flag = False



while i < len(lines) :
    paper = {}
    paper['references'] = []
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


        if line.startswith('#c') :
            temp = re.sub('#c','',line)
            if temp in journal_list :
                paper['publication']  = line[len('#c'):]
                flag = True
                if temp not in journal_unique :
                    journal_unique.add(temp)
                    jcount += 1
                    print "[DEBUG]Journal #",jcount,"added: ",temp


        if line.startswith('#!') :     paper['abstract']     = line[len('#!'):]
        if line.startswith('#%') :     paper['references'].append( line[len('#%'):] )
        i += 1


    if flag == True :
        for item in paper:
            db.publications.insert_one(paper)
    print "[INFO] inserted into db paper", paper['index']

    i += 1

file.close()

