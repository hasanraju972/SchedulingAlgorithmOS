import matplotlib.pyplot as plt
from prettytable import PrettyTable
import threading

# Define the processes with burst time and arrival time
processes = [
    {"pid": "P1", "burst_time": 15, "arrival_time": 0},
    {"pid": "P2", "burst_time": 20, "arrival_time": 0},
    {"pid": "P3", "burst_time": 20, "arrival_time": 20},
    {"pid": "P4", "burst_time": 20, "arrival_time": 25},
    {"pid": "P5", "burst_time": 5, "arrival_time": 45},
    {"pid": "P6", "burst_time": 15, "arrival_time": 55}
]

# Time quantum
time_quantum = 5

# Initialize variables
n = len(processes)
remaining_time = [p["burst_time"] for p in processes]  # Remaining burst times
completion_times = [0] * n  # Completion times for each process
gantt_chart = []  # For tracking execution order in Gantt chart
waiting_times = [0] * n  # Waiting time for each process
turnaround_times = [0] * n  # Turnaround time for each process

# Function to simulate Round-Robin scheduling
def round_robin_scheduling():
    global gantt_chart, completion_times, turnaround_times, waiting_times
    time = 0
    while any(rt > 0 for rt in remaining_time):
        for i in range(n):
            if processes[i]["arrival_time"] <= time and remaining_time[i] > 0:
                # Execute the process for time quantum or remaining burst time, whichever is less
                exec_time = min(time_quantum, remaining_time[i])
                gantt_chart.append((processes[i]["pid"], time))  # Log execution for Gantt chart

                time += exec_time
                remaining_time[i] -= exec_time

                # If process completes, record completion time
                if remaining_time[i] == 0:
                    completion_times[i] = time

    # Calculate Turnaround Time and Waiting Time
    for i in range(n):
        turnaround_times[i] = completion_times[i] - processes[i]["arrival_time"]
        waiting_times[i] = turnaround_times[i] - processes[i]["burst_time"]

    # Display table in console
    table = PrettyTable()
    table.field_names = ["Process", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"]
    for i in range(n):
        table.add_row([processes[i]["pid"], processes[i]["arrival_time"], processes[i]["burst_time"],
                       completion_times[i], turnaround_times[i], waiting_times[i]])

    print("Round-Robin Scheduling Results with Time Quantum =", time_quantum)
    print(table)

# Function to plot the Gantt chart
def plot_gantt_chart():
    # Gantt Chart Data Preparation
    gantt_timeline = []
    last_pid = gantt_chart[0][0]
    start_time = gantt_chart[0][1]

    for i in range(1, len(gantt_chart)):
        if gantt_chart[i][0] != last_pid:
            gantt_timeline.append((last_pid, start_time, gantt_chart[i - 1][1] + time_quantum))
            last_pid = gantt_chart[i][0]
            start_time = gantt_chart[i][1]
    gantt_timeline.append((last_pid, start_time, completion_times[-1]))

    # Plot Gantt Chart
    fig, gnt = plt.subplots(figsize=(12, 4))
    gnt.set_ylim(0, 10)
    gnt.set_xlim(0, max([end for _, _, end in gantt_timeline]) + 10)
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_title("Gantt Chart for Round-Robin Scheduling")

    # Plot the Gantt bars
    for process_id, start, finish in gantt_timeline:
        gnt.broken_barh([(start, finish - start)], (3, 4), facecolors=('tab:blue'))
        gnt.text(start + (finish - start) / 2, 5, process_id, ha='center', va='center', color='white', fontweight='bold')
        gnt.text(start, 4.5, f'{start}', ha='center', va='center', color='black')
        gnt.text(finish, 4.5, f'{finish}', ha='center', va='center', color='black')

    plt.tight_layout()
    plt.show()

# Start the scheduling calculations in a separate thread
scheduling_thread = threading.Thread(target=round_robin_scheduling)
scheduling_thread.start()
scheduling_thread.join()  # Wait for the scheduling thread to complete before plotting

# Plot the Gantt chart in the main thread
plot_gantt_chart()
