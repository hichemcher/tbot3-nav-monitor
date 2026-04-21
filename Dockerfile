FROM ros:humble-ros-base

RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    ros-humble-navigation2 \
    ros-humble-nav2-msgs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/ws

COPY ./src ./src

RUN . /opt/ros/humble/setup.sh && colcon build

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /root/ws/install/setup.bash" >> ~/.bashrc

CMD ["bash"]
