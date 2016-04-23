# Removes leading spaces from ACM_author_list_Aminer.txt

with open("../../data/ACM_author_list_Aminer.txt",'r') as file :
    with open("../../data/ACM_author_list_Aminer_v2.txt",'w') as file_new :
        lines = file.readlines()
        for line in lines :
            file_new.write(line.lstrip(' '))
