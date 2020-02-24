import unittest
import numpy as np
from src.utils import (
    get_lidar_points_from_csv,
    get_flight_path_from_csv,
    get_point_lidar_edge_data,
    Lidar,
    WallInfoMap,
)


class TestCsvUtility(unittest.TestCase):
    def setUp(self):
        self.test_flight_path_csv_file = "sample-data/FlightPath.csv"
        self.test_lidar_path_csv_file = "sample-data/LIDARPoints.csv"

    def test_get_lidar_points_from_csv(self):
        lidar_points = get_lidar_points_from_csv(self.test_lidar_path_csv_file)
        self.assertEqual(len(lidar_points), 34)

    def test_get_flight_path_from_csv(self):
        flight_path_x, flight_path_y = get_flight_path_from_csv(
            self.test_flight_path_csv_file
        )
        self.assertEqual(type(flight_path_x), np.ndarray)
        self.assertEqual(len(flight_path_x), 34)
        self.assertEqual(len(flight_path_y), 34)

    def test_get_point_lidar_edge_data(self):
        xy = (0, 0)

        # Overall 4 points with 0, 90, 180, 270 degree and with distance 1, 2, 3, 4
        lidar_point_data = (np.array([0, 90, 180, 270]), np.array([1, 2, 3, 4]))
        x_points, y_points = np.round(get_point_lidar_edge_data(xy, lidar_point_data))

        # Test point1
        self.assertEqual(x_points[0], 1)
        self.assertEqual(y_points[0], 0)

        # Test point2
        self.assertEqual(x_points[1], 0)
        self.assertEqual(y_points[1], -2)

        # Test point3
        self.assertEqual(x_points[2], -3)
        self.assertEqual(y_points[2], 0)

        # Test point4
        self.assertEqual(x_points[3], 0)
        self.assertEqual(y_points[3], 4)


class TestLidarObject(unittest.TestCase):
    def setUp(self):
        self.test_angle_precision = 0.1
        self.test_distance_precision = 0.1
        self.test_wall_info_map = WallInfoMap("sample-data/Mapping-home-made.csv")
        self.test_lidar_object = Lidar(
            self.test_angle_precision,
            self.test_distance_precision,
            200,
            0,
            0,
            self.test_wall_info_map,
        )

    def tearDown(self):
        self.test_lidar_object.update_location(0, 0)

    def test_update_location(self):

        self.assertEqual(self.test_lidar_object.location_x, 0)
        self.assertEqual(self.test_lidar_object.location_y, 0)

        self.test_lidar_object.update_location(1, 3)

        self.assertEqual(self.test_lidar_object.location_x, 1)
        self.assertEqual(self.test_lidar_object.location_y, 3)

    def test_scan(self):
        scan_results = self.test_lidar_object.scan()
        self.assertEqual(len(scan_results), 360 / self.test_angle_precision)


class TestWallInfoMap(unittest.TestCase):
    def setUp(self):
        self.wall_info_map = WallInfoMap("sample-data/Mapping-home-made.csv")

    def test_wall_info_map_init(self):
        self.assertEqual(len(self.wall_info_map.mapping_list), 6)

    def test_check_overlap(self):
        out_point = (5, 5)
        self.assertTrue(
            not self.wall_info_map.check_overlap(out_point[0], out_point[1])
        )

        in_point = (8, 5)
        self.assertTrue(self.wall_info_map.check_overlap(in_point[0], in_point[1]))


if __name__ == "__main__":
    unittest.main()
