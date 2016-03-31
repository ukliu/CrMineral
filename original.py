#! /usr/bin/env python
#coding=utf-8
# Sample input data (piped into STDIN):


import csv,os,sys
import re

lines=open('/Users/cliu/deepdive/examples/cobalt/CoMineralList.txt').readlines()
minerallist=[]
agelist=['ma','age','dating','ka','ga','kyr','myr','year','geochronology','m.a.','k.a.','date']
for line in lines:
  minerallist.append(line.strip('\n').lower())
minlib={}
textlines=open('/Users/cliu/deepdive/examples/cobalt/co_nlp352.txt').readlines()
articleID=[]
artD={}
lengD={}
thankD={}
#record textlines containing Cr mineral names, location or age information lower().
for line in textlines:
  sline=line.lower().split('\t')
  tL=re.sub('[{}"]','',sline[6])
  tLL=re.sub(r',,,',',;,',tL)
  tList=tLL.split(',') #get rid of {}",,, in the raw texts
  if len(list(set(agelist).intersection(set(tList)))) >0:
    if sline[0] not in articleID:
      articleID.append(sline[0]) # list of articles having age formation
  if ('reference' in tList or 'referenc' in tList or 'references' in tList) and sline[0] in articleID:
    lengD.update({sline[0]:int(sline[1])}) #dictionary of age-containing article length before reference
    #note lengD has fewer items than articleID since articleID counts paper that has age information in reference part
  if('acknowledgement' in tList or 'acknowledgements' in tList or 'acknowledge' in tList or 'thank' in tList or 'thanks' in tList) and sline[0] in articleID:
    thankD.update({sline[0]:int(sline[1])})
  if sline[1]=='1':
    artD.update({sline[0]:tLL}) #record the title of all articles

  locList=re.sub('[{}"]','',sline[5]).split(',')
  sharemin=list(set(minerallist).intersection(set(tList)))
  shareage=[]
  shareloc=[]
  if 'location' in locList:
    for pos in [i for i,j in enumerate(locList) if j=='location']:
      shareloc.append(tList[pos])
  if 'number' in locList:
    for pos in [i for i,j in enumerate(locList) if j=='number']:
      if pos<len(tList)-1 and tList[pos+1] in ['ma', 'ga', 'ka', 'm.a.', 'g.a.', 'k.a.','kyrs', 'myrs']:
        if pos>0 and tList[pos-1]=='±':
          shareage.append(tList[pos-2]+tList[pos-1]+tList[pos]+tList[pos+1])
        else:
          shareage.append(tList[pos]+tList[pos+1])

  if len(sharemin)>0 or len(shareage) >0 or len(shareloc)>0:
    minlib.update({(sline[0],int(sline[1])):(sharemin,shareage,shareloc,' '.join(tList))})
    #record the sentence containing mineral or age or loc information in the paper (including reference part but not the title)

newlib={}
for key in minlib.keys():
  if key[0] in thankD.keys():
    if key[1]<thankD[key[0]]:
      newlib.update({(key[0],key[1]):minlib[key]})
  elif key[0] in lengD.keys() and key[1]<lengD[key[0]]:
    newlib.update({(key[0],key[1]):minlib[key]})
    #record the sentence containing mineral or age or loc information in the paper (excluding reference part but not the title)

w=csv.writer(open("/Users/cliu/PycharmProjects/Cr_test/output1.csv","w"))
newkey=newlib.keys()
newkey.sort()
global paperID
paperID=[]
for key in newkey:
  w.writerow([key[0],key[1],','.join(newlib[key][0]),','.join(newlib[key][1]),','.join(newlib[key][2]),newlib[key][3]])
  if key[0] not in paperID:
    paperID.append(key[0])

v=csv.writer(open("/Users/cliu/PycharmProjects/Cr_test/ID1.csv","w"))
v.writerow(paperID)
