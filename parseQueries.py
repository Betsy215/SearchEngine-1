#Author : Krishna Sai P B V
#Purpose: Parse queries before giving to search engine
#Data:	  April 14th, 2012 

#Input to this file is the list of queries.
#Output is the file with the parsed queries
#after stopping and stemming

#usr/bin/python
import linecache, string, operator, re, sys
from collections import defaultdict
from types import ListType
from porterStemmer import PorterStemmer
import os,shutil

f=open(sys.argv[1])
filetoOpen=sys.argv[1]
s=open("./othersFromGlassgow/common_words")
stopwords_new=[]
stopwords=s.readlines()
for word in stopwords:
	stopwords_new.append(word.rstrip('\n'))
stopwords= stopwords_new
readLines=f.readlines()
filetowrite=sys.argv[2]
FILE=open("parsedQueries", "a")
docID=[]
docN=defaultdict(list)
docAuthors=defaultdict(list)
docInfo=defaultdict(list)
lineNumber=0
mainDict=defaultdict(list)
newDict=defaultdict(list)

#Process author seperately
def processAuthor(docID, line, lineNumber):
	n=1
	while(linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.W' and 
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.N' and
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.B' and
		 linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.I' and 
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.X' and
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.C' and
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.K'):
		docAuthors[docID].append(linecache.getline(filetoOpen,lineNumber+n).strip("\n"))
		n=n+1
		
#Parse through the given data
for i in readLines:
	lineNumber=lineNumber+1
	i=i.strip('\n')
	if(lineNumber>1):
			if(docInfo[docID[len(docID)-1]]<=0):
				docInfo[docID]=""
			if(docAuthors[docID[len(docID)-1]]<=0):
				docAuthors[docID]=""
	if(i[0:2]=='.I'):
		docid=int(i[3:])
		docID.insert(lineNumber-1,(int(i[3:])))
	if(i[0:2]=='.A'):
		processAuthor(docid, i, lineNumber)
	if(i[0:2]=='.N'):
		line=linecache.getline(filetoOpen,lineNumber+1).strip('\n')
		nValues=string.split(line)
		for i in nValues:
			docN[docid].append(i)
	if(i[0:2]=='.W'):
		line=linecache.getline(filetoOpen,lineNumber+1).replace('\n',' ')
		next=2
		while(line[0:2]!='.X' and line[0:2]!='.N' and line[0:2]!='.B' 
			and line[0:2]!='.I' and line[0:2]!='.C' and line[0:2]!='.K'):
			stringtoAdd+=line
			line=linecache.getline(filetoOpen,lineNumber+next)
			line=line.replace("\n"," ")
			next=next+1
		docInfo[docid].append(stringtoAdd)
	stringtoAdd=""	
	stringtoAddHere=""	
	linecache.clearcache()

#Append all the author info, document data, and other(s)
for i in docID:
	mainDict[i].append(docAuthors[i])
	mainDict[i].append(docInfo[i])
	mainDict[i].append(docN[i])

#lower the given word and polish it
def LowerPolish(fileT):
	fileT=fileT.lower()
	toRemove1 = [",","-","=","/","'",";","^","+","|",":","<",">","`","&","(",")"]
	toRemove2 = [".",'"',"[","]","?","!","*","%","{","}"]
	for i in toRemove1:
		if i in fileT:
			fileT=fileT.replace(i," ")		
	for i in toRemove2:
		if i in fileT:
			fileT=fileT.replace(i,'')		

	return fileT
count=0

#Stem each word and add to the dictionary
def printDocsHelper(fileT,k):
	if fileT not in stopwords:
	#stemmed words
		p = PorterStemmer()
       		fileT = p.stem(fileT, 0,len(fileT)-1) + " "
		fileT=re.sub(r'\s', '', fileT)
		print fileT
		if (len(fileT)>1) and (fileT not in stopwords):
			newDict[k].append(fileT)


filetowriteList=[]
#Process each query here
for k,v in mainDict.iteritems():
	print "Processing query: %s" %k
	for value in v:
		if isinstance(value, ListType):
			for val in value:
				fileTemp=string.split(val)					
				for filein in fileTemp:
					filetowriteList.append(filein)
		else: 
			filetowriteList=string.split(value)
		for fileT in filetowriteList:
			fileRaw=fileT
			fileT=LowerPolish(fileT)
			if (' ' in fileT) == True or ('-' in fileT)==True:
				filet=string.split(fileT)
				for fileT in filet:
					printDocsHelper(fileT,k)
			else:
				printDocsHelper(fileT,k)
		del filetowriteList[:]

for k,v in newDict.iteritems():
	FILE.write(str(k)+" ")
	for val in v:
		FILE.write(" "+str(val))
	FILE.write("\n")

