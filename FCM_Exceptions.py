# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 22:19:01 2016

@author: Eric
"""

class FCMConstructionError(Exception) :

    def __init__(self,message,errors) :

      message=message+" : "+str(errors)
      super(Exception, self).__init__(message)



class InvalidWeightError(FCMConstructionError) :

    def __init__(self,errors,message="Invalid weight for an edge ") :

        super(InvalidWeightError,self).__init__(message,errors)

class ConceptExistError(FCMConstructionError) :

    def __init__(self,errors,message="Concept does not exist ") :

        super(ConceptExistError,self).__init__(message,errors)

class EdgeExistError(FCMConstructionError) :

    def __init__(self,errors,message="Edge does not exist between ") :

        e=str(errors[0])+" - "+str(errors[1])
        super(EdgeExistError,self).__init__(message,e)



class InvalidConceptValueError(FCMConstructionError) :

    def __init__(self,errors,message="Invalid Concept value ") :

        super(InvalidConceptValueError,self).__init__(message,errors)