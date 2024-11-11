import matplotlib.pyplot as plt
import threading
import time

# Sample Process Data
processes = [
    {"pid": "P1", "burst_time": 15, "arrival_time": 0},
    {"pid": "P2", "burst_time": 20, "arrival_time": 0},
    {"pid": "P3", "burst_time": 20, "arrival_time": 20},
    {"pid": "P4", "burst_time": 20, "arrival_time": 25},
    {"pid": "P5", "burst_time": 5, "arrival_time": 45},
    {"pid": "P6", "burst_time": 15, "arrival_time": 55}
]

n = len(processes)
completion_time = [0] * n
waiting_time = [0] * n
turnaround_time = [0] * n
gantt_chart = []
process_threads = []

# Function to get the next process with the shortest burst time
def get_next_process(time):
    min_time = float('inf')
    index = -1
    for i in range(n):
        if processes[i]["arrival_time"] <= time and completion_time[i] == 0:
            if processes[i]["burst_time"] < min_time:
                min_time = processes[i]["burst_time"]
                index = i
    return index

# Simulation of the SJF non-preemptive scheduling
def sjf_simulation():
    time_unit = 0
    completed = 0
    while completed != n:
        index = get_next_process(time_unit)
        if index != -1:
            gantt_chart.append((processes[index]["pid"], time_unit))  # Log execution for Gantt chart
            time_unit += processes[index]["burst_time"]  # Execute the process completely
            completion_time[index] = time_unit
            turnaround_time[index] = completion_time[index] - processes[index]["arrival_time"]
            waiting_time[index] = turnaround_time[index] - processes[index]["burst_time"]
            completed += 1

# Function to prepare Gantt chart timeline data
def create_gantt_timeline():
    gantt_timeline = []
    last_pid = gantt_chart[0][0]
    start_time = gantt_chart[0][1]
    for i in range(1, len(gantt_chart)):
        if gantt_chart[i][0] != last_pid:
            gantt_timeline.append((last_pid, start_time, gantt_chart[i - 1][1] + processes[n - 1]["burst_time"]))
            last_pid = gantt_chart[i][0]
            start_time = gantt_chart[i][1]
    gantt_timeline.append((last_pid, start_time, gantt_chart[-1][1] + 1))
    return gantt_timeline

# Function to plot Gantt chart and bar charts for Waiting Time and Turnaround Time
def plot():
    gantt_timeline = create_gantt_timeline()

    # Plot Gantt Chart
    fig, (gnt, ax_wait, ax_turnaround) = plt.subplots(1, 3, figsize=(18, 6))
    gnt.set_ylim(0, 10)
    gnt.set_xlim(0, max(completion_time) + 10)
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_title("Gantt Chart for Non-Preemptive SJF Scheduling")

    # Plot Gantt bars
    for process_id, start, finish in gantt_timeline:
        gnt.broken_barh([(start, finish - start)], (3, 4), facecolors=('tab:blue'))
        gnt.text(start + (finish - start) / 2, 5, process_id, ha='center', va='center', color='white', fontweight='bold')
        gnt.text(start, 4.5, f'{start}', ha='center', va='center', color='black')
        gnt.text(finish, 4.5, f'{finish}', ha='center', va='center', color='black')

    # Process IDs for charts
    process_ids = [p["pid"] for p in processes]

    # Plot Waiting Time Bar Chart
    ax_wait.bar(process_ids, waiting_time, color='tab:orange')
    ax_wait.set_title('Waiting Time for Each Process')
    ax_wait.set_xlabel('Process')
    ax_wait.set_ylabel('Waiting Time (in units)')

    # Plot Turnaround Time Bar Chart
    ax_turnaround.bar(process_ids, turnaround_time, color='tab:green')
    ax_turnaround.set_title('Turnaround Time for Each Process')
    ax_turnaround.set_xlabel('Process')
    ax_turnaround.set_ylabel('Turnaround Time (in units)')

    # Display the plots
    plt.tight_layout()
    plt.show()

# Function to simulate the execution in a thread
def thread_simulation():
    sjf_simulation()  # Run the SJF simulation

# Function to print the process summary table
def print_summary():
    print("Process\tArrival Time\tBurst Time\tCompletion Time\tTurnaround Time\tWaiting Time")
    for i in range(n):
        print(f"{processes[i]['pid']}\t{processes[i]['arrival_time']}\t\t{processes[i]['burst_time']}\t\t"
              f"{completion_time[i]}\t\t{turnaround_time[i]}\t\t{waiting_time[i]}")

# Start the simulation in a thread
simulation_thread = threading.Thread(target=thread_simulation)
simulation_thread.start()
simulation_thread.join()  # Wait for the thread to complete

# Print Process Summary Table
print_summary()

# Plot the results
plot()
