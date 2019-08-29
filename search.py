import re

from ast import literal_eval
from PorterStemmer import PorterStemmer
from TextProcessor import TextProcessor
import json
import sys

titleIndex = {}
bodyIndex = {}
infoboxIndex = {}
catIndex = {}
extIndex ={}
refIndex = {}
title ={}
stemmer = PorterStemmer()
txtProcessor = TextProcessor()

def read_index_file(path_to_index,index_name):
    file=open(path_to_index+'/'+index_name+'Index.txt','r')
    file = file.read()
    idx = file.find('{')
    file = file[idx:]
    file = file[:-1]
    file = file.replace("\'", "\"")
    a = json.loads(file)
    return a
    
def load_index_files(path_to_index):
    
    global titleIndex
    global bodyIndex
    global infoboxIndex
    global catIndex
    global extIndex
    global refIndex
    global title
    
    bodyIndex = read_index_file(path_to_index, 'body')
    titleIndex = read_index_file(path_to_index, 'title')
    infoboxIndex = read_index_file(path_to_index, 'infobox')
    catIndex = read_index_file(path_to_index, 'category')
    extIndex = read_index_file(path_to_index, 'external')
    refIndex = read_index_file(path_to_index, 'reference')
    
    file=open(path_to_index+'/title.txt','r')
    file = file.read()
    title = literal_eval(file)
    

def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')

def processFieldQuery(query):
    query = query.split(' ')
    fieldToQueryTerm = {}
    
    for q in query:
        q = q.split(':')
        term = q[1]
        term = txtProcessor.cleanTextData(''.join(term))
        term = ''.join(term)        
        fieldToQueryTerm[q[0]] = term
    output = []
    for key,value in fieldToQueryTerm.items():
        try:
            if key=='title':
                docDict = titleIndex[value]
                for docId in docDict:
                    output.append(title[int(docId)])
            elif key=='body':
                docDict = bodyIndex[value]
                for docId in docDict:
                    output.append(title[int(docId)])
            elif key=='infobox':
                docDict = infoboxIndex[value]
                for docId in docDict:
                    output.append(title[int(docId)])
            elif key=='category':
                docDict = catIndex[value]
                for docId in docDict:
                    output.append(title[int(docId)])
            elif key=='ref':
                docDict = refIndex[value]
                for docId in docDict:
                    output.append(title[int(docId)])
            elif key=='ext':
                docDict = extIndex[value]
                for docId in docDict:
                    output.append(title[int(docId)])
        except KeyError:
            continue
                     
    if len(output)>10:
        output = output[0:10]
    
    return output   


def processNormalQuery(query):
    output = []
    query = query.lower()
    query = txtProcessor.tokenize(query)
    query = txtProcessor.cleanTokenList(query)
    
    for word in query:
        try:       
            if word in titleIndex:
                docIds = titleIndex[word]
                for docId in docIds:
                    output.append(title[int(docId)])
            if word in bodyIndex:
                docIds = bodyIndex[word]
                for docId in docIds:
                    output.append(title[int(docId)])
            if word in infoboxIndex:
                docIds = infoboxIndex[word]
                for docId in docIds:
                    output.append(title[int(docId)])
            if word in catIndex:
                docIds = catIndex[word]
                for docId in docIds:
                    output.append(title[int(docId)])
            if word in refIndex:
                docIds = refIndex[word]
                for docId in docIds:
                    output.append(title[int(docId)])
            if word in extIndex:
                docIds = extIndex[word]
                for docId in docIds:
                    output.append(title[int(docId)])  
        except KeyError:
            continue 
        
    if len(output)>10:
        output = output[0:10]
    
    return output
            
def processQuery(query):
    if re.search('[title|body|infobox|category|ref|ext]:', query):
        output = processFieldQuery(query)
    else:
        output = processNormalQuery(query)
    return output

def search(path_to_index, queries):
    '''Write your code here'''
    outputs = []
    queries = ''.join(queries).split('\n')
    for query in queries:
        output = processQuery(query)
        outputs.append(output)
    return outputs

def main():
    path_to_index = sys.argv[1] #index folder
    if path_to_index[-1]=='/':
        path_to_index = path_to_index[:-1]
    testfile = sys.argv[2]    # query file
    path_to_output = sys.argv[3] 
    load_index_files(path_to_index)
    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)


if __name__ == '__main__':
    #startTime= time.clock()
    main()
    #stopTime = time.clock()
    #print(stopTime - startTime) 