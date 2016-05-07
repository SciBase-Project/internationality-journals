with open('../../output/ACM_Aminer_journal_list.txt','r') as infile:
	names = infile.readlines()

names.sort()
with open('../../output/Sorted_list.txt','w') as outfile:
	for name in names:
		outfile.write(name)