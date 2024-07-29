alltale_Locate = []
alltale_TimeStart = []
alltale_TimeEnd = []
alltale_NoteNumber = []
bpm = 120 #default
chartinfo = {'bpm':'120','artist':'null','creator':'null','title':'null','column':'4','offset':'0'} #default dict.
mcz_Path = ''
import tkinter as tk
from tkinter import filedialog
import zipfile
import hashlib

print('''
███  ███   █████   ███████  ███████   █████   ██    ████████
███  ███  ██   ██      ██        ██  ██   ██  ██       ██
██ ██ ██  ██       ███████  ███████  ███████  ██       ██
██ ██ ██  ██   ██   ██      ██       ██   ██  ██       ██
██    ██   █████   ███████  ███████  ██   ██  ███████  ██
Official MalodyChart to ALLTALE tool. [Version 1.0.0]
© Merithemm Studio 2024.
      
#####################################################
PLEASE SELECT YOUR .MCZ FILE.
      ''')

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def rm_substring(MainString, Sub): #Only for removing InfoData from .mc File.
    if MainString.startswith(Sub):
        return MainString[len(Sub):]
    elif MainString.endswith(Sub):
        return MainString[:-len(Sub)]
    return MainString

mcz_Path = select_file()
if mcz_Path == '':
    print('[ EXIT ]NO FILE CHOOSED.')
    exit()

#Read .mc/.ogg file
with zipfile.ZipFile(mcz_Path, 'r') as zip_ref:
    mcz_list = zip_ref.namelist()
    mc_file_name = next((f for f in mcz_list if f.endswith('.mc')), None)
    ogg_file_name = next((f for f in mcz_list if f.endswith('.ogg')), None)
    
    if mc_file_name and ogg_file_name:
        with zip_ref.open(mc_file_name) as mc_file:
            mc_content = mc_file.read().decode('utf-8')
        with zip_ref.open(ogg_file_name) as ogg_file:
            hash_md5 = hashlib.md5()
            for chunk in iter(lambda: ogg_file.read(4096), b""):
                hash_md5.update(chunk)
            md5 = hash_md5.hexdigest()+'.ogg'
            print('MUSIC MD5 VALUE: [' + md5 + ']')

    else:
        print('[ EXIT ]MCZ FILE ERROR.')
        exit()

#Read Chart Info and Remove
## Head Remove
mcInfo_Head = ''
getInfoTmp = 0
while (mc_content[getInfoTmp:getInfoTmp+4] == 'note') != True:
    mcInfo_Head += mc_content[getInfoTmp]
    getInfoTmp += 1
for i in range(7):
    mcInfo_Head += mc_content[getInfoTmp+i]
mc_content=rm_substring(mc_content,mcInfo_Head) #Remove .mc's HeadInfo
## Foot Remove
mcInfo_Foot = ''
getInfoTmp = len(mc_content)-1
while (mc_content[getInfoTmp:getInfoTmp + 16] == ',{"beat":[0,0,1]') != True:
    mcInfo_Foot += mc_content[getInfoTmp]
    getInfoTmp -= 1
mcInfo_Foot += mc_content[getInfoTmp]
mcInfo_Foot = mcInfo_Foot[::-1]
mc_content=rm_substring(mc_content,mcInfo_Foot) #Remove .mc's FootInfo

def searchInfo(string_, dict_):
    results = {}
    for key, value in dict_.items():
        if str(value) in string_:
            results[key] = value
    return results

FullmcInfo = mcInfo_Head + mcInfo_Foot
getInfoTmp = ''
InfoKeys = list(chartinfo.keys())
for i in range (len(FullmcInfo)):
    for j in range(len(InfoKeys)):
        if FullmcInfo[i : i + len(InfoKeys[j-1])] == InfoKeys[j-1]:
            getInfoTmp = i + 3 + len(InfoKeys[j-1])
            if InfoKeys[j-1] == 'column' or InfoKeys[j-1] == 'offset':
                getInfoTmp -= 1
                while (FullmcInfo[getInfoTmp] == ',') != True:
                    getInfoTmp += 1
                chartinfo[InfoKeys[j-1]] = FullmcInfo[i + 2 + len(InfoKeys[j-1]):getInfoTmp]
            elif InfoKeys[j-1] == 'bpm':
                getInfoTmp -= 1
                while (FullmcInfo[getInfoTmp] == '}') != True:
                    getInfoTmp += 1
                chartinfo[InfoKeys[j-1]] = FullmcInfo[i + 2 + len(InfoKeys[j-1]):getInfoTmp]
            else:
                while (FullmcInfo[getInfoTmp] == '"') != True:
                    getInfoTmp += 1
                
                chartinfo[InfoKeys[j-1]] = FullmcInfo[i + 3 + len(InfoKeys[j-1]):getInfoTmp]
            
