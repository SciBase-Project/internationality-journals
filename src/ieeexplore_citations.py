# append paper number to links below to get details
# for eg : http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6196220
details_link = 'http://ieeexplore.ieee.org/xpl/abstractSimilar.jsp?arnumber='
authors_link = 'http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber='
references_link = 'http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber='
citations_link = 'http://ieeexplore.ieee.org/xpl/abstractCitations.jsp?arnumber='


import urllib2
from bs4 import BeautifulSoup

def get_id(link) :

    import re
    searchObj = re.search( r'(.*)arnumber=(\d*).*', link)
    if searchObj:
        return searchObj.group(2)
    else :
        return ""

def get_authors(id) :
    link = authors_link + str(id)
    print "[INFO]  Fetching authors from link ", link

    authors = []
    try :
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        # print soup.prettify()
        metas = soup.find_all("meta", attrs={"name" : "citation_author"})

        for meta in metas :
            if meta['name'] == 'citation_author' :
                authors.append( meta['content'] )
    except :
        pass

    authors = [normalise_name(x) for x in authors]

    print "[DEBUG] ", authors
    return authors

def get_references(id) :
    link = references_link + str(id)
    print "[INFO]  Fetching references from link ", link

    try :
        page = urllib2.urlopen(link).read()
        soup = BeautifulSoup(page, 'html.parser')

        ol = soup.find('ol', attrs={'class' : 'docs'})
        lis = ol.findAll('li')

        for li in lis :
            citation = li.find('a')
            citation_id = get_id(str(citation))
            cited_authors = set(get_authors(citation_id))

            common_authors = main_authors.intersection(cited_authors)

            if len(common_authors) > 0 :
                print "[CHECK]  Common authors ", common_authors

    except :
        pass


def normalise_name(name) :
    # replace all '.' with space
    name = name.replace(".", " ")

    sub_names = name.split(',')

    # start from second sub name
    i = 1
    while i < len(sub_names) :
        s = sub_names[i].strip()

        # fetch all initials
        res = " ".join(item[0].upper() for item in s.split())

        sub_names[i] = res

        i += 1

    # reverse list
    sub_names = list(reversed(sub_names))
    return " ".join(x for x in sub_names)

id = get_id('http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=6196220')

main_authors = set(get_authors(id))
get_references(id)
