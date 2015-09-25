authors_link = 'http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber='

all_papers = []

import urllib2
from bs4 import BeautifulSoup

def get_authors(id):

    link = authors_link + str(id)
    print "[INFO]  Fetching authors from link " + str(link)

    authors = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        # print soup.prettify()
        metas = soup.find_all("meta", attrs={"name": "citation_author"})

        for meta in metas:
            if meta['name'] == 'citation_author':
                authors.append(meta['content'])
    except:
        pass

    # print "[DEBUG] ", authors
    return authors


def store_papers() :
    print "[INFO]  Writing " + str(len(all_papers)) + " papers to file"

    import json
    file = open("../output/ieee_citation_network.json", "w")
    file.write(json.dumps(all_papers, indent=4))
    file.close()

    print "[INFO]  Done Writing papers to file"


with open("../output/ieee_citation_network_edges.txt") as f:
    lines = f.readlines()

i = 0
limit = len(lines)

while i < limit :
    src, dest, type = lines[i].split(' ')

    paper = {}
    paper['id'] = src
    paper['authors'] = get_authors(src)
    paper['citations'] = [{'id' : dest, 'authors' : get_authors(dest)}]

    i = i + 1

    while i < limit :
        src, dest, type = lines[i].split(' ')

        if src != paper['id'] :
            break
        paper['citations'].append( {'id' : dest, 'authors' : get_authors(dest)} )

        i = i + 1

    all_papers.append(paper)

    if len(all_papers) % 25 == 0 :
        store_papers()

store_papers()


