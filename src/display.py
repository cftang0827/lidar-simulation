import csv
import sys
import time
from argparse import ArgumentParser

import numpy as np
from matplotlib import pyplot as plt

# Parse argument, get the file name of flight path and lidar points
parser = ArgumentParser()
parser.add_argument("--flight-path")
parser.add_argument("--lidar-points")
parser.add_argument("--scan-id")
args = parser.parse_args()


def get_flight_path_from_csv(filename):
    flight_path_x = []
    flight_path_y = []
    with open(filename, newline="") as csvfile:
        rows = csv.reader(csvfile)

        for line, item in enumerate(rows):
            if line % 2 == 1:
                flight_path_x.append(float(item[0]))
                flight_path_y.append(float(item[1]))

    flight_path_x = np.array(flight_path_x)
    flight_path_y = np.array(flight_path_y)

    return flight_path_x, flight_path_y


def get_lidar_points_from_csv(filename):

    with open(filename, newline="") as csvfile:
        rows = csv.reader(csvfile)
        lidar_points = []
        for line, item in enumerate(rows):
            if line == 0:
                point_number, angle_point_number = float(item[0]), float(item[1])

            if line % (angle_point_number + 1) == 0:
                angles = []
                distances = []
            else:
                angles.append(float(item[0]))
                distances.append(float(item[1]) / 1000)

            if line % (angle_point_number + 1) == angle_point_number:
                lidar_points.append((np.array(angles), np.array(distances)))

    return lidar_points


def get_point_lidar_edge_data(point_xy, lidar_point_data):

    edge_points = []
    angle_points = lidar_point_data[0]
    distances = lidar_point_data[1]
    x, y = point_xy

    x_points = x + np.cos((-angle_points / 360.0) * 2 * np.pi) * distances
    y_points = y + np.sin((-angle_points / 360.0) * 2 * np.pi) * distances

    return x_points, y_points


def plot_all(
    axs, point_index, flight_path_x, flight_path_y, lidar_points, annotate=False
):
    x_points, y_points = get_point_lidar_edge_data(
        (flight_path_x[point_index], flight_path_y[point_index]),
        lidar_points[point_index],
    )

    axs.plot(flight_path_x, flight_path_y, "bo")

    if annotate:
        for index, (x, y) in enumerate(zip(flight_path_x, flight_path_y)):
            axs.annotate(
                "{}".format(index),
                xy=(x, y),
                xytext=(-20, 10),
                textcoords="offset points",
            )

    axs.scatter(x_points, y_points, s=2, c="g", marker="x")

    axs.plot(flight_path_x[point_index], flight_path_y[point_index], "ro")


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
