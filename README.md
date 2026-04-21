# TurtleBot3 Navigation Monitoring System

## Overview

This project implements a real-time monitoring system for robot navigation using ROS2.
It evaluates performance metrics such as path length, execution time, distance to goal, efficiency, and battery consumption.

## Features

* Real-time monitoring using odometry
* Efficiency calculation (optimal vs actual path)
* CSV logging for offline analysis
* Integration with Nav2 goals
* Docker support for reproducibility

## System Architecture

Navigation (Nav2) → Odometry → Monitoring Node → Metrics → CSV Logging

## How to Run

### 1. Run Simulation (Host Machine)

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True
```

### 2. Run Monitoring Node (Docker)

```bash
docker build -t monitor .
docker run -it --rm --network host monitor
ros2 run tbot3_nav_monitor monitor_node
```

### 3. Send Goal

Use RViz and click “Nav2 Goal” to send a target.

## Output

* Terminal: real-time navigation metrics
* File: `nav_metrics.csv` containing:

  * time
  * path length
  * distance to goal
  * efficiency
  * battery level

## Docker

The monitoring node is containerized using Docker to ensure portability and reproducibility across different environments.

## Author

Hichem Cheriet
