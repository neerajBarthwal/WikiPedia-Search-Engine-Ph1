import xml.sax.handler
from TextProcessor import TextProcessor
from IndexBuilder import IndexBuilder
import time
import sys

class DataHandler(xml.sax.handler.ContentHandler):

    '''
        SAX Parser
    '''
    flag = False
    
    def __init__(self):
        self.titleFound = False
        self.idFound = False
        self.textFound = False
        self.docId = ""
        self.title=""
        self.text=""
        self.indexFileNumber = 0
        self.offset = 0
        self.outputDir = ""
        self.index = {}
        self.titleTermFreq = {}
        self.infoBoxTermFreq={}
        self.bodyTermFreq = {}
        self.categoryTermFreq = {}
        self.externalLinkTermFreq = {}
        self.referenceTermFreq = {}
        self.docIdCounter = 0
        self.docIdTitleMapping = {}
        self.textProcessor = TextProcessor()
        self.indexBuilder = IndexBuilder()
        self.docIdToTextMapping = {}
        
    def startElement(self, name, attrs):
        
        '''
        Invoked when a start of a tag is seen by SAX API
        '''
        if name=="id" and not self.idFound:
            self.docId =""
            self.idFound = True
        
        if name =="title" and not self.titleFound:
            self.title=""
            self.titleFound = True
        
        if name == "text" and not self.textFound:
            self.text = ""
            self.textFound = True
    
    def characters(self, content):
        '''
        Invoked when characters inside a tag are found
        '''
        if self.idFound:
            self.docId+=content
        
        elif self.titleFound:
            self.title+=content
            self.docIdTitleMapping[self.docIdCounter] = content
                    
        elif self.textFound:
            self.text+=content
            
    def endElement(self, name):
        '''
        Invoked when a tag end is encountered
        '''
        if name=="id":
            self.idFound = False
        elif name == "title":
            self.titleFound = False
        elif name=="text":
            self.textFound = False
            self.text = self.text.lower()
            self.docIdToTextMapping[self.docIdCounter] = self.text
            self.docIdCounter+=1
            
        elif name=="page":
            DataHandler.flag = False

def main():
    
    if len(sys.argv)!=3:
        print("Invalid Input.\n Correct Usage: python Parser.py <path_of_xml_dump> <path_of_index_folder>") 
        
    path_to_dump = sys.argv[1]
    path_to_index = sys.argv[2]
    
    if path_to_index[-1]=='/':
        path_to_index = path_to_index[:-1]
    
    xmlparser = xml.sax.make_parser()
    handler = DataHandler()
    xmlparser.setContentHandler(handler)
    xmlparser.parse(path_to_dump)
    
    IndexBuilder.INDEX_ROOT_DIR = path_to_index
    
    processedTitleBulk = handler.textProcessor.processTitleBulk(handler.docIdTitleMapping)
    processedTextBulk = handler.textProcessor.processTextBulk(handler.docIdToTextMapping)
    
    handler.indexBuilder.buildIndexBulk(processedTextBulk,processedTitleBulk,handler.docIdTitleMapping)
    handler.docIdToTextMapping={}
    handler.docIdTitleMapping={}
    
    
if __name__ == "__main__":
    startTime= time.clock()
    main()
    stopTime = time.clock()
    print(stopTime - startTime)   