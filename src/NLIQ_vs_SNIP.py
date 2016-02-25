import csv
import matplotlib.pyplot as plt

jinfo = {"Jname":[],"ourSNIP":[],"SNIP":[],"SE":[],"NSE":[],"NLIQ":[]}
i = 0

with open ("../output/SNIP/SNIP_ourSNIP_NLIQ.csv") as file :
    journal = csv.reader(file, delimiter=',', quotechar='|')
    for item in journal:
        i += 1
        if (i > 1) :
            jinfo["Jname"].append(item[0])
            jinfo["ourSNIP"].append(item[1])
            jinfo["SNIP"].append(item[2])
            jinfo["SE"].append(item[3])
            jinfo["NSE"].append(item[4])
            jinfo["NLIQ"].append(item[5])

x = jinfo["SNIP"]
y = jinfo["NLIQ"]

plt.scatter(x,y,alpha=0.5)
plt.show()

