import math

# use a hash table for the closed list and the cache, the key will be x + sqrt(y) from the position
# use level to determine the nodes position in the array cache


class Cache:
    def __init__(self):
        self.head = None
        self.arr = []
        self.ht = HashTable()

    def findIndex(self, position):
        for i in self.arr:
            if position.equals(i):
                return self.arr.index(i)

    def buildCache(self, node):
        self.head = node
        self.arr = [None] * (node.level + 1)
        nextNode = node
        while nextNode is not None:
            self.arr[nextNode.level] = nextNode.position
            self.ht.add(nextNode.position)
            #print("looping")
            nextNode = nextNode.parent

    def completeCache(self, otherCache, node):
        self.buildCache(node)
        startPos = otherCache.findIndex(node.position)
        arraySize = (len(otherCache.arr) - startPos) + len(self.arr)
        for i in range(startPos + 1, arraySize - 1):
            self.arr.append(otherCache.arr[i])
            self.ht.add(otherCache.arr[i])
        for i in self.arr:
            print("#{} ({}, {})".format(self.arr.index(i), i.xVal, i.yVal))


class HashTable:

    def __init__(self):
        self.ht = {}
        self.size = 0

    def add(self, position):
        self.ht[position.xVal + math.sqrt(position.yVal)] = position
        self.size += 1

    def hasKey(self, position):
        try:
            return self.ht[position.xVal + math.sqrt(position.yVal)]
        except KeyError:
            return None


class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.size = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def isEmpty(self):
        return len(self.queue) == []

        # for inserting an element in the queue

    def insert(self, data):
        self.queue.append(data)
        self.size += 1

        # for popping an element based on Priority

    def delete(self):
        try:
            minimum = 0
            for i in range(len(self.queue)):
                if self.queue[i].fVal < self.queue[minimum].fVal:
                    minimum = i
            item = self.queue[minimum]
            del self.queue[minimum]
            self.size -= 1
            return item
        except IndexError:
            print()
            exit()


class grid():

    def __init__(self, xUpperBound, xLowerBound, yUpperBound, yLowerBound):
        self.xUpperBound = xUpperBound
        self.xLowerBound = xLowerBound
        self.yUpperBound = yUpperBound
        self.yLowerBound = yLowerBound
        self.arr = [[0 for i in range(xLowerBound, xUpperBound + 1)] for j in range(yLowerBound, yUpperBound + 1)]
        self.buildMap()

    def buildMap(self):
        mapFile = open("map.txt", 'r')
        for row in range(self.yLowerBound, self.yUpperBound):
            line = mapFile.readline()
            for column in range(self.xLowerBound, self.xUpperBound):
                self.arr[column][row] = int(line[column])
        mapFile.close()
        for i in self.arr:
            print(i)

    def isBarrier(self, position):
        if self.arr[position.xVal][position.yVal] == 1:
            return True

    def withinBounds(self, position):
        if position.xVal > self.xUpperBound or position.yVal > self.yUpperBound:
            return False
        if position.xVal < self.xLowerBound or position.yVal < self.yLowerBound:
            return False
        return True


class coordinate():
    def __init__(self, xVal, yVal):
        self.xVal = xVal
        self.yVal = yVal

    def equals(self, otherCoordinate):
        if self.xVal is otherCoordinate.xVal and self.yVal is otherCoordinate.yVal:
            return True
        return False

class starSearch():
    def __init__(self, openList, closedList, start, end, grid, otherCache):
        self.openList = openList
        self.closedList = closedList
        self.start = start
        self.end = end
        self.grid = grid
        self.cache = Cache()
        self.otherCache = otherCache
        self.foundGoal = False

    class Node():
        def __init__(self, fVal, gVal, position, level, parent):
            self.fVal = fVal
            self.gVal = gVal
            self.position = position
            self.level = level
            self.parent = parent

    def findPath(self):
        self.openList.insert(self.Node(0, 0, self.start, 0, None))  # inserts root node to open list
        searchCount = 0
        while not self.openList.isEmpty() and self.foundGoal is False:
            searchCount += 1
            self.successors(self.openList.delete())
        if self.foundGoal is True:
            print("Number of searches: {}".format(searchCount))
            return self.cache
        return None

    def isDiagonal(self, currentPosition, newPosition):
        xDiff = currentPosition.xVal - newPosition.xVal
        yDiff = currentPosition.yVal - newPosition.yVal
        if xDiff is not 0 and yDiff is not 0:
            return True
        else:
            return False

    def generateFVal(self, node, currentPosition, newPosition):
        return self.generateHVal(newPosition) + self.generateGVal(node.gVal, self.isDiagonal(currentPosition, newPosition))

    def generateHVal(self, newPosition):
        return math.sqrt(math.pow((self.end.xVal - newPosition.xVal), 2) + math.pow((self.end.yVal - newPosition.yVal), 2))

    def generateGVal(self, previousVal, diagonal):
        if diagonal is True:
            return previousVal + math.sqrt(2)
        return previousVal + 1

    def validPosition(self, position):
        if self.grid.withinBounds(position) and not self.grid.isBarrier(position):
            return True
        else:
            return False
        
    def unvisited(self, position):
        if self.closedList.hasKey(position) is not None:
            return False
        else:
            return True

    def isGoal(self, node):
        if node.position.xVal is self.end.xVal and node.position.yVal is self.end.yVal:
            self.printPath(node)
            print("Number of moves: {}".format(node.level))
            print("Building cache")
            self.cache.buildCache(node)
            return True
        return False

    def foundCache(self, node):
        if self.otherCache is None:
            return False
        elif self.otherCache.ht.hasKey(node.position):
            print("Completing cache")
            self.cache.completeCache(self.otherCache, node)
            return True
        else:
            return False

    def successors(self, node):
        if self.isGoal(node):
            self.foundGoal = True
            return
        elif self.foundCache(node):
            self.foundGoal = True
            return
        self.closedList.add(node.position)
        for i in range(-1, 2):
            for j in range(-1, 2):
                newPosition = coordinate(node.position.xVal + i, node.position.yVal + j)
                newNode = self.Node(self.generateFVal(node, newPosition, newPosition), node.gVal, newPosition, node.level + 1, node)
                if self.validPosition(newPosition) and self.unvisited(newPosition):
                    self.openList.insert(newNode)

    def printPath(self, node):
        arr = [None] * (node.level + 1)
        nextNode = node
        while nextNode is not None:
            arr[nextNode.level] = nextNode
            nextNode = nextNode.parent
        for i in arr:
            print("#{} ({},{})".format(arr.index(i), i.position.xVal, i.position.yVal))







if __name__ == '__main__':
    ol = PriorityQueue()
    cl = HashTable()
    ch = Cache()
    gr = grid(10, 0, 10, 0)
    searcher = starSearch(PriorityQueue(), HashTable(), coordinate(3, 6), coordinate(6, 3), gr, ch)
    ch2 = searcher.findPath()
    #print("Open list size: {}".format(ol.size))
    ol2 = PriorityQueue()
    cl2 = HashTable()
    searcher2 = starSearch(PriorityQueue(), HashTable(), coordinate(3, 6), coordinate(6, 3), gr, ch2)
    ch3 = searcher2.findPath()
    #print(cl.size)
