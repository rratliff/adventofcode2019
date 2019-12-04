from wiregrid import *

if __name__ == '__main__':
    with open('day3-wire.txt') as wires:
        lines = wires.readlines()
        r1 = generateRoute(routeInput(lines[0]))
        r2 = generateRoute(routeInput(lines[1]))
        print("Answer: ",distanceToClosestCrossing(findCrossingPoints(r1,r2)))
