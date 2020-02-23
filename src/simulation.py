import csv
import numpy as np
from argparse import ArgumentParser


# Parse argument, get the file name of flight path and lidar points
parser = ArgumentParser()
parser.add_argument("--mapping-files")
parser.add_argument("--flight-path")
parser.add_argument("--lidar-points")
args = parser.parse_args()


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
    with open(lidar_points_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        for line, s in enumerate(scan_path_data):
            writer.writerow([line, len(s)])
            for data in s:
                writer.writerow(data)


if __name__ == "__main__":
    main()
