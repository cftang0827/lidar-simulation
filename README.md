# Lidar Simulation Task

## Introduction
In this repository, we have two tasks, the first one is `display`, and the second one is `simulation`

- Development platform: MacOS
- Development programming language: `Python 3.8`
- Dependencies package: `numpy`, `matplotlib`
- Testing platform: `MacOS`, `Windows with Anaconda 3.7`
- Project layout

```
├── README.md
├── requirements.txt
├── sample-data
│   ├── FlightPath-home-made.csv
│   ├── FlightPath.csv
│   ├── LIDARPoints.csv
│   └── Mapping-home-made.csv
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   └── utils.cpython-38.pyc
│   ├── display.py
│   ├── simulation.py
│   └── utils.py
└── test
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-38.pyc
    │   └── test.cpython-38.pyc
    └── test.py
```

#### 1. Display
In the task, we will input two files `FlightPath.csv` and `LIDARPoints.csv`, the first one is flight path of drone, and the second one is the lidar data fetched by lidar on the drone. We will use these two data to reconstuct and display the scan point from lidar. 

For example, we displayed number 1 path of drone and showed all the data point from lidar
![1](https://i.imgur.com/aW2V7Dw.png)

blue point is the drone flight path, and the number is the number of flight path. Also, the green point is the lidar scan point

x axis and y axis is the absolute coordinate of the system.

#### 2. Simulation
In this task, we will generate our wall information and flight path manually, and then use these data to simulate and generate lidar scan point data. 

After simulation, we could use task 1 `display` to show the wall information. 

For example, we could use display program to show the simulation room
![2](https://i.imgur.com/AQAYARv.png)

## How to run the task

#### 1. Git glone this repository
```shell
$ git clone https://github.com/cftang0827/scoville-lidar-simulation.git
$ cd scoville-lidar-simulation![4](https://i.imgur.com/fwJAlyc.png)
```

#### 2. Install dependencies
```shell
$ pip install -r requirements.txt
```

#### 3. Run unit test
```shell
$ python -m unittest discover
```

#### 4. Display task
```
usage: display.py [-h] [--flight-path FLIGHT_PATH] [--lidar-points LIDAR_POINTS] [--scan-id SCAN_ID]

optional arguments:
  -h, --help            show this help message and exit
  --flight-path FLIGHT_PATH
  --lidar-points LIDAR_POINTS
  --scan-id SCAN_ID
```
`scan-id` is the scan id of the lidar on the drone, use `all` to show all the data

- Example for number 1
```shell
python src/display.py --flight-path sample-data/FlightPath.csv --lidar-points sample-data/LIDARPoints.csv --scan-id 1
```
and you will get
![1](https://i.imgur.com/aW2V7Dw.png)

- Example for all
```shell
$ python src/display.py --flight-path sample-data/FlightPath.csv --lidar-points sample-data/LIDARPoints.csv --scan-id all
```
and you will get the image
![4](https://i.imgur.com/HKvGGsh.png)

**Be aware** if you want to shut down the program, you need to close the figure generate by matplotlib first. 

#### 4. Simulation task
```
usage: simulation.py [-h] [--mapping-files MAPPING_FILES] [--flight-path FLIGHT_PATH] [--lidar-points LIDAR_POINTS]

optional arguments:
  -h, --help            show this help message and exit
  --mapping-files MAPPING_FILES
  --flight-path FLIGHT_PATH
  --lidar-points LIDAR_POINTS
```

- Example
```shell
python src/simulation.py --flight-path sample-data/FlightPath-home-made.csv  --mapping-files sample-data/Mapping-home-made.csv --lidar-points sample-data/lidar-home-made.csv
```

And you will get a lidar scan point data called `lidar-home-made.csv` 
Then you can use `display.py` to show the layout of wall

```shell
python src/display.py --flight-path sample-data/FlightPath-home-made.csv --lidar-points sample-data/lidar-home-made.csv --scan-id all
```
![2](https://i.imgur.com/AQAYARv.png)

