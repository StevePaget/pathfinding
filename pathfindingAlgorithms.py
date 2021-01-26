import math
from pygame_functions import *

class Node():
	def __init__(self, name, x, y, heuristicWeight=None):
		self.name = name
		self.links = {}
		self.xCoord = x
		self.yCoord = y
		self.heuristicWeight = heuristicWeight
		self.clearPath()


	def makeLink(self, otherNode, distance):			# this is just used for setting up the node links at the start
		if not otherNode in self.links:
			self.links[otherNode] = distance 	# it creates a bidirectional link of the same distance between both
			otherNode.links[self] = distance



	def drawMe(self,current):
		if self == current:
			drawEllipse(self.xCoord,  self.yCoord, 20,20, "red")
		else:
			drawEllipse(self.xCoord,  self.yCoord, 20,20, "grey")

	def highlightMe(self):
		drawEllipse(self.xCoord,  self.yCoord, 20,20, "yellow")

	def clearPath(self):
		self.shortestDistanceFromStart = None # These are used for the pathfinding algorithms
		self.visited = False
		self.previous = None
		self.fullPathEstimate = None

	def __str__(self):
		return "Node " + str(self.name)



def printAstarNodeTable(graph, current): # this is just to make it easier to see what is going on
	print("Current node table:")
	print("Node       Visited     pathDist   Heuristic  FullPath  Previous")
	for node in graph:
		print(str(node) + "       " + str(node.visited).rjust(5) + "     " + str(node.shortestDistanceFromStart).rjust(6) + "    " + str(node.heuristicWeight).rjust(6) + "       " + str(node.fullPathEstimate).rjust(6)+ "     " + str(node.previous).rjust(6), end = "")
		if current == node:
			print ("<-- Current")
		else:
			print()
	
	
def dijkstra(graph, start,end):
	'''This is a more efficient method than brute force. Although still checking all node links, it discards routes early if it has already found a shorter alternative.'''
	
	checksmade = 0
	current = start
	current.shortestDistanceFromStart = 0
	while current != end:
		for linkedNode in current.links:
			checksmade +=1
			if linkedNode.shortestDistanceFromStart == None or current.shortestDistanceFromStart + current.links[linkedNode] < linkedNode.shortestDistanceFromStart:
				linkedNode.shortestDistanceFromStart = current.shortestDistanceFromStart + current.links[linkedNode] # update the distances
				linkedNode.previous = current #  mark this as the previous node
				
		#now mark the current node as visited because we checked every link that leads from it.
		current.visited = True
		# now find the unvisited node with the shortest path
		shortest = None
		for thisnode in graph:
			checksmade +=1
			if thisnode.visited == False and thisnode.shortestDistanceFromStart != None and (shortest==None or thisnode.shortestDistanceFromStart < shortest):
				shortest = thisnode.shortestDistanceFromStart
				current = thisnode
	#printNodeTable(graph,current)
	return graph, checksmade

def generateAStarWeights(graph, target):
	'''this takes each node in the graph and calculates its distance from the target based on the node's XCoord and YCoord properties
	It just uses Pythagoras for this caculation'''
	for node in graph:
		node.heuristicWeight = int(math.sqrt((target.xCoord - node.xCoord)**2 + (target.yCoord - node.yCoord)**2))
	return graph
	
def AStar(graph, start, end):
	'''This uses the A* algorithm, which uses a heuristic to try to guess the likely direction 
	it requires a graph where the nodes have XCoord and YCoord variables, for the estimation of distance to the end node.'''
	
	start.shortestDistanceFromStart = 0
	start.fullPathEstimate = start.heuristicWeight
	checksmade = 0
	current = start
	while not end.visited:
		for linkedNode in current.links:
			if linkedNode.visited == False:
				checksmade +=1
				if linkedNode.fullPathEstimate == None or current.shortestDistanceFromStart + current.links[linkedNode] + linkedNode.heuristicWeight < linkedNode.fullPathEstimate:
					linkedNode.fullPathEstimate = current.shortestDistanceFromStart + current.links[linkedNode] + linkedNode.heuristicWeight # update the distances
					linkedNode.shortestDistanceFromStart = current.shortestDistanceFromStart + current.links[linkedNode]
					linkedNode.previous = current #  mark this as the previous node

		#now mark the current node as visited because we checked every link that leads from it.
		current.visited = True
		#printNodeTable(graph,current)
		# now find the unvisited node with the shortest path
		shortest = None
		for thisnode in graph:
			checksmade +=1
			if thisnode.visited == False and thisnode.fullPathEstimate != None and (shortest==None or thisnode.fullPathEstimate < shortest):
				shortest = thisnode.fullPathEstimate
				current = thisnode
		printAstarNodeTable(graph,current)
	return graph, checksmade

			



