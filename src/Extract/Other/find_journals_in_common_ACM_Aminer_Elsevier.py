
import re
import unicodedata
import ast

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

count = 0
found_journals = []

with open('../../../output/ACM_Aminer_journal_list.txt') as file :
    with open('../../../data/Elsevier_journal_list.csv') as jlist :
        lines = file.read()
        journals = jlist.readlines()
        for journal in journals :
            #print "[INFO]", journal
            try :
                if lines.find(text_to_id(journal)) != -1 :
                    count += 1
                    print "[DEBUG]",journal, "#",count
                    found_journals.append(journal)

            except TypeError :
                continue

print '[INFO] Found ',count
with open('../../../output/ACM_Aminer_journal_list.txt') as file :
    lines = file.readlines()
    print len(lines)

print '[INFO] Total number of journals ',

with open("../../../output/ACM_Elsevier_both_journal_list.txt",'w') as file :
    for journal in found_journals :
        file.write(journal)

