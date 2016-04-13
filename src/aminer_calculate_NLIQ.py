__author__ = 'Sukrit'
import bson
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit


import pymongo
client = pymongo.MongoClient("localhost", 27017)
# db name - aminer
db = client.aminer
# collection
db.publications







