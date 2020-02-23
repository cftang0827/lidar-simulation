import csv
import numpy as np
from argparse import ArgumentParser
from utils import get_flight_path_from_csv, WallInfoMap, Lidar, write_lidar_points_csv


# Parse argument, get the file name of flight path and lidar points
parser = ArgumentParser()
parser.add_argument("--mapping-files")
parser.add_argument("--flight-path")
parser.add_argument("--lidar-points")
args = parser.parse_args()


def main():

    flight_path = args.flight_path
    lidar_points_path = args.lidar_points
    mapping_path = args.mapping_files

    flight_path_x, flight_path_y = get_flight_path_from_csv(flight_path)
    wall_map = WallInfoMap(mapping_path)
    lidar_object = Lidar(0.5, 0.05, 100, flight_path_x[0], flight_path_y[0], wall_map)
    scan_path_data = [lidar_object.scan()]
    for x, y in zip(flight_path_x[1:], flight_path_y[1:]):
        print("Simulating point ({}, {})".format(x, y))
        lidar_object.update_location(x, y)
        scan_path_data.append(lidar_object.scan())

    write_lidar_points_csv(lidar_points_path, scan_path_data)


if __name__ == "__main__":
    main()
