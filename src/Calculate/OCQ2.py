import pymongo
import ast
from subprocess import call
import re
import unicodedata
import json

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

from os import system
system("brew services start mongodb")
# connecting to the database
client = pymongo.MongoClient("localhost", 27017)
# getting the table of the
db = client.acm_aminer

data = {}

journal_author_dict = {}
author_self_cites = {}
author_total_cites = {}
author_list = []
author_paper_count = {}
journal_list = []

#indexing based on the index of an article
article_list = list(db['publications'].find())
count = 0

system("brew services stop mongodb")

print(len(article_list))
for article in article_list:
    count += 1
    data[article['index']] = dict(article)
    # try:
    #     if article['publication'] not in journal_list:
    #         journal_author_dict[article['publication']] = []
    #         journal_list.append(article['publication'])
    #     for author  in article['authors']:
    #         author = text_to_id(author)
    #         if author not in author_total_cites:
    #             author_total_cites[author] = 0
    #             author_self_cites[author] = 0
    #             author_paper_count[author] = 1
    #             author_list.append(author)
    #         else:
    #             author_paper_count[author] += 1
    #         if author not in journal_author_dict[article['publication']]:
    #             journal_author_dict[article['publication']].append(author)
    # except KeyError:
    #     pass
    # count += 1
    print('article ' + str(count) + ' done')

with open('../../data/OCQ_temp_data/Journal_author.json','r') as outfile:
   journal_author_dict = json.load(outfile)

with open('../../data/OCQ_temp_data/author_selfcites.json','r') as outfile:
    author_self_cites = json.load(outfile)

with open('../../data/OCQ_temp_data/author_total_cites.json','r') as outfile:
    author_total_cites = json.load(outfile)

with open('../../data/OCQ_temp_data/journal_list.json','r') as outfile:
    journal_list = json.load(outfile)['list']

# with open('../../data/OCQ_temp_data/data.json','w') as outfile:
#     json.dump({'data':data},outfile)

print("calculating the citation counts")

article_list = {}
for element in data:
 	for reference in list(data[element]['references']):
 		if reference == '':
 			continue
 		try:
 			for author in data[element]['authors']:
 				author_total_cites[author] += 1
 			cited = data[reference]
 		except Exception:
 			continue
        try:
     		for author in data[element]['authors']:
     			if author in cited['authors']:
     				author_self_cites[author] += 1
        except Exception:
            pass

with open('../../data/OCQ_temp_data/author_selfcites.json','w') as outfile:
    json.dump(author_self_cites,outfile)

with open('../../data/OCQ_temp_data/author_total_cites.json','w') as outfile:
    json.dump(author_total_cites,outfile)

with open('../../output/ACM_Elsevier_journal_list.txt','r') as outfile:
    required_journals = outfile.readlines()

with open('../../output/calc_ocq.csv','w') as outfile:
    for journal in required_journals:
        try:
            total_quotient = 0.0
            normalized_quotient = 0.0
            for author in journal_author_dict[journal.strip('\n')]:
                if author_total_cites[author]!=0:
                    quotient = (author_total_cites[author] - author_self_cites[author])/(1.0 * author_total_cites[author])
                    total_quotient += quotient
            if total_quotient!=0:
                normalized_quotient = total_quotient/len(journal_author_dict[journal.strip('\n')])
            outfile.write(journal.strip('\n') + ',' + str(normalized_quotient) + '\n')
            print(journal.strip('\n') + ',' + str(normalized_quotient) + '\n')
        except KeyError:
            pass
# with open('../../output/calc_ocq.csv','w') as outfile:
# 	for author in author_list:
# 		outfile.write(text_to_id(author) + ',' + str(author_total_cites[author]) + ',' + str(author_self_cites[author]) + '\n')
# 		if author_self_cites[author]!=0:
# 	 		print(text_to_id(author) + ' ' + str(author_total_cites[author]) + ' ' + str(author_self_cites[author]) +' '+ str(author_paper_count[authorau]))