#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:09:26 2020

@author: vamshi_kiran
"""

import re

class item():
    
    def __init__(self,Id,freq):
        self.id = Id
        self.freq = freq
    
    def __repr__(self):
        return str(self.__dict__)

class DB_config():
    
    def __init__(self):
        self.db={}
    
    def __repr__(self):
        return str(self.__dict__)
    
    def add(self, doc):
        return self.db.update({doc['id']: doc})
    
    def get(self, id):
        return self.db.get(id, None)

class indexing():
    
    def __init__(self,db):
        self.index={}
        self.db=db
    def __repr__(self):
        return str(self.__dict__)
    
    def index_document(self, doc):
        clean_text = re.sub("[^\w\s]","",doc['text'])
        terms = clean_text.split(" ")
        index_dict = {}
        for term in terms:
            freq = index_dict[term].freq if term in index_dict else 0
            index_dict[term] = item(doc['id'],freq+1)
        update_dict = { key : [item]
                        if key not in self.index
                        else self.index[key]+[item]
                        for key,item in index_dict.items() }
        self.index.update(update_dict)
        self.db.add(doc)
        return doc
    
    def lookup(self,query):
        return {term:self.index[term] for term in query.split(' ') if term in self.index}
        
  
def highlight_term(id, term, text):
    replaced_text = text.replace(term, "\033[1;32;40m {term} \033[0;0m".format(term=term))

    return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)

db = DB_config()
index = indexing(db)
doc1 = {
    'id': '1',
    'text': 'The big sharks of Belgium drink beer.'
}
doc2 = {
    'id': '2',
    'text': 'Belgium has great beer. They drink beer all the time.'
}
index.index_document(doc1)
index.index_document(doc2)


search_term = "beer"
result = index.lookup(search_term)

for term in result.keys():
    for appearance in result[term]:
        document = db.get(appearance.id)
        print(highlight_term(appearance.id, term, document['text']))      
