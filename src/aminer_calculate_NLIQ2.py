import pymongo
# connecting to the database
client = pymongo.MongoClient("localhost", 27017)
# getting the table of the
db = client.aminer
# list of journal names
db.publications

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

data = {}

article_list = list(db.publications)

for article in article_list:
	if article['publication'] in journal_list :

        if article['authors'] in author_list :
            if article['publication'] not in data:
		        data[article['publication']] = []

            data[article['publication']].append(article)




