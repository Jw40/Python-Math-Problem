from itertools import zip_longest
import csv

# You can define some helper functions here if you like!

# modified from CAB203 digraphs.py

# vertices connected by an edge from u.
def N_out(V, E, u):
    return { v for v in V if (u,v) in E }

def findPath(V, E, start, end, path = None):
   """Given a (directed) graph (V,E), outputs a list of vertices forming a (directed) path from start to end.  If no such path exists, returns None.
   
   Implemented using a simple DFS algorithm."""
   # Take care of starting case so user doesn't have to supply the empty path
   if path is None: path = [ start ]  
   
   # Base case:
   if start == end: return path

   # Search through neighbours.  Ignore vertices that are already on the path 
   # so we don't create a cycle.
   for v in N_out(V, E, start):
      if v in path:
         continue
      path.append(v)
      # try to find end by going through v.  If we do, then we have found the path.
      r = findPath(V, E, v, end, path)
      if r is not None: return path
      path.pop()

   # If we haven't returned yet, then we can't find the end going this direction.
   return None

def augmentingEdges(V, E, w, f):
   """Given an anti-symmetric directed graph, edge weights w, and a valid flow f, returns an edge set representing edges that can be in an augmenting path. """
   # forward edges
   E1 = { (u,v) for (u,v) in E if f[(u,v)] < w[(u,v)] }

   # backward edges
   E2 = { (v,u) for (u,v) in E if f[(u,v)]  > 0 }
   return E1 | E2

def augmentingPath(V, E, w, f, s, d):
   """Given an anti-symmetric directed graph, edge weights w, and a valid flow f, source vertex s and drain vertex d, returns an augmenting path as a list of vertices."""
   Enew = augmentingEdges(V, E, w, f)
   return findPath(V, Enew, s, d)


def edgeCap(w, f, u, v):
   """Given edge weights w, flow f, and edge (u,v), returns the augmenticy capacity of the edge."""
   if (u,v) in f:
      return w[(u,v)] - f[(u,v)]

   return f[(v,u)]

def augmentingPathCapacity(path, f, w):
   """Given an augmenting path, edge weights w and a valid flow f, returns the capacity of the augmenting path."""
   cap = edgeCap(w, f, path[0], path[1])

   # search over all edges in the path
   for (u,v) in zip(path[1:-1], path[2:]):
      ecap = edgeCap(w, f, u, v)
      cap = ecap if ecap < cap else cap

   return cap

def augmentFlow(path, f, w):
   """Given an augmenting path, edge weights w and a valid flow f, returns a valid flow g augmented along the augmenting path."""
   g = dict(f)
   a = augmentingPathCapacity(path, f, w)
   for u,v in zip(path[:-1], path[1:]):
      if (u,v) in f:         
         g[(u,v)] = f[(u,v)] + a
      else:
         g[(v,u)] = f[(v,u)] - a
   return g

def maxFlow(V, E, w, s, d):
   """Given an anti-symmetric directed graph, edge weights w, a valid flow f, source vertex s and drain vertex d, returns a maximum flow. """
   f = { e: 0 for e in E }  # initial flow all 0

   # augment along augmenting paths as long as we can
   while (path := augmentingPath(V, E, w, f, s, d)) is not None:
      f = augmentFlow(path, f, w)
   return f

def optimiseWidgets(filename):
   # Code your solution here

   # open the file in read mode  
   filename = open(filename, 'r')

   # creating dictreader object
   file = csv.DictReader(filename)
   #convert dict to list
   list_of_dict = list(file)

   # creating empty lists
   machine = []
   input = []
   output = []
   capacity = []

   # iterating over each row and append
   # values to empty list
   for col in list_of_dict:
      machine.append(col['Machine'])
      input.append(col['Input'])
      output.append(col['Output'])
      capacity.append(col['Capacity'])
   
   #convert the input and output lists into sets 
   inputset = set(input)
   outputset = set(output)
   
   #debug
   #print(input)
   #print(inputset)
   
   #unique elements in either input or output 
   set_difference = inputset.union(outputset)

   #initalize string variables used below in the for loops 
   feedStock = ""
   finalProduct = ""

   #find the unique elemements within 2 different lists, if it is only in 1 of the sets but not both
   checker = list(set(inputset).symmetric_difference(set(outputset)))

   #check if the item was in the input list (feed stock)
   for item in input:
      if item in checker:
         feedStock = item

   #check if the item was in the output lsit(final product)
   for item in output:
      if item in checker:
         finalProduct = item

   #debug
   #print("FeedStock =", feedStock)
   #print("FinalProduct =", finalProduct)

   #combine the input and output into a tuple ((p[0], q[0]), (p[1],q[1]),...)
   zipped = zip_longest(input,output)
   zipped2 = zip_longest(input,output)

   #convert capacity list from string to int
   #modified from: https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
   for i in range(0, len(capacity)):
      capacity[i] = int(capacity[i])

   #create a new dictonary with key ((input, output) : capacity)
   Dic = dict(zip(zipped, capacity))

   #create a new dictonary with ((input, output) : machine)
   Dic2 = dict(zip(zipped2, machine))

   #create variables for graph to pass to maxFlow in digraphs
   # V = the Vertices in the graph (unique elements in the input or output set)
   # w = the neighbours inbetween the verticies (relationship between the input and output sets)
   # E = the capacity of the edge (machine capacity)
   # s = the deduced feed stock 
   # d = the deduced final product 
   V = set_difference
   w = Dic
   E = set(w.keys())
   s = feedStock
   d = finalProduct

   #call to maxflow in digraphs to find the optimal soulation (DFS)
   digraphOutput = (maxFlow(V, E, w, s, d))

   #debug
   #print(digraphOutput)

   #combine the two dicontaries, Dic and Dic2, this holds the relationship between the input/out and capacity and the relationship between the input/out and machine
   #modified from: https://www.delftstack.com/howto/python/change-the-key-in-a-dictionary-in-python/
   machineSettings = (dict([(Dic2.get(key), value) for key, value in digraphOutput.items()]))
   return machineSettings 

## TEST HARNESS
# The following will be run if you execute the file like python3 widget_n1234567.py widgetsamplefile.csv
# Your solution should not depend on this code.
if __name__ == '__main__':
   import sys

   if len(sys.argv) < 2:
      print("Please provide a filename for the input CSV file.")
      sys.exit(1)

   filename = sys.argv[1]
   solution = optimiseWidgets(filename)
   print(solution)