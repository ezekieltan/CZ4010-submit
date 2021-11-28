import pandas as pd
from tqdm import tqdm
import copy
import itertools

def xorHexString(a,b):
    result = int(a, 16) ^ int(b, 16) # convert to integers and xor them together
    return '{:x}'.format(result)     # convert back to hexadecimal

def xorHexStringPandas(x):
    return xorHexString(x[0],x[1])

def hexString2IntArray(hexString):
    c = hexString
    if(len(hexString) % 2 == 1):
        hexString = '0'+hexString
    intArray = [int(c[i:i+2],16) for i in range(0,len(c),2)]
    return intArray

def hex2bin(s):
    hexadecimal = s
    end_length = len(hexadecimal) * 4
    hex_as_int = int(hexadecimal, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    return padded_binary

def intArray2HexString(a):
    return ''.join('{:02x}'.format(x) for x in a)

def hex2int(s):
    hexadecimal = s
    hex_as_int = int(hexadecimal, 16)
    return hex_as_int

# Perform the KSA algorithm
def KSA(S, key_list, to=-1):
    j = 0
    N = len(S)
    if(to<0):
        to=N
    Ss = {}
    Js = {}
    # Iterate over the range [0, N]
    for i in range(0, to):
        if(i==3):
            Ss[i] = copy.deepcopy(S)
            Js[i] = j
            
        # Find the key
        j = (j + S[i]+key_list[i]) % N
        
        # Update S[i] and S[j]
        S[i], S[j] = S[j], S[i]
        
        if(i==to):
            return S, Ss, Js
    return S, Ss, Js

# Perform PGRA algorithm
def PGRA(S):
    
    N = len(S)
    i = j = 0
    key_stream = []
    
    # Iterate over [0, length of pt]
    for k in range(0, 256):
        i = (i + 1) % N
        j = (j + S[i]) % N
        
        # Update S[i] and S[j]
        S[i], S[j] = S[j], S[i]
        k = (S[i]+S[j]) % N
        key_stream.append(S[k])
    return key_stream

def rc4KeyPrep(key, S):
    key_list = key
    # Making key_stream equal
    # to length of state vector
    diff = int(len(S)-len(key_list))
    if diff != 0:
        for i in range(0, diff):
            key_list.append(key_list[i])
    return key_list

def rc4(key):
    #print("Key : ", key)
    # The initial state vector array
    S = [i for i in range(0, 256)]
    key_list = rc4KeyPrep(key, S)
    S, Ss, Js = KSA(S, key_list)
    key_stream = PGRA(S)
    return key_stream





def main():
    hexChars = ['0','1','2','3','4','5','6','7','8']
    outputs = {}
    for ca in tqdm(hexChars):
        for cb in hexChars:
            for cc in hexChars:
                for cd in hexChars:
                    for ce in hexChars:
                        for cf in hexChars:
                            hexString = ca+cb+cc+cd+ce+cf+'ABCDEF0123'
                            rc4Output = rc4(hexString2IntArray(hexString))
                            outputs[''+ca+cb+cc+cd+ce+cf] = rc4Output[:256]
    outputDf = pd.DataFrame.from_dict(outputs, orient='index')
    keyPositions = [0,1,2,3,4]
    results = {k:[] for k in keyPositions}
    
    for i in keyPositions:
        for index, ks in tqdm(outputDf.iterrows()):
            S = [i for i in range(0, 256)]
            ivString = str(index)
            iv = [int(ivString[0:2],16), int(ivString[2:4],16), int(ivString[4:6],16)]
            throwaway, Ss, Js = KSA(S, rc4KeyPrep(iv, S), 4)
            idx = (3+i-ks[2+i])%256
            a = Ss[3].index(idx)
            b = 0
            for xx in range(3, 3+i+1):
                b = b + Ss[3][xx]
            summ = (a-(Js[3]+b))%256
            results[i].append(summ)
    resultsRanking = []
    for k in results.keys():
        resultsRanking.append(pd.DataFrame(results[k], columns = ['x'])['x'].value_counts().reset_index()['index'].tolist()[:5])
    print(resultsRanking)
    

if __name__ == "__main__":
    main()
