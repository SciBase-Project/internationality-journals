
import pymongo

client = pymongo.MongoClient("localhost", 27017)

# db name - aminer
db = client.acm_aminer

# collection
db.shortened   

print "DB name: ", db.name
print "DB collection: ", db.publications


print "[INFO] Processing papers"

file = open("../data/ACM_Aminer.txt")
lines = file.readlines()
file.close()
papers = {}
i = 0
while i < len(lines) :
    paper = {}
    paper['references'] = []
    while lines[i] !=  '\n' :
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
        if line.startswith('#*') :
            i += 1
            continue #paper['title']        = line[len('#*'):]
        if line.startswith('#@') :     paper['authors']      = line[len('#@'):].split(',')
        if line.startswith('#o') :
            i += 1
            continue #paper['affiliations'] = line[len('#o'):]
        if line.startswith('#t') :
            i += 1
            continue #paper['year']         = line[len('#t'):]
        if line.startswith('#c') :     paper['publication']  = line[len('#c'):]
        if line.startswith('#!') :
            i += 1
            continue#paper['abstract']     = line[len('#!'):]
        if line.startswith('#%') :     paper['references'].append( line[len('#%'):] )
        print "line",i+1,"done"
        i += 1


    db.publications.insert_one(paper)

    print "[INFO] inserted into db paper", paper['index']

    i += 1

#file.close()

