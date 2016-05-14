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

journal_author_dict = {}
author_self_cites = {}
author_total_cites = {}
author_list = []
author_paper_count = {}
journal_list = []

#indexing based on the index of an article
article_list = list(db['publications'].find())
count = 0
call(["brew","services","stop","mongodb"])
for article in article_list:
    count += 1
    data[article['index']] = dict(article)
    try:
        if article['publication'] not in journal_list:
            journal_author_dict[article['publication']] = []
            journal_list.append(article['publication'])
        for author  in article['authors']:
            author = text_to_id(author)
            if author not in author_total_cites:
                author_total_cites[author] = 0
                author_self_cites[author] = 0
                author_paper_count[author] = 1
                author_list.append(author)
            else:
                author_paper_count[author] += 1
            if author not in journal_author_dict[article['publication']]:
                journal_author_dict[article['publication']].append(author)
    except KeyError:
        pass

with open('../../data/OCQ_temp_data/Journal_author.json','w') as outfile:
    json.dump(journal_author_dict,outfile)

with open('../../data/OCQ_temp_data/author_selfcites.json','w') as outfile:
    json.dump(author_self_cites,outfile)

with open('../../data/OCQ_temp_data/author_total_cites.json','w') as outfile:
    json.dump(author_total_cites,outfile)

journal_dict = {'list':journal_list}
with open('../../data/OCQ_temp_data/journal_list.json','w') as outfile:
    json.dump(journal_dict,outfile)

with open('../../data/OCQ_temp_data/data.json','w') as outfile:
    json.dump(data,outfile)

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

with open('../../output/calc_ocq.csv','w') as outfile:
    for journal in journal_list:
        total_quotient = 0.0
        normalized_quotient = 0.0
        for author in journal_author_dict[journal]:
            if author_total_cites[author]!=0:
                quotient = (author_total_cites[author] - author_self_cites[author])/(1.0 * author_total_cites[author])
                total_quotient += quotient
        if total_quotient!=0:
            normalized_quotient = total_quotient/len(journal_author_dict[journal])
        outfile.write(journal + ',' + normalized_quotient + '\n')
        print(journal + ',' + normalized_quotient + '\n')
# with open('../../output/calc_ocq.csv','w') as outfile:
# 	for author in author_list:
# 		outfile.write(text_to_id(author) + ',' + str(author_total_cites[author]) + ',' + str(author_self_cites[author]) + '\n')
# 		if author_self_cites[author]!=0:
# 	 		print(text_to_id(author) + ' ' + str(author_total_cites[author]) + ' ' + str(author_self_cites[author]) +' '+ str(author_paper_count[authorau]))