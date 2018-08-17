import networkx as nx
import matplotlib.pyplot as plt
from types import FunctionType
import inspect
import sys


'''
This is a Python package for Fuzzy Cognitive Maps
'''

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












class FCM :

    '''
    This is the constructor for the Fuzzy graph.
    It initializes the networkx Digraph
    '''
    def __init__(self) :

        self._fcm_graph=nx.DiGraph()


    '''
    This method is an interface for the add_node
    method of DiGraph
    '''
    def add_concept(self,concept) :

      self._fcm_graph.add_node(concept)
      self._fcm_graph.node[concept]['value']=0.0
      return

    '''
    This method is an interface for the add_edge
    method of Digraph.It checks whether the
    weight provided is the range of [-1,1].
    If the node does not exist,we create them
    before creating the edge.
    '''

    def add_edge(self,concept1,concept2,weight) :

        if weight<-1.0 or weight >1.0 :           # Error checking for the weight

             raise InvalidWeightError(weight)



        if concept1 not in self._fcm_graph.nodes() :   # If the node doesnt exist,create the node
            self.add_concept(concept1)

        if concept2 not in self._fcm_graph.nodes() :   # If the node doesnt exist,create the node
            self.add_concept(concept2)

        self._fcm_graph.add_edge(concept1,concept2,weight=weight) # Adding the edge

    '''
    This method removes edges from the fcm graph.
    It also checks if the nodes exist and if the edge
    exists.
    '''
    def remove_edge(self,node1,node2) :

        if node1 not in self._fcm_graph.nodes()  :
            raise ConceptExistError(node1);

        if  node2 not in self._fcm_graph.nodes() :
            raise ConceptExistError(node2)


        if not self._fcm_graph.has_edge(node1,node2) :
            nodes=[node1,node2]
            raise EdgeExistError(nodes)

        self._fcm_graph.remove_edge(node1,node2)


    '''
    This method is an interface for
    the remove_node() .If the node
    does exist,it prints an error
    message and returns.
    '''
    def remove_concept(self,concept) :

        if concept not in self._fcm_graph.nodes() :

            raise ConceptExistError(concept)



        self._fcm_graph.remove_node(concept)
        return True


    '''
    This method is an interface for
    nodes().It returns the dictionary of
    concepts in the graph having the node of the value as value and the concept as the key.
    '''

    def concepts(self) :
      dictToReturn = {}
      for node in self._fcm_graph.nodes():
       dictToReturn[node] = self._fcm_graph.node[node]['value']
      return dictToReturn

    '''
    This method adds an attribute to
    a node and accepts either an integer
    of a function which returns an integer
    '''

    def set_value(self,concept,num) :

        if concept not in self._fcm_graph.nodes() :   # Error if the given concept does not exist
            raise ConceptExistError(concept)



        if type(num) is int or type(num) is float  :             # If the parameter passed is an int,add it to the attribute

          if num>=-1.0 and num<=1.0 :
            self._fcm_graph.node[concept]['value']=num
          else :
            raise InvalidConceptValueError(num)

        elif type(num) is FunctionType or type(num) is self.FunctionType :

            param_length=(inspect.getargspec(num)[0])


            if len(param_length)!=0 :
                raise InvalidConceptValueError(num)

            self._fcm_graph.node[concept]['value']=num()

        else :
            raise InvalidConceptValueError(num)





    '''
    This method is an interface for the draw()
    in the networkx package.We draw the DiGraph
    using spring layout and labels with the help
    of matplotlib
    '''
    def draw(self) :

       nx.draw(self._fcm_graph,pos=nx.spring_layout(self._fcm_graph),with_labels=True)
       plt.show()