#!/usr/bin/python 
# -*- coding: utf-8 -*-
'''
@Author: Fei Pei
@Date: 2020-04-14 16:46:56
@LastEditTime: 2020-04-14 16:47:38
@LastEditors: Fei Pei
'''

import json

class JsonAttributeError(AttributeError): pass

class JsonObject(dict):
    def __init__(self, d = None):
        if not d:
            d = {}
            
        dict.__init__(self, d)
        
        for key, value in self.iteritems():
            if isinstance(value, dict):
                self[key] = JsonObject(value)
            elif isinstance(value, list):
                for i in range(len(value)):
                    item = value[i]
                    if isinstance(item, dict):
                        value[i] = JsonObject(item)
                
    def __getattr__(self, name):
        # __getattr__ is called after __getattribute__
        return self.get(name, None)
        
    def __setattr__(self, name, value):
        if name.find('.') == -1:
            self.__set_value(name, value)            
        else:
            names = name.split('.', 1)
            child = self.get(names[0], None)
            
            if child is None:
                child = JsonObject()
                self[names[0]] = child
                
            setattr(child, names[1], value)
            
    def __set_value(self, name, value):
        if type(value) == JsonObject:
            self[name] = value
        elif type(value) == dict:
            self[name] = JsonObject(value)
        else:
            self[name] = value
                        
    def __hash__(self):
        return id(self)    
    
    @staticmethod
    def loads(json_content):
        return JsonObject(json.loads(json_content, encoding='utf-8'))
        
    def dumps(self, indent=None, ensure_ascii=True):
        result = json.dumps(self, ensure_ascii=ensure_ascii, indent=indent)
        if isinstance(result, unicode):
            result = result.encode('utf-8')

        return result

    def dumps_to_unicode(self, indent=None):
        result = json.dumps(self, ensure_ascii=False, indent=indent)
        return result
        
    def append(self, name, value):
        """Append an element to a list attr."""
        old = getattr(self, name)
        if isinstance(old, list):
            old.append(value)
        elif not old:
            setattr(self, name, [value])
        else:
            msg = 'Item:append - the old value is not list. Name: %s, Value: %s' % (name, value)
            raise JsonAttributeError(msg)
            
if __name__ == '__main__':
    user_def = {'name' : 'user123', 'password' : '123456', 
                "values" : {"a" : 1, "b" : 2} }
    
    user = JsonObject(user_def) 
    print user.name
    print user.password
    print user.email
    
    user.email = 'user123@localhost'
    print user.email
    print user
    
    user.email_verified = True
    print user
    
    user.props = {}
    user.props.sex = 'male'
    user.props.age = 26
    print user

    user = JsonObject.loads(user.dumps())
    print user, type(user)
