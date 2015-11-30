
def get_median_split_journals() :

    print "[INFO] Processing journals to be considered"

    journals_snip = []
    file = open("../data/journal_snip.txt")
    for line in file.readlines() :
        entry = line.strip().split(" : ")
        journal = entry[0]
        snip = entry[1]
        journals_snip.append([journal, int(snip)])
    file.close()

    print "[DEBUG] Journals : ", journals_snip
    print "[INFO] Done processing journals to be considered"



    print "[INFO] segregating journals based on median snip"

    # sort the list
    journals_snip.sort(key=lambda x:x[1])

    #print journals_snip

    median_snip = 0

    N = len(journals_snip)
    half = len(journals_snip) // 2

    if not N % 2:
        median_snip = (journals_snip[half - 1][1] + journals_snip[half][1]) / 2.0
    else : median_snip = journals_snip[half][1]

    print "[DEBUG] Median snip value: ", median_snip

    journals_low = []
    journals_high = []

    for journal, snip in journals_snip :

        if snip >= median_snip : journals_high.append(journal)
        else : journals_low.append(journal)

    print "[DEBUG] Journals with snip below median : ", len(journals_low), journals_low
    print "[DEBUG] Journals with snip above median : ", len(journals_high), journals_high

    print "[INFO] Done segregation"


    return journals_low, journals_high

# get_median_split_journals()