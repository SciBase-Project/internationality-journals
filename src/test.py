import collections

print "\n\n[INFO] Processing articles for publication venues.\n"
print "------------------------------------------------------------------------------------------------\n\n"
file = open("../data/aminer_publication_tiny.txt")
lines = file.readlines()
papers = {}
i = 0
article_count = 0
pub_count = 0
author_list_temp = []
author_article_count = collections.OrderedDict()
author = set()

while i < len(lines) :
    if lines[i].startswith('#@') :