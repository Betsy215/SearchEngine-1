#Author: Krishna Sai
#Student at Northeastern University,
#Boston, MA, US
#

#Parse CACM collection and write words as files to a temporary directory
#so that the size of the corpus have no affect on the memory

#To run this file, please create a wordFiles named directory where this program is 
#on disk. In this directory, the temporary word files gets created
#This file takes input as the document(s) to search at
#This file outputs four different files and a number of word files as mentioned
#below

#usr/bin/python
import linecache, string, operator, re, sys
from collections import defaultdict
from types import ListType
from porterStemmer import PorterStemmer
import os,shutil


f=open(sys.argv[1])
filetoOpen=sys.argv[1]
#open the common words provided in glassgow
s=open("./othersFromGlassgow/common_words")
stopwords_new=[]
stopwords=s.readlines()
#stop words that are not important
for word in stopwords:
	stopwords_new.append(word.rstrip('\n'))
stopwords= stopwords_new
readLines=f.readlines()
#variables, arrays and dictionaries needed
docID=[]
docBibilo={}
docC={}
docTitle=defaultdict(list)
docK=defaultdict(list)
docN=defaultdict(list)
docAuthors=defaultdict(list)
docInfo=defaultdict(list)
line=0
lineNumber=0
dlen=0
#filetowrite=[]
stringtoAdd=""
stringtoAdd2=""
authortowrite=[]
filetowrite=[]
docLen={}
mainDict=defaultdict(list)
totalToCheck=defaultdict(list)
count=0
doclen=0
#process author for each document
def processAuthor(docID, line, lineNumber):
	n=1
	while(linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.W' and 
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.N' and
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.T' and
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.B' and
		 linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.I' and 
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.X' and
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.C' and
		linecache.getline(filetoOpen,lineNumber+n)[0:2]!='.K'):
		docAuthors[docID].append(linecache.getline(filetoOpen,lineNumber+n).strip("\n"))
		n=n+1

#process through the document and populate the arrays		
for i in readLines:
	lineNumber=lineNumber+1
	i=i.strip('\n')
	if(lineNumber>1):
			if(docInfo[docID[len(docID)-1]]<=0):
				docInfo[docID]=""
			if(docK[docID[len(docID)-1]]<=0):
				docK[docID]=""
			keys=docC.keys()
			if docid not in keys:
				docC[docid]=""
	if(i[0:2]=='.I'):
		docid=int(i[3:])
		print "Processing doc: ",docid	
		docID.insert(lineNumber-1,(int(i[3:])))
	if(i[0:2]=='.T'):
		#line=linecache.getline(filetoOpen,lineNumber+1).strip('\n')
		#docTitle[docid]=line
		line1=linecache.getline(filetoOpen,lineNumber+1).replace('\n',' ')
		next1=2
		while(line1[0:2]!='.X' and line1[0:2]!='.N' and line1[0:2]!='.B' 
			and line1[0:2]!='.I' and line1[0:2]!='.C' and line1[0:2]!='.K' 
			and line1[0:2]!='.W'):
			stringtoAdd2+=line1
			line1=linecache.getline(filetoOpen,lineNumber+next1)
			line1=line1.replace("\n"," ")
			next1=next1+1
		docTitle[docid].append(stringtoAdd2)
	if(i[0:2]=='.B'):
		line=linecache.getline(filetoOpen,lineNumber+1).strip('\n')
		docBibilo[docid]=line
	if(i[0:2]=='.A'):
		processAuthor(docid, i, lineNumber)
	if(i[0:2]=='.N'):
		line=linecache.getline(filetoOpen,lineNumber+1).strip('\n')
		nValues=string.split(line)
		for i in nValues:
			docN[docid].append(i)
	if(i[0:2]=='.K'):
		line=linecache.getline(filetoOpen,lineNumber+1).replace('\n',' ')
		next=2
		while(line[0:2]!='.X' and line[0:2]!='.N' and line[0:2]!='.B' 
			and line[0:2]!='.I' and line[0:2]!='.T' and line[0:2]!='.C' and line[0:2]!='.K'):
			stringtoAddHere+=line
			line=linecache.getline(filetoOpen,lineNumber+next).replace('\n'," ")
			next=next+1
		docK[docid].append(stringtoAddHere)
	if(i[0:2]=='.C'):
		line=linecache.getline(filetoOpen,lineNumber+1).strip('\n')
		docC[docid]=line
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
	stringtoAdd2=""
	stringtoAddHere=""	
	linecache.clearcache()

#append all of the individual arrays to the whole dictionary
#This could be done while parsing but if one wants to index only on
#either author or text or.... then this helps
for i in docID:
	mainDict[i].append(docTitle[i])
	mainDict[i].append(docBibilo[i])
	mainDict[i].append(docAuthors[i])
	mainDict[i].append(docInfo[i])
	mainDict[i].append(docN[i])
	mainDict[i].append(docC[i])
	mainDict[i].append(docK[i])

#lowe each word, and replace escape and other characters
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

	#print "returning fileT:" ,fileT	
	return fileT

#apply porter stemmer to the word and return the word
def applyStem(word):
	p = PorterStemmer()
  	word = p.stem(word, 0,len(word)-1)	
	return word

