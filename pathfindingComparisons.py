from pygame_functions import *
import pathfindingAlgorithms



screenSize(840,840)
setBackgroundColour("black")

class Node():
	def __init__(self, name, x, y):
		self.name = name
		self.links = {}
		self.xCoord = x
		self.yCoord = y
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
		self.shortestDistanceFromStart = None # These are used for the pathfinding algorithm
		self.visited = False
		self.previous = None
		self.fullPathEstimate = None
		
	def __str__(self):
		return "Node " + str(self.name)

	
def drawmap(map,current):
	clearShapes()
	#draw nodes
	for y in range(len(map)):
		for x in range(len(map[y])):
			if map[y][x]:
				map[y][x].drawMe(current)
	
	# draw links
	for y in range(len(map)):
		for x in range(len(map[y])):
			if map[y][x]:
				for link in map[y][x].links:
					drawLine(map[y][x].xCoord, map[y][x].yCoord, link.xCoord, link.yCoord,"grey")

def drawPath(current):
	while current.previous != None:
		current.highlightMe()
		current = current.previous
	
def clearPaths(graph):
	for node in graph:
		if node:
			node.clearPath()
		

def createLinks(map):
	# link the nodes
	def joinNodes (x1, y1, x2, y2):
		if map[y1][x1] and map[y2][x2]:
			map[y1][x1].makeLink(map[y2][x2], 40)  # set a standard distance of 40
			
	for y in range(len(map)):
		for x in range(len(map[0])):
			if map[y][x]:
				#link up
				if y > 0:
					joinNodes(x,y,x,y-1)
				#link down
				if y <len(map)-1:
					joinNodes(x,y,x,y+1)
				#link left
				if x > 0:
					joinNodes(x,y,x-1,y)
				#link right
				if x <len(map[0])-1:
					joinNodes(x,y,x+1,y)	

def makeGraph(map):
	graph = []
	for y in range(12):
		for x in range(5):
			if map[y][x]:
				graph.append(map[y][x])
	return graph

def setup():
	#make a 5 by 12 grid of nodes	
	map = []
	for y in range(12):
		map.append([])
		for x in range(5):
			map[y].append(Node(str(y)+ ":" + str(x), 50+x*40, 50+y*40))
			
	# Delete the inaccessible areas
	for y in range(1,4):
		for x in range(1,3):
			map[y][x] = None
			
	for y in range(5,8):
		for x in range(2,4):
			map[y][x] = None
			
	for y in range(9,10):
		for x in range(1,5):
			map[y][x] = None	
			
	for y in range(10,11):
		for x in range(1,4):
			map[y][x] = None
			
	# put all nodes into a list
	graph = makeGraph(map)
	createLinks(map)
	return  graph, map

graph, map = setup()
start = map[0][2]
drawmap(map, start)
label = makeLabel("Click to select target",18,10,10,"white")
showLabel(label)
while True:
	if mousePressed():
		x = mouseX()
		y  = mouseY()
		nearestNodePointX = (x-40)//40
		nearestNodePointY = (y-40)//40
		target = map[nearestNodePointY][nearestNodePointX]
		drawmap(map, start)
		clearPaths(graph)
		changeLabel(label,"using Bruteforce")
		pause(2000)
		graph, checksmade = pathfindingAlgorithms.bruteForce(graph,start,target)
		drawPath(target)
		changeLabel(label,"Checks made: " + str(checksmade))
		pause(2000)
		drawmap(map, start)
		clearPaths(graph)		
		changeLabel(label,"using Dijkstra")
		pause(2000)
		graph, checksmade = pathfindingAlgorithms.dijkstra(graph, start, target )
		drawPath(target)
		changeLabel(label,"Checks made: " + str(checksmade))
		pause(2000)
		drawmap(map, start)
		clearPaths(graph)		
		changeLabel(label,"using A*")
		pause(2000)
		graph = pathfindingAlgorithms.generateAStarWeights(graph, target)
		graph, checksmade = pathfindingAlgorithms.AStar(graph, start, target )
		drawPath(target)
		# PathFindingAlgorithms.printNodeTable(graph,target)
		changeLabel(label,"Checks made: " + str(checksmade))		
	pause(10)

endWait()