chartinfo['column'] = int(chartinfo['column'])
chartinfo['bpm'] = float(chartinfo['bpm'])
chartinfo['offset'] = float(chartinfo['offset'])
bpm = chartinfo['bpm']

if (chartinfo['column'] == 4) != True:
    print('[ EXIT ]ALLTALE NOW CAN ONLY READ 4K CHARTS.')
    exit()

print('THE INFORMATION OF THE CHART IS AS FOLLOWS.')
print('[ TIPS ]Only the BPM and Offset values should be adjusted before conversion. If other information is incorrect, you can change it after the conversion.')
print('============================================')
print('Your Song:[ ' + chartinfo['title'] + ' - ' + chartinfo['artist'] + ' ]. Chart created by [ ' + chartinfo['creator'] + ' ].' )
print('BPM:' + str(chartinfo['bpm']) + ', Offset = ' + str(chartinfo['offset']) + ' ms.')
print('============================================')

if input('[ CONFIRM ]Please confirm. (Y/N)') == 'Y':
    print('CHART CONFIRMED')
else:
    print('[ EXIT ]CONVERSION NOT CONFIRMED, PROCESS ABORTED.')
    exit()
    

#Main Processor
tmp_m = ''
tmp_i = 1
tmp_n = ''
transferCache = []
sliceCache = []
while (tmp_i >= len(mc_content)) != True: 
    while (tmp_i-1 >= len(mc_content) or mc_content[tmp_i-1] == '{') != True:
        tmp_i += 1

    tmp_i += 1
    while (tmp_i-1 >= len(mc_content) or mc_content[tmp_i-1] == '}') != True:
        tmp_m = tmp_m + str(mc_content[tmp_i-1])
        tmp_i += 1
    
    transferCache.append(tmp_m)
    tmp_m = ''
    tmp_i += 1

del transferCache[-1] #deleteLastElement
tmp_i = 1
tmp_m = ''
for i in range(len(transferCache)):
    tmp_i = 1
    while tmp_i < len(transferCache[i]):
        while (tmp_i > len(transferCache[i]) or transferCache[i][tmp_i-1] == ',') != True: 
            tmp_m = tmp_m + str(transferCache[i][tmp_i-1])
            tmp_i += 1
        
        sliceCache.append(tmp_m)
        tmp_m = ''
        tmp_i += 1
    
    alltale_NoteNumber.append(len(alltale_NoteNumber) + 1)
    tmp_n = float(sliceCache[0][8:len(sliceCache[0])]) 
    tmp_n += float(sliceCache[1])/float((sliceCache[2][0:len(sliceCache[2])-1]))
    if len(sliceCache) == 4:
        alltale_Locate.append(int(sliceCache[4-1][-1])+1)
        alltale_TimeStart.append((tmp_n)*(60/bpm))
        alltale_TimeEnd.append((tmp_n)*(60/bpm))
    else:
        alltale_Locate.append(int(sliceCache[7-1][-1])+1)
        alltale_TimeStart.append((tmp_n)*(60/bpm))
        tmp_n = float(sliceCache[4-1][12-1:len(sliceCache[4-1])])
        tmp_n += float(sliceCache[5-1])/float((sliceCache[6-1][0:len(sliceCache[6-1])-1]))
        alltale_TimeEnd.append((tmp_n)*(60/bpm))
    
    sliceCache = []

with open('Locate.txt', 'w', encoding='utf-8') as file:
    for item in alltale_Locate:
        file.write(str(item) + '\n') 

with open('TimeStart.txt', 'w', encoding='utf-8') as file:
    for item in alltale_TimeStart:
        file.write(str(item) + '\n') 

with open('TimeEnd.txt', 'w', encoding='utf-8') as file:
    for item in alltale_TimeEnd:
        file.write(str(item) + '\n')

with open('NoteNumber.txt', 'w', encoding='utf-8') as file:
    for item in alltale_NoteNumber:
        file.write(str(item) + '\n')  

print('CONVERTED. PRESS ENTER TO QUIT THE PROGRAM.')
input('')