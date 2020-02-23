import csv

import numpy as np


class WallInfoMap:
    def __init__(self, mapping_path):
        self.mapping_list = []
        with open(mapping_path, newline="") as csvfile:
            rows = csv.reader(csvfile)
            for line, item in enumerate(rows):
                self.mapping_list.append(
                    (float(item[0]), float(item[1]), float(item[2]), float(item[3]))
                )

    def check_overlap(self, x, y):
        for x_start, y_start, x_end, y_end in self.mapping_list:
            if ((x - x_start) * (x - x_end) <= 0) and (
                (y - y_start) * (y - y_end) <= 0
            ):
                return True

        return False


class Lidar:
    def __init__(
        self,
        angle_precision,
        distance_precision,
        longest_distance,
        location_x,
        location_y,
        wall_info_map,
    ):
        self.angle_precision = angle_precision
        self.distance_precision = distance_precision
        self.longest_distance = longest_distance
        self.location_x = location_x
        self.location_y = location_y
        self.wall_info_map = wall_info_map

    def update_location(self, location_x, location_y):
        self.location_x = location_x
        self.location_y = location_y

    def scan(self):

        angle_lists = np.arange(0, 360, self.angle_precision)
        distance_lists = np.arange(0, self.longest_distance, self.distance_precision)
        scan_results = []

        for angle in angle_lists:
            # print(angle)

            x_lists = (
                self.location_x + np.cos((-angle / 360.0) * 2 * np.pi) * distance_lists
            )
            y_lists = (
                self.location_y + np.sin((-angle / 360.0) * 2 * np.pi) * distance_lists
            )

            for dist, (x, y) in enumerate(zip(x_lists, y_lists)):
                if self.wall_info_map.check_overlap(x, y):
                    break
            if dist == len(distance_lists) - 1:
                dist = 0
            scan_results.append(
                (float(angle), float(dist * self.distance_precision * 1000))
            )

        return scan_results


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


def write_lidar_points_csv(lidar_points_path, scan_path_data):
    with open(lidar_points_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        for line, s in enumerate(scan_path_data):
            writer.writerow([line, len(s)])
            for data in s:
                writer.writerow(data)


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
