# PID Motor Control Package

This repository contains a ROS 2 package designed to simulate a DC motor, generate setpoints, and control the motor using a PID controller.

## Prerequisites

Ensure you have ROS 2 installed and sourced on your system, along with `colcon` for building packages.

## Building the Workspace

1. Navigate to the root of your ROS 2 workspace (e.g., `~/ros2_ws/`).
2. Build the packages using `colcon`:

```bash
colcon build --packages-select custom_interfaces motor_control
```

3. Source the setup file to overlay the new packages onto your environment:

```bash
source install/setup.bash
```

---

## Running the Project

You can launch the entire system (the DC motor simulation, the setpoint generator, and the PID controller) using the provided launch file.

Run the following command in your terminal:

```bash
ros2 launch motor_control motor_launch.py
```

This will start three nodes simultaneously:

- `/motor_sys` (from `dc_motor.py`)
- `/sp_gen` (from `set_point.py`)
- `/ctrl` (from `controller.py`)

---

## Visualizing the Node Graph (rqt_graph)

To verify that your nodes are communicating correctly over their respective topics, you can use `rqt_graph`.

1. Open a new terminal.
2. Source your ROS 2 installation (and workspace if needed).
3. Run the following command:

```bash
rqt_graph
```

This will open a GUI window displaying the nodes and the topics connecting them (e.g., `/set_point`, `/motor_input_u`).

---

## Adjusting Parameters

The nodes are designed to accept parameter updates at runtime. You can adjust the PID gains, the setpoint signal types, and the DC motor constants on the fly.

### Option 1: Using the RQT GUI (Recommended)

Open a new terminal and run:

```bash
rqt
```

In the top menu bar, go to:

**Plugins → Configuration → Parameter Reconfigure**

In the left pane, click on the node you want to tune:

- Select `ctrl` to adjust `kp`, `ki`, `kd`, and `ts` (sampling time).
- Select `sp_gen` to change the signal type (e.g., `"constant"`, `"sine"`, `"square"`) or the amplitude.
- Select `motor_sys` to adjust `sys_gain_K` or `sys_tau_T`.

Modify the values in the right pane. The changes will be applied to the running system immediately.

---

### Option 2: Using the Command Line Interface (CLI)

You can also set parameters directly from the terminal using the `ros2 param` command.

View all available parameters:

```bash
ros2 param list
```

Set specific parameters (examples):

To change the Proportional gain (`kp`) of the controller to `1.5`:

```bash
ros2 param set /ctrl kp 1.5
```

To change the setpoint signal type to a square wave:

```bash
ros2 param set /sp_gen type "square"
```

To change the amplitude of the setpoint signal to `10.0`:

```bash
ros2 param set /sp_gen amplitude 10.0
```

---

## Visualizing Data (Optional)

To see the motor's performance and track how well the output follows the setpoint, you can plot the topic data in real-time.

Run `rqt_plot`:

```bash
rqt_plot
```

In the **Topic** text box:

- Type `/set_point/data` and click the **+** button.
- Type the motor output topic (e.g., `/motor_speed_y/data` or `/motor_output_y/data` depending on your current node connections) and click the **+** button to overlay the system response.
