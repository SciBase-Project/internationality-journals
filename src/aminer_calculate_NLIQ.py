import pymongo
import ast

# connecting to the database
client = pymongo.MongoClient("localhost", 27017)
# getting the table of the  
db = client.aminer
# list of journal names
journal_names = open('../output/Aminer_elsevier_189_jlist.txt','r').readlines()
#author_names = open("../data/")
data = {}

self_cites = {}
total_cites = {}

#indexing based on the index of an article
article_list = list(db['publications'].find())
for article in article_list:
	data[article['index']] = dict(article)
	if article['publication'] not in total_cites:
		total_cites[article['publication']] = 0
		self_cites[article['publication']] = 0
article_list={}
for element in data:
	for reference in list(data[element]['references']):
		if reference =='':
			continue
		try:
			jname = data[reference]['publication']
		except KeyError:
			continue
		total_cites[jname] += 1
		if jname == data[element]['publication']:
			self_cites[jname] += 1
for name in journal_names:
	self = self_cites[name.strip('\n')]
	total = total_cites[name.strip('\n')]
	quotient = (total - self)/(total*1.0)
	print(name.strip('\n')+' '+str(total)+' '+str(self)+' '+str(quotient))
