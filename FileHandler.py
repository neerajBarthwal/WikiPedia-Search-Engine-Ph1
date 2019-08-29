import json
from collections import defaultdict

class FileHandler:
    
    
    def __init__(self):
        pass

    def createIndexByFields(self,rootDir,index,wordsOfIndex):
        title = defaultdict(list)
        infobox = defaultdict(list)
        body = defaultdict(list)
        category = defaultdict(list)
        references = defaultdict(list)
        externalLink = defaultdict(list)
                
        for word in wordsOfIndex:
            postings = index[word]
            
            for entry in postings:
                entry = entry.split(' ')
                docId = entry[0]
                
                if entry[1]!='0':
                    title[word].append(docId)
                if entry[2]!='0':
                    body[word].append(docId)
                if entry[3]!='0':
                    infobox[word].append(docId)
                if entry[4]!='0':
                    category[word].append(docId)
                if entry[5]!='0':
                    externalLink[word].append(docId)
                if entry[6]!='0':
                    references[word].append(docId)
                          
        with open(rootDir+'/titleIndex.txt', 'w') as indexHandle:
            indexHandle.write(str(title))
        
        with open(rootDir+'/bodyIndex.txt', 'w') as indexHandle:
            indexHandle.write(str(body))
             
        with open(rootDir+'/categoryIndex.txt', 'w') as indexHandle:
            indexHandle.write(str(category))
            
        with open(rootDir+'/infoboxIndex.txt', 'w') as indexHandle:
            indexHandle.write(str(infobox))
            
        with open(rootDir+'/externalIndex.txt', 'w') as indexHandle:
            indexHandle.write(str(externalLink))
        
        with open(rootDir+'/referenceIndex.txt', 'w') as indexHandle:
            indexHandle.write(str(references))
                    
            
    def writeIndexToDisk(self,rootDir,index,indexFileNumber):  
        #sort the index on terms obtained from corpus
        words = sorted(index)
        self.createIndexByFields(rootDir, index, wordsOfIndex=words)

         
    def writeDocIdTitleMappingToDisk(self,rootDir,docIdTitleMapping):
        
        with open(rootDir+'/title.txt', 'w') as indexHandle:
            indexHandle.write(str(docIdTitleMapping))
        