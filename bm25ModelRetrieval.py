#Author : Krishna Sai P B V
#Purpose: BM25 retrieval model implementation
#	  for the developed search engine
#Data:	  April 12th, 2012 

#Input to this file is the list of parsed queries.
#Output is the file with the relevant documents retrieved
#Using this model

#!/usr/bin python
from __future__ import division
from collections import defaultdict
#from collections import OrderedDict
import sys, string, re, os, subprocess, urllib, operator
from sys import stdout
import operator,math

#Dictionaries, arrays, variables needed
totalQueryNum=64
filetoprint=open('filetoPrint3.txt', "w")
bmtf={}
sorted_bmtf={}
bmtf_ext={}
querytf={}
docLen={}
dup={}
docs={}
K1=1.2
K2=100
b=0.75
docdup = defaultdict(list)
file1=open("file1",'r')
file1=file1.readlines()
file2=open("file2",'r')
file2=file2.readlines()
file3=open("file3",'r')
file3=file3.readlines()
avgDocLen=47
avgQueryLength=19
docID=defaultdict(list)

#navigate through the index files
for line in file3:
	line=line.strip('\n')
	line=line.strip()
	line=string.split(line)
	dociD=int(line[0])
	doclen=int(line[1])
	docLen[dociD]=doclen

#find the index of the given word
def findIndex(word,rawtf):
	ctf=0
	doclen=0
	df=0
	docid=0
	tf=0
	tID=0
	toSee=0
	for lines in file1:
		lines=lines.strip('\n')
		lines=lines.strip()
		lines=string.split(lines)
		if word in lines:
			tID=lines[0]
			ctf=lines[4]
			df=int(lines[3])
			break

	for lines in file2:	
		lines=lines.strip('\n')
		lines=lines.strip()
		lines=string.split(lines)
		if tID == lines[0]:
			docid=int(lines[1])
			toAppend=(word,str(lines[2]))
			rawtf[docid].append(toAppend)
	return df

bm25_ext={}
bm25={}
def caluclate_bm25(query):
	ind=query.index(" ")
	queryNum=query[0:ind]
	query=query[ind+1:]
	allWordsInQuery=string.split(query)
	allwordsLen= len(allWordsInQuery)
	visited=[]
	doctf={}
	rawtf=defaultdict(list)
	k=0
	qtf={}
	value=0
	getid=0
	termfreq=0
	sumValue=0
	flag=0
	N=3204
	df={}
	for words in allWordsInQuery:
		qtf[words]=allWordsInQuery.count(words)
	for words,count in qtf.iteritems():		
		df[words]=findIndex(words,rawtf)
	for k,v in rawtf.iteritems():
		ri=0
		R=0
		K=K1*((1-b) + b * docLen[k] / avgDocLen)
		for val in v:
			word=val[0]
			ni=df[word]
			termfreq=int(val[1])	
			qtfToAdd=qtf[word]
			flag1=float((ri+0.5) / (R-ri + 0.5))
			flag2=float((ni-ri+0.5) / (N-ni-R+ri+0.5))
			flag3=float(((K1+1) * termfreq) / (K+termfreq))
			flag4=float(((K2+1) * qtfToAdd) / (K2+qtfToAdd))
			flag_temp=math.log(float(flag1/flag2))
			flag=flag_temp * flag3 * flag4
			sumValue=sumValue+flag
		bmtf[k]= sumValue
		sumValue=0
		bmtf_ext[k]= "CACM-"+str(k)
	sorted_bmtf = sorted(bmtf.iteritems(), key=operator.itemgetter(1),reverse=True)
	i=1	
	print "writing output to file: %s" %(filetoprint)
	for key,value in sorted_bmtf:
		if i<1001:	
			filetoprint.write(str(queryNum) + " " + "Q0" + " " +str(bmtf_ext[key]) + " " + str(i) + " " + str(value) + " " +"Exp")
			filetoprint.write("\n")		
			i=i+1
	
#File to read queries from
f = open(sys.argv[1],mode="r")
for q in f:
	print "Query being processed: %s" %(q)	
	caluclate_bm25(q)
		
filetoprint.close()			
	

