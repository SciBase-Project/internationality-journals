'''
Please put 'aminer_publications.txt' in 'data' folder
Used to extract all unique authors from Aminer
'''


import collections
import json
import os
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


print "\n\n[INFO] Processing articles for author names.\n"
print "------------------------------------------------------------------------------------------------\n\n"
file = open("../../data/ACM_Aminer.txt")
journals = open("../../output/ACM_Elsevier_journal_list_curated_v2")

lines = file.readlines()
papers = {}
i = 0
article_count = 0
pub_count = 0

author_article_count = collections.OrderedDict()
author_set = set()
author_individual = set()
author_set_count = 0

while i < len(lines) :
    #line = lines[i].strip()

    #AMINER FORMAT
    #index ---- index id of this paper
    #* ---- paper title
    #@ ---- authors (separated by commas)
    #o ---- affiliations (separated by semicolons, and each affiliaiton corresponds to an author in order)
    #t ---- year
    #c ---- publication venue
    #% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
    #! ---- abstract

    #print line[len('#c'):]
    if lines[i].startswith('#c') :

        print len(lines[i])

        if len(lines[i]) <= 3 : #no publication venue exists
            i += 1
            continue


        article_count +=1
        #print lines[i]

        if lines.find(journal)
        #if apublication venue not already present
        if lines[i][len('#c'):] not in author_set :
            author_set.add(lines[i][len('#c'):])
            pub_count += 1
            print("[INFO] Publication set %d : %s" %(pub_count, lines[i][len('#c'):]))

            author_article_count[lines[i][len('#c'):]] = 1

        else :

            author_article_count[lines[i][len('#c'):]] += 1

    i += 1


file.close()

# getting individual authors from author value in #@
for auth in author_set :
    author_set_count += 1
    author_temp = auth.strip("\n").split(",")
    for author in author_temp :
        if author not in author_individual :
            author_individual.add(text_to_id(author))



print "\n------------------------------------------------------------------------------------------------"


print "\n\n[INFO] Done processing articles for author names.\n\n"
print "[DEBUG] Total number of articles: ", article_count
print "[DEBUG] Total number of uniqe author sets: ", author_set_count
print "[DEBUG] Total number of authors: ", len(author_individual)
print "[DEBUG] Saving author names to file.\n"


print "\n------------------------------------------------------------------------------------------------"

'''
with open("../../data/ACM_author_list_Aminer.txt",'w') as file :
    for author in author_individual :
        file.write(author)
        file.write("\n")
'''
