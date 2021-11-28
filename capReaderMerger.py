import pandas as pd


import pyshark
import os
import pandas as pd
import sys
from tqdm import tqdm
from lib_FileSystemUtilities import FileSystemUtilities as fsu
from lib_TableReader import TableReader
import threading

folderName = sys.argv[1]

tr = TableReader(folderName)
names = tr.getDfNames()
dfs = []
for name in names:
    dfs.append(tr.getDf(name))
finalDf = pd.concat(dfs)
finalDf = finalDf.sort_values(by=['Unnamed: 0'])
finalDf.to_csv(folderName+'.csv', index=False)