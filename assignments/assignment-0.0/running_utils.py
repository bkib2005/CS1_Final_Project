"""
Author: Barrett Kiburz
Date: January 2025

Two functions that help with data for elevation in a running app.
"""

def elevation_gain(elevations):
    """
    Calculates only the elevation gain from a given array of recorded elevations.
    """
    gain = 0
    for i in range(len(elevations)):
        if i != 0:
            change = elevations[i] - elevations[i-1]
            if change > 0:
                gain += change
    return gain


def convert_map(map):
    """
    Converts a map of elevations recorded in meters to feet.
    """
    for i in range(len(map)):
        for j in range(len(map[i])):
            map[i][j] *= 3.28084
    return map
