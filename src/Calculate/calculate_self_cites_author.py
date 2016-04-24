

import re
import unicodedata
import ast

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    text = re.sub('_',' ',text)
    return text



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


file = open("../data/aminer_tiny.txt")
lines = file.readlines()
papers = {}
i = 0

jcount = 0
journal_unique = set()
flag = False


# references -> the list of references a paper makes to other papers
# citation -> a list of papers that have cited/referred this paper
citations = {} #{ "index" : { 'authors' : [] , 'references' : [] , 'cited_by' : [] , 'referred_count' : 0 } }

while i < len(lines) :
    paper = {}
    paper['references'] = []
    paper['authors'] = []
    while lines[i] !='  \n':
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

        if line.startswith('#index') : paper['index'] = line[len('#index'):]

        #simplifying author names
        if line.startswith('#@') :
            temp_list      = line[len('#@'):].split(',')
            for author in temp_list :
                paper['authors'].append(text_to_id(author))


        if line.startswith('#%') :
            paper['references'].append( line[len('#%'):] )
        #print "line",i+1,"done"

        i += 1
        if i == len(lines) :
            break


    if 'index' in paper : # to account for ones with no 'index' key
        if paper['index'] not in citations : # if index doesn't already exist
            citations[paper['index']] = { 'authors' : [] , 'references' : [] , 'cited_by' : [] , 'referred_count' : 0 }

        citations[paper['index']]['authors'] = paper['authors'] # adding authors
        citations[paper['index']]['references'] = paper['references'] # adding list of references


        for ref in paper['references'] : # for each reference
            cite = []
            if len(ref) != 0 : # if there are references
                if ref not in citations : # if index doesn't exist in citations
                    cite.append(paper['index'])
                    citations[ref] = { 'authors' : [] , 'references' : [] , 'cited_by': cite , 'referred_count' : 1 } # adding one citation
                else :
                    citations[ref]['referred_count'] += 1 # increasing citation count, as it already exists
                    if paper['index'] not in citations[ref]['cited_by'] : # unique cited_by
                        citations[ref]['cited_by'].append(paper['index']) # adding new citation to list

        print "[INFO] inserted into db paper", paper['index'], "\n\n"

    i += 1
    #if i == len(lines) :
    #       break

file.close()

print citations

