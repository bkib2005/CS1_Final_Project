"""
Author: Barrett Kiburz
Date: January 2025

Reads 3 given points and outputs the distance between each of them
as well as which ones are the closest.
"""
import sys
import math

def get_distance(x1, y1, x2, y2):
    """
    Returns the distance between two given points.
    """
    distance = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
    return distance

def main():
    if len(sys.argv) != 7:
        sys.stderr.write("ERROR: Provide the coordinates as command line arguments like this: xa ya xb yb xc yc\n")
        exit()

    distanceAB = get_distance(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    distanceAC = get_distance(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[5]), float(sys.argv[6]))
    distanceBC = get_distance(float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))

    print("Distance ab: " + str(distanceAB))
    print("Distance ac: " + str(distanceAC))
    print("Distance bc: " + str(distanceBC))

    if distanceAB < distanceAC and distanceAB < distanceBC:
        print("Closest two points: ab")
    elif distanceAC < distanceAB and distanceAC < distanceBC:
        print("Closest two points: ac")
    elif distanceBC < distanceAB and distanceBC < distanceAC:
        print("Closest two points: bc")

if __name__ == "__main__":
    main()
