import math

# use a hash table for the closed list and the cache, the key will be x + sqrt(y) from the position

class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def isEmpty(self):
        return len(self.queue) == []

        # for inserting an element in the queue

    def insert(self, data):
        self.queue.append(data)

        # for popping an element based on Priority

    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max]:
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()

class grid():
    yUpperBound = 10
    yLowerBound = 0
    xUpperBound = 10
    xLowerBound = 0

    def isBarrier(self, position):
        asdf = 1
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

class starSearch():
    def __init__(self, openList, closedList, start, end, grid):
        self.openList = openList
        self.closedList = closedList
        self.start = start
        self.end = end
        self.grid = grid

    class Node():
        def __init__(self, fVal, position, level, parent):
            self.fVal = fVal
            self.position = position
            self.level = level
            self.parent = parent

    def findPath(self):
        self.openList.insert(self.Node(0, self.start, 1, None))  # inserts root node to open list
        while not self.openList.isEmpty():
            self.sucessors(self.openList.delete())

    def generateFVal(self, node, currentPosition, newPosition):
        return self.generateHVal(currentPosition, newPosition) + self.generateGVal(node.fVal)

    def generateHVal(self, currentPosition, newPosition):
        return math.sqrt(math.pow((newPosition.xVal - currentPosition.xVal), 2) + math.pow((newPosition.yVal - currentPosition.yVal), 2))

    def generateGVal(self, previousVal):
        return previousVal + 1

    def validPosition(self, position):
        if grid.withinBounds(position) and not grid.isBarrier(position):
            return True

    def sucessors(self, node):
        for i in range(0, 3):
            for j in range(0, 3):
                newPosition = coordinate(node.position.xVal + i, node.position.yVal + j)
                if self.validPosition(newPosition):
                    self.openList.insert(self.Node(self.generateFVal(node, node.position, newPosition), newPosition, node.level + 1, node))







if __name__ == '__main__':
    myQueue = PriorityQueue()
    myQueue.insert(12)
    myQueue.insert(1)
    myQueue.insert(14)
    myQueue.insert(7)
    print(myQueue)
    while not myQueue.isEmpty():
        print(myQueue.delete())