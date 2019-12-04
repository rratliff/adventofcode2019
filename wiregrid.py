import unittest

def manhattanDistance(x, y):
    '''given a point, find its manhattan distance'''
    return abs(x) + abs(y)

def findCrossingPoints(route1, route2):
    '''given 2 routes, find all the crossing points'''
    s1 = set(route1)
    s2 = set(route2)
    allCrossings = s1.intersection(s2)
    allCrossings.remove((0,0))
    return tuple(allCrossings)

def r(dist, origin=(0,0)):
    x1, y1 = origin
    return x1+dist, y1

def l(dist, origin=(0,0)):
    x1, y1 = origin
    return x1-dist, y1

def u(dist, origin=(0,0)):
    x1, y1 = origin
    return x1, y1+dist

def d(dist, origin=(0,0)):
    x1, y1 = origin
    return x1, y1-dist

def inclusive(a,b):
    smaller = min(a,b)
    larger = max(a,b)
    return tuple(range(smaller, larger+1))

def add(p1, p2):
    return (p1[0]+p2[0], p1[1]+p2[1])

def occupiedPoints(p1, p2):
    if p1 == p2:
        return p1
    elif p1[0] == p2[0]:
        # travel in the y direction
        return tuple(((p1[0], y) for y in inclusive(p1[1], p2[1])))
    elif p1[1] == p2[1]:
        # travel in the x direction
        return tuple(((x, p1[1]) for x in inclusive(p1[0], p2[0])))
    else:
        raise ValueError("We don't know how to route a wire from {} to {}".format(p1, p2))

def generateRoute(points):
    # return a list of all occupied points when traveling the list of points provided
    occupied = []
    occupied.append((0,0))
    for origin, p2 in zip(points[:-1], points[1:]):
        nextPoint = add(origin,p2)
        occupied.extend(occupiedPoints(origin, nextPoint))
    return tuple(occupied)


class TestWireGrid(unittest.TestCase):

    def test_wireRoute(self):
        self.assertEqual(r(5), (5,0))
        self.assertEqual(r(5, (5,0)), (10,0))
        self.assertEqual(r(5, r(5)), (10,0))

    def test_inclusive(self):
        self.assertEqual(inclusive(3,5), (3,4,5))
        self.assertEqual(inclusive(-5, -3), (-5, -4, -3))
        self.assertEqual(inclusive(-3, -5), (-5, -4, -3))

    def test_occupiedPoints(self):
        self.assertEqual(occupiedPoints((0,0), (0,0)), (0,0))
        self.assertEqual(occupiedPoints((1,1), (1,1)), (1,1))
        self.assertEqual(occupiedPoints((0,0), (1,0)), ((0,0), (1,0)))
        self.assertEqual(occupiedPoints((0,0), (2,0)), ((0,0), (1,0), (2,0)))

    def test_generateRoute(self):
        self.assertEqual(generateRoute((r(1), u(1))), ((0,0), (1,0), (1,1)))
        self.assertEqual(generateRoute((u(1), r(1))), ((0,0), (0,1), (1,1)))

    def test_routeCrossings(self):
        r1 = generateRoute((r(1), u(1)))
        r2 = generateRoute((u(1), r(1)))
        self.assertEqual(findCrossingPoints(r1, r2), tuple(tuple(1,1)))

    def test_manhattanDistance(self):
        self.assertEqual(manhattanDistance(3,3), 6)
        self.assertEqual(manhattanDistance(-3,-3), 6)


if __name__ == '__main__':
    unittest.main()
