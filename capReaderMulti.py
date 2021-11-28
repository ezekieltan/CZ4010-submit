import pyshark
import os
import pandas as pd
import sys
from tqdm import tqdm
from lib_FileSystemUtilities import FileSystemUtilities as fsu
import threading

folderName = sys.argv[1]
size = sys.argv[2]

def process(items, start, end):
    counter = 0
    for filename in items[start:end]:                                               
        try:
            os.system("python capReaderSingle.py " + folderName+' '+ filename+' '+str(size)+' '+ str(start+counter))
            counter = counter + 1                                           
        except Exception:                                                       
            print('error with item')                                            


def split_processing(items, num_splits=4):                                      
    split_size = len(items) // num_splits                                       
    threads = []                                                                
    for i in range(num_splits):                                                 
        # determine the indices of the list this thread will handle             
        start = i * split_size                                                  
        # special case on the last chunk to account for uneven splits           
        end = None if i+1 == num_splits else (i+1) * split_size                 
        # create the thread                                                     
        threads.append(                                                         
            threading.Thread(target=process, args=(items, start, end)))         
        threads[-1].start() # start the thread we just created                  

    # wait for all threads to finish                                            
    for t in threads:                                                           
        t.join()                                                                



filelist = fsu.getFilesInFolder(folderName)
split_processing(filelist)