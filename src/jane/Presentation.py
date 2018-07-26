'''
Created on 25 Jul. 2018

@author: pengwang
'''

class Presentation(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    def listHead(self,data):
        head=data.columns
        head2=data.index.levels[0].tolist()
        return(head,head2)
    
      
    def listRow(self,col,accountName,data):
        return data.query("name=='"+accountName+"'")[col].tolist()
        