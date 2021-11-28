import pyshark
import os
import pandas as pd
from tqdm import tqdm
import sys
from lib_FileSystemUtilities import FileSystemUtilities as fsu

def getIVInt(pkt):
    try:
        ivString = str(pkt[0].wep_iv)[4:]
        ivStringArray = [ivString[i:i+2] for i in range(0, len(ivString), 2)]
        ivIntArray = [int(i, 16) for i in ivStringArray]
        return ivIntArray
    except AttributeError as e:
        return None


folderName = sys.argv[1]
size = int(sys.argv[2])
filelist = fsu.getFilesInFolder(folderName)

totalPacketInfo = {}
fileCounter = 0
for filename in filelist:
    cap = pyshark.FileCapture(os.path.join(folderName, filename))
    for i in tqdm(range(size)):
        result = {}
        try:
            pkt = cap[i]
        except KeyError as e:
            continue
        try:
            iv = getIVInt(pkt)
            if iv is not None:
                result['iv0'] = iv[0]
                result['iv1'] = iv[1]
                result['iv2'] = iv[2]
            result['bssid'] = pkt.wlan.bssid
            result['ra'] = pkt.wlan.ra
            result['da'] = pkt.wlan.da
            result['ta'] = pkt.wlan.da
            result['sa'] = pkt.wlan.sa
            result['staa'] = pkt.wlan.staa
            result['data'] = pkt.data.data
        except AttributeError as e:
            continue
        totalPacketInfo[size*fileCounter+i] = result
    fileCounter = fileCounter + 1
    print()
    print()
    print()
    print()
    print()
    print(fileCounter, ' of ', len(filelist))
    print()
    print()
    print()
    print()
    print()

df = pd.DataFrame.from_dict(totalPacketInfo, orient='index')
df.to_csv(folderName+'.csv')