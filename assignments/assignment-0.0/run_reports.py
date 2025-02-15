"""
Author: Barrett Kiburz
Date: January 2025

Runs reports of run data from the NighKey app.
"""
from gps_data import GPSData
from running_utils import elevation_gain
import datetime
import math
import pprint
import sys
import time

TOLERANCE = 0.001
EARTH_RADIUS = 6371

def load_data(fileName):
    f = open(fileName, "r")
    runData = []
    lines = f.readlines()
    for line in lines:
        if line != lines[0]:
            elements = line.strip().split(',')
            runData.append(GPSData(float(elements[0]), float(elements[1]), float(elements[2]), elements[3]))
    f.close()
    return runData

def get_distance(latitudeA, latitudeB, longitudeA, longitudeB):
    """
    Finds the distance between two given locations in km using their
    latitude and longitude in degrees.
    """
    latitudeA = math.radians(latitudeA)
    latitudeB = math.radians(latitudeB)
    longitudeA = math.radians(longitudeA)
    longitudeB = math.radians(longitudeB)
    return math.acos(math.sin(latitudeA) * math.sin(latitudeB) + math.cos(latitudeA) * math.cos(latitudeB) *
                     math.cos(longitudeB - longitudeA)) * EARTH_RADIUS

def seconds_between(a, b):
    """
    Computes and returns the difference in time in seconds between
    two given ISO8601 formatted strings `a` and `b`.
    """
    time_a = datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%S")
    time_b = datetime.datetime.strptime(b, "%Y-%m-%dT%H:%M:%S")
    return (time_b-time_a).total_seconds()

def format_seconds(seconds):
    """
    Returns a formatted string of the given number of `seconds`
    into the format "HH:MM:SS"
    """
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def main():
    if len(sys.argv) != 3:
        sys.stderr.write("ERROR: Please provide two data file names as command arguments.\n")
        exit()
    runDataA = load_data(sys.argv[1])
    runDataB = load_data(sys.argv[2])

    print("=====================")
    print("Elevation Report")
    print("=====================")
    runDataA.sort(key = lambda x: x.elevation)
    print(f"Highest Elevation: {runDataA[len(runDataA) - 1].elevation:.2f}m")
    print(f"Lowest Elevation: {runDataA[0].elevation:.2f}m\n")

    print("=====================")
    print("Elevation Gain Report")
    print("=====================")
    runDataA.sort(key = lambda x: x.time)
    elevations = []
    for x in runDataA:
        elevations.append(x.elevation)
    print(f"Elevation Gain: +{elevation_gain(elevations):.2f}m\n")

    print("=====================")
    print("Distance Report")
    print("=====================")
    totalDistance = 0
    for i in range(len(runDataA)):
        if i < len(runDataA) - 1:
            totalDistance += get_distance(runDataA[i].latitude, runDataA[i + 1].latitude, runDataA[i].longitude, runDataA[i + 1].longitude)
    print(f"Total distance: {totalDistance:.2f}km\n")

    print("=====================")
    print("Time Report")
    print("=====================")
    movingTime = 0
    waitTime = 0
    for i in range(len(runDataA)):
        if i < len(runDataA) - 1:
            timeGap = seconds_between(runDataA[i].time, runDataA[i + 1].time)
            if timeGap < 10:
                movingTime += timeGap
            else:
                waitTime += timeGap
    print(f"Moving time: {format_seconds(movingTime)} ({movingTime}s)")
    print(f"Wait time: {format_seconds(waitTime)} ({waitTime}s)")
    print(f"Total time: {format_seconds(waitTime + movingTime)} ({(waitTime + movingTime)}s)\n")

    if len(runDataA) > len(runDataB):
        length = len(runDataA)
    else:
        length = len(runDataB)
    print("==========================================")
    print("Inconsistent/Missing Data Reports")
    print("==========================================")
    runDataB.sort(key = lambda x: x.time)
    missing = 0
    inconsistent = 0
    for i in range(length):
        if runDataA[i].time < runDataB[i].time:
            print("Data point " + str(runDataA[i]) + " missing in Data Set B")
            runDataB.insert(i, runDataA[i])
            missing += 1
        elif runDataA[i].time > runDataB[i].time:
            print("Data point " + str(runDataB[i]) + " missing in Data Set A")
            runDataA.insert(i, runDataB[i])
            missing += 1
        latitudeDiff = abs(runDataA[i].latitude - runDataB[i].latitude)
        longitudeDiff = abs(runDataA[i].longitude - runDataB[i].longitude)
        if latitudeDiff > TOLERANCE or longitudeDiff > TOLERANCE:
            print("Data points are inconsistent:")
            print(str(runDataA[i]))
            print(str(runDataB[i]))
            inconsistent += 1
    print("\nNumber of missing data points: " + str(missing))
    print("Number of inconsistent data points: " + str(inconsistent))

if __name__ == "__main__":
    main()
