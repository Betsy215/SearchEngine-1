#Author : Krishna Sai P B V
#Purpose: Vector space model- jmercertf retrieval model implementation
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

totalQueryNum=64
filetoprint=open('JMercerOutput.txt', "w")

querytf={}
docLen={}
dup={}
docs={}
docdup = defaultdict(list)
file1=open("file1",'r')
file1=file1.readlines()
file2=open("file2",'r')
file2=file2.readlines()
file3=open("file3",'r')
file3=file3.readlines()
avgDocLen=47
docID=defaultdict(list)
avgQueryLength=19

#parse through the index files to find the words
#and get its information
for line in file3:
	line=line.strip('\n')
	line=line.strip()
	line=string.split(line)
	dociD=int(line[0])
	doclen=int(line[1])
	docLen[dociD]=doclen

#Finding the word index
def findIndex(word,rawtf):
	#print "ctf","    ","df"
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
			ctf=int(lines[4])
			df=lines[3]
			break

	for lines in file2:	
		lines=lines.strip('\n')
		lines=lines.strip()
		lines=string.split(lines)
		if tID == lines[0]:
			docid=int(lines[1])
			toAppend=(word,str(lines[2]))
			rawtf[docid].append(toAppend)
	return ctf
			

jmercer_ext={}
jmercertf={}
#Caluclating the score for Jmercer smoothing
def caluclate_jmercer(url_narrative):
	ind=url_narrative.index(" ")
	queryNum=url_narrative[0:ind]
	url_narrative=url_narrative[ind+1:]
	allWordsInQuery=string.split(url_narrative)
	allwordsLen= len(allWordsInQuery)
	visited=[]
	jmercertf={}
	querytf={}
	doctf={}
	rawtf=defaultdict(list)
	k=0
	qtf={}
	value=0
	getid=0
	termfreq=0
	sumValue=0
	flag=0
	ct=0
	ctf={}
	lConstant=0.9
	num_Unique_Terms=11310
	num_Terms=111017
	for words in allWordsInQuery:
		qtf[words]=allWordsInQuery.count(words)

	for item in allWordsInQuery:
		ctf[item]=findIndex(item,rawtf)
	for k,v in rawtf.iteritems():
		for val in v:
			word=val[0]
			tf=int(val[1])
			score=math.log(((lConstant * float(tf/docLen[k])) + ((1-lConstant)* float(ctf[word]/num_Terms))),10)
			toremove_flag=len(v)-1
			sumValue=sumValue+score	
		sumValue=sumValue+math.log((allwordsLen-1) * (1-lConstant) * float(ctf[word] / num_Terms),10)
		toremove=toremove_flag * math.log((1-lConstant) * float(ctf[word]/num_Terms),10)
		sumValue=sumValue-toremove
		jmercertf[k]= sumValue
		qtf=0
		value=0
		qtfToAdd=0
		termfreq=0
		sumValue=0
		flag=0
		jmercer_ext[k]= "CACM-"+str(k)
	sorted_jmercertf = sorted(jmercertf.iteritems(), key=operator.itemgetter(1),reverse=True)
	i=1	
	print "writing output to file: %s" %(filetoprint)
	for key,value in sorted_jmercertf:
		if i<1001:	
			filetoprint.write(str(queryNum) + " " + "Q0" + " " +str(jmercer_ext[key]) + " " + str(i) + " " + str(value) + " " +"Exp")
			filetoprint.write("\n")		
			i=i+1
		
f = open(sys.argv[1],mode="r")
for q in f:
	print "Query being processed: %s" %(q)	
	caluclate_jmercer(q)
		
filetoprint.close()			
	

