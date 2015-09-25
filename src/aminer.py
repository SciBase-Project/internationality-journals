file = open("../data/aminer_publications.txt")

journals = {}

for line in file.readlines() :
    line = line.strip()
    journal_name = ""
    if line.startswith("#c") :
        journal_name = line[2:]
        if journal_name not in journals :
            journals[journal_name] = 1
        else :
            journals[journal_name] += 1

print journals