from wiregrid import *

if __name__ == '__main__':
    with open('day3-wire.txt') as wires:
        lines = wires.readlines()
        r1 = generateRoute(routeInput(lines[0]))
        r2 = generateRoute(routeInput(lines[1]))
        print("Part 1 answer: ",distanceToClosestCrossing(findCrossingPoints(r1,r2)))
        print("crossing points: ",len(findCrossingPoints(r1,r2)))
        print("distances: ",[distanceToPoint(r1, c)+distanceToPoint(r2, c) for c in findCrossingPoints(r1,r2)])
        print("Part 2 answer: ",bestIntersection(r1,r2))
