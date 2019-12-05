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
    return allCrossings

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
    unordered = range(smaller, larger+1)
    return unordered if a < b else reversed(unordered)

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
    '''return a list of all occupied points when traveling the list of points provided'''
    origin = (0,0)
    occupied = [origin]
    for p2 in points:
        nextPoint = add(origin,p2)
        occupied.extend(occupiedPoints(origin, nextPoint)[1:])
        origin = nextPoint
    return occupied

def distanceToClosestCrossing(crossings):
    distances = [manhattanDistance(*point) for point in crossings]
    return min(distances)

def routeInput(route):
    segments = route.split(',')
    points = []
    for s in segments:
        direction = s[0].lower()
        dist = int(s[1:])
        point = globals()[direction](dist)
        points.append(point)
    return points

def distanceToPoint(route, point):
    distances = {}
    total = 0
    for rp in route:
        if not rp in distances:
            distances[rp] = total
        if rp == point:
            break
        total += 1
    return distances[rp]

def bestIntersection(r1, r2):
    cps = findCrossingPoints(r1, r2)
    return min([distanceToPoint(r1, c)+distanceToPoint(r2, c) for c in cps])

class TestWireGrid(unittest.TestCase):

    def test_movement(self):
        self.assertEqual(r(5), (5,0))
        self.assertEqual(r(5, (5,0)), (10,0))
        self.assertEqual(r(5, r(5)), (10,0))

    def test_inclusive(self):
        self.assertEqual(tuple(inclusive(3,5)), (3,4,5))
        self.assertEqual(tuple(inclusive(5,3)), (5,4,3))
        self.assertEqual(tuple(inclusive(-5, -3)), (-5, -4, -3))
        self.assertEqual(tuple(inclusive(-3, -5)), (-3, -4, -5))

    def test_occupiedPoints(self):
        self.assertEqual(occupiedPoints((0,0), (0,0)), (0,0))
        self.assertEqual(occupiedPoints((1,1), (1,1)), (1,1))
        self.assertEqual(occupiedPoints((0,0), (1,0)), ((0,0), (1,0)))
        self.assertEqual(occupiedPoints((0,0), (2,0)), ((0,0), (1,0), (2,0)))
        self.assertEqual(occupiedPoints((2,0),(0,0)), ((2,0), (1,0), (0,0)))

    def test_generateRoute(self):
        self.assertEqual(generateRoute((r(1), u(1))), [(0,0), (1,0), (1,1)])
        self.assertEqual(generateRoute((u(1), r(1))), [(0,0), (0,1), (1,1)])
        self.assertEqual(generateRoute((u(1), r(3),u(1))), [(0,0), (0,1), (1,1), (2,1), (3,1), (3,2)])

    def test_distanceToPoint(self):
        route = generateRoute((u(1), r(3),u(1)))
        self.assertEqual(distanceToPoint(route, (3,2)), 5)
        r1 = generateRoute(routeInput('R8,U5,L5,D3'))
        self.assertEqual(distanceToPoint(r1, (3,3)), 20)
        self.assertEqual(distanceToPoint(r1, (6,5)), 15)
        r2 = generateRoute(routeInput('U7,R6,D4,L4'))
        self.assertEqual(distanceToPoint(r2, (3,3)), 20)
        self.assertEqual(distanceToPoint(r2, (6,5)), 15)

    def test_distanceToPointWithLoop(self):
        r1 = generateRoute(routeInput('U4,R2,D2,L4'))
        self.assertEqual(r1[-1], (-2,2))
        self.assertEqual(distanceToPoint(r1, (-2,2)), 12)

    def test_distanceToPointWithDoubleLoop(self):
        r1 = generateRoute(routeInput('U4,R2,D2,L4,U2,R1,D4'))
        self.assertEqual(r1[-1],(-1,0))
        self.assertEqual(distanceToPoint(r1, (-1,0)), 19)

    def test_distanceToPointContrived(self):
        r1 = generateRoute(routeInput('U4,R2,D2,L4,U2,R1,D4'))
        r2 = generateRoute(routeInput('L1'))
        self.assertEqual(bestIntersection(r1,r2), 20)

    def test_bestIntersection(self):
        r1 = generateRoute(routeInput('R8,U5,L5,D3'))
        r2 = generateRoute(routeInput('U7,R6,D4,L4'))
        self.assertEqual(bestIntersection(r1, r2), 30)

    def test_moreDistanceExamples(self):
        r1 = generateRoute(routeInput('R75,D30,R83,U83,L12,D49,R71,U7,L72'))
        r2 = generateRoute(routeInput('U62,R66,U55,R34,D71,R55,D58,R83'))
        self.assertEqual(bestIntersection(r1, r2), 610)
        r1 = generateRoute(routeInput('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'))
        r2 = generateRoute(routeInput('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'))
        self.assertEqual(bestIntersection(r1, r2), 410)

    def test_findCrossingPoints(self):
        r1 = generateRoute((r(1), u(1)))
        r2 = generateRoute((u(1), r(1)))
        self.assertEqual(findCrossingPoints(r1, r2), {(1,1)})
        doubleLoopRoute = generateRoute(routeInput('U4,R2,D2,L4,U2,R1,D4'))
        leftone = generateRoute((l(1),))
        self.assertEqual(findCrossingPoints(doubleLoopRoute, leftone), {(-1,0)})
        self.assertEqual(bestIntersection(leftone,doubleLoopRoute), 20)

    def test_manhattanDistance(self):
        self.assertEqual(manhattanDistance(3,3), 6)
        self.assertEqual(manhattanDistance(-3,-3), 6)

    def test_distanceToClosestCrossing(self):
        self.assertEqual(distanceToClosestCrossing(((1,1),)), 2)
        self.assertEqual(distanceToClosestCrossing(((1,1),(2,2))), 2)

    def test_routeInput(self):
        self.assertEqual(routeInput('R5'), [r(5)])
        self.assertEqual(routeInput('R1,U1'), [r(1),u(1)])
        self.assertEqual(routeInput('R8,U5,L5,D3'), [r(8), u(5), l(5), d(3)])

    def test_all_together(self):
        r1 = generateRoute(routeInput('R8,U5,L5,D3'))
        r2 = generateRoute(routeInput('U7,R6,D4,L4'))
        crossingPoints = findCrossingPoints(r1,r2)
        self.assertEqual(crossingPoints, {(3,3),(6,5)})
        self.assertEqual(distanceToClosestCrossing(crossingPoints), 6)

    def test_longer_examples(self):
        r1 = generateRoute(routeInput('R75,D30,R83,U83,L12,D49,R71,U7,L72'))
        r2 = generateRoute(routeInput('U62,R66,U55,R34,D71,R55,D58,R83'))
        crossingPoints = findCrossingPoints(r1,r2)
        self.assertEqual(distanceToClosestCrossing(crossingPoints), 159)
        r1 = generateRoute(routeInput('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'))
        r2 = generateRoute(routeInput('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'))
        self.assertEqual(distanceToClosestCrossing(findCrossingPoints(r1,r2)), 135)

if __name__ == '__main__':
    unittest.main()
