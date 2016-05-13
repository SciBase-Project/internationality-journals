import pymongo
import ast
from subprocess import call
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

call(["brew","services","start","mongodb"])

# connecting to the database
client = pymongo.MongoClient("localhost", 27017)
# getting the table of the  
db = client.acm_aminer

data = {}

author_self_cites = {}
author_total_cites = {}
author_list = []
author_paper_count = {}

#indexing based on the index of an article
article_list = list(db['publications'].find())

call(["brew","services","stop","mongodb"])

for article in article_list:
    data[article['index']] = dict(article)
    try:
        for author  in article['authors']:
    		if author not in author_total_cites:
                author_total_cites[author] = 0
                author_self_cites[author] = 0
                author_paper_count[author] = 1
                author_list.append(author)
            else:
                author_paper_count[author] += 1
    except KeyError:
        pass

article_list = {}
for element in data:
 	for reference in list(data[element]['references']):
 		if reference == '':
 			continue
 		try:
 			for author in data[element]['authors']:
 				author_total_cites[author] += 1
 			cited = data[reference]
 		except KeyError:
 			continue
        try:
     		for author in data[element]['authors']:
     			if author in cited['authors']:
     				author_self_cites[author] += 1
        except KeyError:
            pass
with open('../../output/calc_ocq.csv','w') as outfile:
	for author in author_list:
		outfile.write(text_to_id(author) + ',' + str(author_total_cites[author]) + ',' + str(author_self_cites[author]) + '\n')
		if author_self_cites[author]!=0:
	 		print(text_to_id(author) + ' ' + str(author_total_cites[author]) + ' ' + str(author_self_cites[author]) +' '+ str(author_paper_count[authorau]))
# for element in data:
# 	for reference in list(data[element]['references']):
# 		if reference =='':
# 			continue
# 		try:
# 			jname = data[reference]['publication']
# 		except KeyError:
# 			continue
# 		author_total_cites[jname] += 1
# 		if jname == data[element]['publication']:
# 			author_self_cites[jname] += 1
			
# for name in journal_names:
# 	self = author_self_cites[name.strip('\n')]
# 	total = author_total_cites[name.strip('\n')]
# 	quotient = (total - self)/(total*1.0)
# 	print(name.strip('\n')+' '+str(total)+' '+str(self)+' '+str(quotient))
