# Removes all possible journal-name subset.s
# eg. Age is a subset of Agent, etc.


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


with open("../../../output/ACM_Elsevier__journal_list_curated.txt",'r') as file :
    lines = file.readlines()
    lines = filter(lambda item : item != '\n', lines)
    lines_2 = file.readlines()
    lines_2 = filter(lambda item : item != '\n', lines_2)

    list = []
    for item in lines :
        list.append(item.rstrip('\r\n'))

    unique_list = []

    for item in list :
        for item2 in list :
            if len(item2) != len(item) and item2.find(item) != -1 :
                print item, ">", item2
                unique_list.append(item2)

with open("../../../output/ACM_Elsevier_journal_list_curated_v2",'w') as file :
    for item in unique_list :
        file.write(item+'\n')

