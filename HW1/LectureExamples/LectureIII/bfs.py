from graphs import *
def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'): #Create 7 nodes
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence')))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g


def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result
def BFS(graph, start, end, toPrint = False):
    #initalizes paths
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        #temporary path is first element in pathque
        tmpPath = pathQueue.pop(0)
        if toPrint:
            print('Current BFS path:', printPath)
        #stores final node in tmpPath in lastNode
        lastNode = tmpPath[-1]
        if lastNode == end:
            #checks if target node has been reached
            return tmpPath
        #iterates through child nodes
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath: #prevents looping
                #initalizes newPath with the temporary path and node in tmpPath
                newPath = tmpPath + [nextNode]
                #adds new path to the queue
                pathQueue.append(newPath)
    return None


def shortestPath(graph, start, end, toPrint=False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)

def testSP(source, destination):
    g = buildCityGraph(Digraph)
    sp = shortestPath(g, g.getNode(source), g.getNode(destination),
                      toPrint = True)
    if sp != None:
        print('Shortest path from', source, 'to',
              destination, 'is', printPath(sp))
    else:
        print('There is no path from', source, 'to', destination)

testSP('Boston', 'Phoenix')