def DistanceToExit(fromNode, toNode, distanceSoFar, path, checksmade): 
	'''This is a recursive procedure that tries every possible route from the fromNode to the toNode and
	checks the distances of each. It then finds the shortest route.
	Note that it does not compare routes until it has reached the very end node, so it does not discard routes earlier if
	a shorter path to the same node already exists'''
	
	#print("checking path:")
	#for node in path:
		#print(str(node), end="->")
	#print ()
	
	copyPath = path[:]
	distanceSoFar+=1
	copyPath.append(fromNode)
	if fromNode==toNode: # We have arrived at an exit
		return copyPath, distanceSoFar, checksmade
	
	shortestDist = None
	bestPath = None
	
	for linkedNode in fromNode.links:
		checksmade +=1
		if linkedNode not in copyPath:
			testpath, testDistance, checksmade = DistanceToExit(linkedNode,toNode,distanceSoFar,copyPath, checksmade)
			if testpath != None:
				if shortestDist == None or testDistance < shortestDist: # this is the best so far
					shortestDist = testDistance
					bestPath = testpath
					
	return bestPath, shortestDist, checksmade
				

def bruteForce(graph, start,end):
	'''This calls the recursive procedure, DistanceToExit, shown above'''
	
	bestpath, shortestDist, checksmade = DistanceToExit(start, end, 0, [], 0)
	for nodenum in range(len(bestpath)-1,0,-1):
		bestpath[nodenum].previous = bestpath[nodenum-1]
	return graph, checksmade


def readPathFromGraph(graph, endNode):
	# this takes a graph which has been previously run through one of the algorithms
	# and reads back from the end node to the start, using the .previous property to track
	# the route
	thisNode = endNode
	path = []
	while thisNode.previous != None:
		path.insert(0,str(thisNode))
		thisNode = thisNode.previous
	path.insert(0,str(thisNode))
	return path
	
	
	
if __name__ == "__main__":
	nodetable = []
	# make the nodes
	
	# This uses the image shown in the textbook (Hodder Computer Science for A Level) on page 63
	# The second and third numbers are x-and-y coordinates, if this node is on a spacial map
	# The final number is a heuristic weight used in the A-Star algorithm (see page 72)
	
	nodeA = Node("A",0,0,95)
	nodeB = Node("B",0,0,80)
	nodeC = Node("C",0,0,90)
	nodeD = Node("D",0,0,75)
	nodeE = Node("E",0,0,70)
	nodeF = Node("F",0,0,65)
	nodeG = Node("G",0,0,50)
	nodeH = Node("H",0,0,45)
	nodeI = Node("I",0,0,25)
	nodeJ = Node("J",0,0,0)
	
	
	
	# link them
	nodeA.makeLink(nodeB,50) # we don't need to link back from B to A, as the link is made symmetrically
	nodeA.makeLink(nodeC,25)
	nodeB.makeLink(nodeD,25)
	nodeB.makeLink(nodeI,80)
	nodeC.makeLink(nodeF,50)
	nodeC.makeLink(nodeE,45)
	nodeD.makeLink(nodeF,10)
	nodeD.makeLink(nodeI,70)
	nodeE.makeLink(nodeH,35)
	nodeE.makeLink(nodeG,30)
	nodeF.makeLink(nodeH,25)
	nodeG.makeLink(nodeJ,80)	# notice an error in the text book on page 64, where H joins to J??
	nodeI.makeLink(nodeJ,30)
	
	# make a graph from them
	
	graph = [nodeA,nodeB,nodeC,nodeD,nodeE,nodeF,nodeG,nodeH,nodeI, nodeJ]	
	
	print("Seatching using brute force:")
	graph, checksmade = bruteForce(graph, nodeA, nodeJ)
	print(checksmade, "checks made")
	print (readPathFromGraph(graph, nodeJ))
	
	print("Searching using Dijkstra:")
	graph, checksmade = dijkstra(graph, nodeA, nodeJ)
	print(checksmade, "checks made")
	print (readPathFromGraph(graph, nodeJ))
	
	for node in graph:
		node.clearPath()
	print("Searching using A*:")
	graph, checksmade = AStar(graph, nodeA, nodeJ)
	print(checksmade, "checks made")	
	print (readPathFromGraph(graph, nodeJ))
