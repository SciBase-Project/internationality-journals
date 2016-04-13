'''
Please put 'aminer_publications.txt' in 'data' folder
'''


import collections



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

'''

print "\n\n[INFO] Processing articles for publication venues.\n"
print "------------------------------------------------------------------------------------------------\n\n"
file = open("../data/aminer_publications.txt")
lines = file.readlines()
papers = {}
i = 0
article_count = 0
pub_count = 0
publication_article_count = collections.OrderedDict()
publication_venue = set()

while i < len(lines) :
    #line = lines[i].strip()

    #AMINER FORMAT
    #index ---- index id of this paper
    #* ---- paper title
    #@ ---- authors (separated by semicolons)
    #o ---- affiliations (separated by semicolons, and each affiliaiton corresponds to an author in order)
    #t ---- year
    #c ---- publication venue
    #% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
    #! ---- abstract

    #print line[len('#c'):]
    if lines[i].startswith('#c') :
        article_count +=1

        #publication_venue.add(lines[i][len('#c'):])

        if lines[i][len('#c'):] not in publication_venue :
            publication_venue.add(lines[i][len('#c'):])
            pub_count += 1
            print("[INFO] Publication venue %d : %s" %(pub_count, lines[i][len('#c'):]))

            publication_article_count[lines[i][len('#c'):]] = 1

        else :

            publication_article_count[lines[i][len('#c'):]] += 1

    i += 1


file.close()

print "\n------------------------------------------------------------------------------------------------"

print "\n\n[INFO] Done processing articles for publication venues.\n\n"
print "[DEBUG] Total number of articles: ", article_count
print "[DEBUG] Total number of unique publication venues: ", len(publication_venue)

print "\n------------------------------------------------------------------------------------------------"

print "[DEBUG] Top 10 publications:\n"

count = 0
sort_pub = sorted(publication_article_count, key = publication_article_count.__getitem__,reverse = True)
publication_article_count_sorted = collections.OrderedDict()

for publication in sort_pub :
    publication_article_count_sorted[publication.strip()] = publication_article_count[publication]



for key, value in publication_article_count_sorted.iteritems() :
    print key, ":" , value
    count += 1
    if (count > len(publication_article_count)) or count > 10 :
        break


# DOES NOT WORK YET :/
with open("../output/both_journal_list.txt") as file :
    lines = file.readlines()
    for line in lines :
        if line.strip() in publication_venue :
            print line

