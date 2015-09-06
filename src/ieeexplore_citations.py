# append paper number to links below to get details
# for eg : http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6196220
details_link = 'http://ieeexplore.ieee.org/xpl/abstractSimilar.jsp?arnumber='
authors_link = 'http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber='
references_link = 'http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber='
citations_link = 'http://ieeexplore.ieee.org/xpl/abstractCitations.jsp?arnumber='

import urllib2
from bs4 import BeautifulSoup


def get_id(link):
    import re

    try :
        searchObj = re.search(r'(.*)arnumber=(\d*).*', link)
        if searchObj:
            return searchObj.group(2)
        else:
            return ""
    except :
        return ""


def get_authors(id):
    link = authors_link + str(id)
    # print "[INFO]  Fetching authors from link " + str(link)

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

    authors = [normalise_name(x) for x in authors]

    # print "[DEBUG] ", authors
    return authors


def get_references(id):
    link = references_link + str(id)
    print "\n[INFO]  Fetching references from link " + str(link)

    main_authors = set(get_authors(id))

    edges = []
    try:
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        ol = soup.find('ol', attrs={'class': 'docs'})
        lis = ol.findAll('li')

        for li in lis:
            citation = li.find('a')
            citation_id = get_id(str(citation))
            cited_authors = set(get_authors(citation_id))

            common_authors = main_authors.intersection(cited_authors)

            if len(common_authors) > 0:
                print "[CHECK]  Common authors ", common_authors
                edges.append([id, citation_id, '1'])
            else:
                if citation_id is not "":
                    edges.append([id, citation_id, '0'])

    except:
        pass

    return edges


def normalise_name(name):
    # replace all '.' with space
    name = name.replace(".", " ")

    sub_names = name.split(',')

    # start from second sub name
    i = 1
    while i < len(sub_names):
        s = sub_names[i].strip()

        # fetch all initials
        res = " ".join(item[0].upper() for item in s.split())

        sub_names[i] = res

        i += 1

    # reverse list
    sub_names = list(reversed(sub_names))
    return " ".join(x for x in sub_names)


all_edges = []


def compute_in_parallel(args):
    for arg in args:
        print "\n[INFO]  Processing " + str(arg)
        all_edges.extend(get_references(get_id(arg)))


def citation_network():
    from openpyxl import load_workbook

    wb = load_workbook(filename='../data/Data3.xlsx', read_only=True)
    ws = wb['Sheet1']


    links = []
    for row in ws.iter_rows('G39:G1005'):
        for cell in row:
            links.append(cell.value)


    import threading
    num_per_thread = 100
    divide = lambda lst, sz: [lst[i : i + sz] for i in range(0, len(lst), sz)]
    divided_links = divide(links, num_per_thread)

    print "[INFO]  Number of threads ", (len(links) / num_per_thread) + 1

    threads = []
    for i in range(len(divided_links)):
        t = threading.Thread(target=compute_in_parallel, args=(divided_links[i],))
        threads.append(t)
        t.start()

    for t in threads :
        t.join()


    print "[INFO]  Number of egdes " + str(len(all_edges))
    print "[INFO]  Writing edges file"

    file = open("../output/ieee_citation_network.txt", "w")
    for edge in all_edges:
        file.write(" ".join(edge))
        file.write('\n')
    file.close()

    print "[INFO]  Done Writing edges to file"


citation_network()
