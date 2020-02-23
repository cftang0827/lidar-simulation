import csv
import sys
import time
from argparse import ArgumentParser
from utils import (
    get_flight_path_from_csv,
    get_lidar_points_from_csv,
    get_point_lidar_edge_data,
    plot_all,
)

import numpy as np
from matplotlib import pyplot as plt

# Parse argument, get the file name of flight path and lidar points
parser = ArgumentParser()
parser.add_argument("--flight-path")
parser.add_argument("--lidar-points")
parser.add_argument("--scan-id")
args = parser.parse_args()


def main():

    flight_path = args.flight_path
    lidar_points_path = args.lidar_points
    scan_id = args.scan_id

    flight_path_x, flight_path_y = get_flight_path_from_csv(flight_path)
    lidar_points = get_lidar_points_from_csv(lidar_points_path)
    if len(flight_path_x) != len(flight_path_y) or len(flight_path_x) != len(
        lidar_points
    ):
        raise Exception(
            "Some errors in flight path file or lidar points file, number not match"
        )
    try:
        fig, axs = plt.subplots(1, 1)
        if not scan_id.isdigit():
            if scan_id.lower().strip() != "all":
                raise Exception(
                    'Error in input scan_id, only scan id number and "all" are available'
                )
            for index in range(len(flight_path_x)):

                annotate = True if index == 0 else False
                plot_all(
                    axs,
                    index,
                    flight_path_x,
                    flight_path_y,
                    lidar_points,
                    annotate=annotate,
                )
            plt.title("Simulation figure")
            plt.show()

        else:
            scan_id = int(scan_id)
            if scan_id >= len(flight_path_x) or scan_id < 0:
                raise Exception(
                    "Scan id {} is not match, only 0 - {} are available".format(
                        scan_id, len(flight_path_x) - 1
                    )
                )
            plot_all(
                axs, scan_id, flight_path_x, flight_path_y, lidar_points, annotate=True
            )
            plt.title("Simulation figure")
            plt.show()
    except Exception as e:
        print("Error message: {}".format(e))
        exit()


if __name__ == "__main__":
    main()
