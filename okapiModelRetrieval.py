#Author : Krishna Sai P B V
#Purpose: Vector space model- Okapitf retrieval model implementation
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
import operator

#Prints the top documents retrieved to this file!
filetoprint=open('okapiOutput.txt', "w")
#Declarations of dictionaries, lists used
querytf={}
docLen={}
dup={}
docs={}
okapitf_ext={}
okapitf={}
docID=defaultdict(list)
docdup = defaultdict(list)
file1=open("file1",'r')
file1=file1.readlines()
file2=open("file2",'r')
file2=file2.readlines()
file3=open("file3",'r')
file3=file3.readlines()
#Initializing values
avgDocLen=47 #Refer calDocLen.py attached with this
totalQueryNum=64
avgQueryLength=19
#Get all docids and their corresponding lengths
for line in file3:
	line=line.strip()
	line=string.split(line)
	dociD=int(line[0])
	doclen=int(line[1])
	docLen[dociD]=doclen

#Caluclate index values and append rawtf for each word
def findIndex(word,rawtf):
	ctf=0
	doclen=0
	df=0
	docid=0
	tf=0
	tID=0
	toSee=0
	#Get tID,ctf,df to get its corresponding docs
	for lines in file1:
		lines=lines.strip()
		lines=string.split(lines)
		if word == lines[1]:
			tID=lines[0]
			ctf=lines[4]
			df=lines[3]
			break
	#Get the docs which contains the given term and append to rawtf dict
	for lines in file2:	
		lines=lines.strip()
		lines=string.split(lines)
		if tID == lines[0]:
			docid=int(lines[1])
			toAppend=(word,str(lines[2]))
			rawtf[docid].append(toAppend)
			#rawtf[docid].append(int(lines[2]))
			
#Process the given query and caluclate the querytf and okapitf and write to file
def caluclate_vsokapi(url_narrative):
	ind=url_narrative.index(" ")
	queryNum=url_narrative[0:ind]
	url_narrative=url_narrative[ind+1:]
	allWordsInQuery=string.split(url_narrative)
	allwordsLen= len(allWordsInQuery)
	visited=[]
	okapitf={}
	querytf={}
	doctf={}
	qtf={}
	rawtf=defaultdict(list)
	k=0
	value=0
	getid=0
	termfreq=0
	sumValue=0
	flag=0
	ct=0
	#caluclate the frequency of term in the query and get index
	for words in allWordsInQuery:
		qtf[words]=allWordsInQuery.count(words)
	#Caluclate the querytf using the mentioned formula	
	for item,tf in qtf.iteritems():
		querytf[item]=float(tf/(tf+0.5+(1.5*allwordsLen/avgQueryLength)))
		findIndex(item,rawtf)
	#For each unique term,doc caluclate documenttf and dot product it with querytf as below	
	for k,v in rawtf.iteritems():
		for val in v:
			word=val[0]
			termfreq=int(val[1])
			qtfToAdd=querytf[word]
			flag=float(termfreq / (termfreq + 0.5 +(1.5 * docLen[k]/avgDocLen)))
			sumValue=sumValue+float(flag*qtfToAdd)
		okapitf[k]= sumValue
		qtf=0
		value=0
		qtfToAdd=0
		termfreq=0
		sumValue=0
		flag=0
		okapitf_ext[k]= "CACM-"+str(k)
	sorted_okapitf = sorted(okapitf.iteritems(), key=operator.itemgetter(1),reverse=True)
	i=1	
	print "writing output to file: %s" %(filetoprint)
	filetoprint.write()
	for key,value in sorted_okapitf:
		if i<1001:	
			filetoprint.write(str(queryNum) + " " + "Q0" + " " +str(okapitf_ext[key]) + " " + str(i) + " " + str(value) + " " +"Exp")
			filetoprint.write("\n")		
			i=i+1
		
#Opening file to read and process queries
f = open(sys.argv[1],mode="r")
#Processing each query
for q in f:
	print "Query being processed: %s" %(q)	
	caluclate_vsokapi(q)
#Close the file opened		
filetoprint.close()			
	