#check the frequency of the word in the document id and return it
def checkforFrequency(docid, word):
	freq=0
	count=0
	word=word[12:]
	toCheck=[]
	toApplyStem=[]
	for i in mainDict[docid]:
		if isinstance(i,ListType):
			for listTerm in i:
				if isinstance(listTerm, ListType):
					for term in lisTerm:
						toCheck.insert(count,term)
				else:
					toCheck.insert(count,listTerm)
		else:
			toCheck.insert(count, i)
		count=count+1
	for toCheckItem in toCheck:
		toCheckItem=string.split(toCheckItem)
		for items in toCheckItem:
			items=LowerPolish(items)
			items=items.strip()
			if (' ' in items):
				toApplyStem=string.split(items)
			else:
				toApplyStem.append(items)
			for item in toApplyStem:
				item=applyStem(item)
				if item.strip()==word.strip():
					freq=freq+1
			del toApplyStem[:]
	del toCheck[:]	
	return freq

#check if the word is already written
def checkifWritten(fileT, key):
	f=open(fileT,'r')
	toReturn=[]
	words_new=[]
	existing=f.readlines()
	for words in existing:
		words=string.split(words)
		words_new.append(str(words[1]))
	if str(key) in words_new:
		return False
	else: 	
		
		return True

#print docs helper
def printDocsHelper(fileT,k):
	if fileT not in stopwords:
	#stemmed words
		p = PorterStemmer()
       		fileT = p.stem(fileT, 0,len(fileT)-1) + " "
		fileT=re.sub(r'\s', '', fileT)
		if (len(fileT)>1) and (fileT not in stopwords):
			fileT="./wordFiles/" + fileT
			FILE=open(fileT,'a')
			initFreq=checkforFrequency(k,fileT)
			if checkifWritten(fileT,k):
				FILE.write(str(fileT[12:])+ " " +str(k)+ " " +str(initFreq))	
				FILE.write("\n")
				return 1
	return 0


#write the word as a file to the specified directory
def printDocuments(mainDict):
	filetowrite=[]
	count=1
	pos=0
	for k,v in mainDict.iteritems():
		dlen=0
		print "Processing document: %s" %k
		for value in v:
			if isinstance(value, ListType):
				for val in value:
					fileTemp=string.split(val)					
					for filein in fileTemp:
						filetowrite.insert(pos,filein)
						pos=pos+1
			else: 
				filetowrite=string.split(value)
			for fileT in filetowrite:
				fileRaw=fileT
				fileT=LowerPolish(fileT)
				if (' ' in fileT) == True or ('-' in fileT)==True:
					filet=string.split(fileT)
					for fileT in filet:
						dlen=dlen+printDocsHelper(fileT,k)
						
				else:
					dlen=dlen+printDocsHelper(fileT,k)

		docLen[k]=str(dlen)
		del filetowrite[:]

printDocuments(mainDict)

#return all words in specific to the given arguments
def getAllWords(line,lineNumberr,wordCount):
	countt=0
	freq=0
	toCheck=[]
	line=line.strip()
	line=line.rstrip('\n')
	words=string.split(line)
	toCheck.insert(countt,words[0])
	countt=countt+1
	toWrite=words[0]
	countWrite=0
	toPrint=toWrite
	while toWrite == toCheck[0]:
		freq=freq+int(words[2])
		countWrite=countWrite+1
		toPrint=toWrite
		lineNumberr=lineNumberr+1
		if lineNumberr < linesLength:
			flagLine=lines[lineNumberr].rstrip('\n')
		else: 
			break
		words=string.split(flagLine)
		toWrite=words[0]
	FILEone.write(str(wordCount)+" " +str(toPrint)+" " +str(lineNumberr-1)+" " +str(countWrite)+" "+str(freq))
	FILEone.write("\n")
	return countWrite

#go to the directory where the word files are written to
f=open("fileappend1","a")
for r,d,fi in os.walk("./wordFiles"):
    for files in fi:
            g=open(os.path.join(r,files))
            shutil.copyfileobj(g,f)
            g.close()
f.close()

FILEone=open("file1","a")

f=open("fileappend1","r")
lines=f.readlines()
#temp variable
lineNumberr=0
wordCount=1
linesLength= len(lines)
i=0
while i<=len(lines)-1 :
	toAdd=getAllWords(lines[i],lineNumberr,wordCount)
	lineNumberr=lineNumberr+toAdd
	wordCount=wordCount+1
	i=i+toAdd

terms={}
FILEone.close()
#a file that maps term names to term IDs and associated term information, 
#such as inverted index offset and length values and corpus frequency statistics
FILERead=open("file1","r")
r=FILERead.readlines()
for rlines in r:
	rlines=rlines.strip('\n')
	rlines=rlines.strip()
	rlines=string.split(rlines)
	terms[rlines[1]]=rlines[0]
#the inverted index file that maps term IDs to document IDs and associated term frequencies
fileTwo=open("file2","a")
for lines in lines:
	lines=string.split(lines)
	toWrite=terms[lines[0]]
	fileTwo.write(str(toWrite)+" " +str(lines[1])+" "+str(lines[2]))
	fileTwo.write("\n")
fileTwo.close()
f.close()
FILERead.close()
#le that maps document IDs to document names and associated document information, such as document lengths
file3=open('file3',"a")
for k,v in docLen.iteritems():
	file3.write(str(k)+" " +str(docLen[k]))
	file3.write("\n")
