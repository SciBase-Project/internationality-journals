import pymongo
import ast

import re
import unicodedata

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


# connecting to the database
client = pymongo.MongoClient("localhost", 27017)
# getting the table of the  
db = client.aminer

data = {}

self_cites = {}
total_cites = {}
author_list = []

#indexing based on the index of an article
article_list = list(db['publications'].find())
for article in article_list:
	data[article['index']] = dict(article)
	for author  in article['authors']:
		if author not in total_cites:
			total_cites[author] = 0
			self_cites[author] = 0
			author_list.append(author)
 
for element in data:
 	for reference in list(data[element]['references']):
 		if reference == '':
 			continue
 		try:
 			for author in data[element]['authors']:
 				total_cites[author] += 1
 			cited = data[reference]
 		except KeyError:
 			continue
 		for author in data[element]['authors']:
 			if author in cited['authors']:
 				self_cites[author] += 1
with open('../../output/calc_ocq.csv','w') as outfile:
	for author in author_list:
		outfile.write(text_to_id(author) + ',' + str(total_cites[author]) + ',' + str(self_cites[author]) + '\n')
		if self_cites[author]!=0:
	 		print(text_to_id(author) + ' ' + str(total_cites[author]) + ' ' + str(self_cites[author]))
# for element in data:
# 	for reference in list(data[element]['references']):
# 		if reference =='':
# 			continue
# 		try:
# 			jname = data[reference]['publication']
# 		except KeyError:
# 			continue
# 		total_cites[jname] += 1
# 		if jname == data[element]['publication']:
# 			self_cites[jname] += 1
			
# for name in journal_names:
# 	self = self_cites[name.strip('\n')]
# 	total = total_cites[name.strip('\n')]
# 	quotient = (total - self)/(total*1.0)
# 	print(name.strip('\n')+' '+str(total)+' '+str(self)+' '+str(quotient))
