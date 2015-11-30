import json

with open('../output/aminer_cites.json') as data_file:
        data = json.load(data_file)

for publication in data :
    papers = data[publication]

    count = 0
    for paper in papers :
        cites = data[publication][paper]
        for cite in cites :

            # true if self cite - atleast one common author name
            type = cite['self']

            if type :
                count += 1

    # print "[DEBUG] Self cite count with atleast one common author;", "publication : ", publication, "; count : ", count
    print "[DEBUG] Publication : ", publication, "; count : ", count